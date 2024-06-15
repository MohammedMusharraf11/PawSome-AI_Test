import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

def chatbot():
    st.info("Chatbot function called")  # Debug statement
    
    def run_chat_with_pdf():
        st.info("run_chat_with_pdf function called")  # Debug statement

        # Load environment variables
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        st.info(f"API Key loaded: {api_key is not None}")  # Debug statement
        genai.configure(api_key=api_key)

        # Define functions
        def get_pdf_text(pdf_docs):
            text = ""
            for pdf in pdf_docs:
                try:
                    pdf_reader = PdfReader(pdf)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            st.info(f"Extracted text length: {len(text)}")  # Debug statement
            return text

        def get_text_chunks(text):
            try:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
                chunks = text_splitter.split_text(text)
                st.info(f"Number of text chunks: {len(chunks)}")  # Debug statement
                return chunks
            except Exception as e:
                st.error(f"Error splitting text into chunks: {e}")
                return []

        def get_vector_store(text_chunks):
            try:
                embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                vector_store = FAISS.from_texts(text_chunks, embedding=embedding_function)
                vector_store.save_local("faiss_index")
                st.info("Vector store created and saved")  # Debug statement
            except Exception as e:
                st.error(f"Error creating vector store: {e}")

        def get_conversational_chain():
            try:
                prompt_template = """
                Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
                provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
                Context:\n {context}?\n
                Question: \n{question}\n

                Answer:
                """
                model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
                prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
                chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
                st.info("Conversational chain created")  # Debug statement
                return chain
            except Exception as e:
                st.error(f"Error creating conversational chain: {e}")
                return None

        def user_input(user_question):
            try:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
                docs = new_db.similarity_search(user_question)
                st.info(f"Documents found for question: {len(docs)}")  # Debug statement
                chain = get_conversational_chain()
                if chain:
                    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
                    return response["output_text"]
                else:
                    return "Error creating conversational chain."
            except Exception as e:
                st.error(f"Error processing user input: {e}")  # Debug statement
                return "An error occurred while processing your question."

        # Main function
        def main():
            st.header("Chat with PDF using Gemini")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            st.info("Displaying file uploader")  # Debug statement
            with st.form(key="uploader_form"):
                pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
                submit_button = st.form_submit_button(label="Submit & Process")

            if submit_button:
                if pdf_docs:
                    with st.spinner("Processing..."):
                        try:
                            raw_text = get_pdf_text(pdf_docs)
                            if raw_text:
                                text_chunks = get_text_chunks(raw_text)
                                if text_chunks:
                                    get_vector_store(text_chunks)
                                    st.success("Processing completed successfully.")
                                else:
                                    st.error("No text chunks generated.")
                            else:
                                st.error("No text extracted from PDFs.")
                        except Exception as e:
                            st.error(f"Error processing PDF files: {e}")
                else:
                    st.warning("Please upload at least one PDF file.")

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Ask a question from the PDF files"):
                st.info(f"User prompt: {prompt}")  # Debug statement
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                response = user_input(prompt)
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

        if __name__ == "__main__":
            main()

    # Call the function to run the app
    run_chat_with_pdf()
