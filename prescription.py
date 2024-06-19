import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from scrap import search_medicine_1mg  # Import the scraper function

def presc_analyze():
    # Load environment variables
    load_dotenv()

    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Function to load Gemini Vision Pro model and get response
    def get_gemini_response(input_prompt, image_data, user_prompt):
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([input_prompt, image_data[0], user_prompt])
        return response.text

    # Function to extract data from uploaded image
    def input_image_setup(uploaded_file):
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data,
                }
            ]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded")

    def extract_medicine_names_heuristic(text):
        import re
        # Split based on common delimiters, numbers, or new lines
        potential_medicines = re.split(r'\d+\.\s*|\n|\r|,', text)
        # Clean up and filter out non-medicines
        potential_medicines = [med.strip() for med in potential_medicines if med.strip() and med.lower() not in ["the", "to", "of", "and", "is"]]
        return potential_medicines

    # Streamlit app configuration
    # st.set_page_config(page_title="Prescription & Medicine Information Extractor")
    st.header("Prescription & Medicine Information Extractor")

    user_prompt = "Give me the details about the Prescription and along with basic personal details and tell about medications and frequency in a proper tabular form"
    uploaded_file = st.file_uploader("Choose a Prescription Image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    submit = st.button("Extract Information")

    # System prompt for understanding prescriptions
    info_prompt = """You are an expert in understanding prescriptions. 
    You will receive prescription images and answer questions based on them. 
    Please consider the following information: {user_prompt}"""

    # System prompt for extracting medicine names (heuristic)
    medicine_prompt = "Please list all the medications mentioned in the prescription."

    if submit:
        image_data = input_image_setup(uploaded_file)

        # Extract information based on user prompt
        info_response = get_gemini_response(info_prompt.format(user_prompt=user_prompt), image_data, "")
        st.subheader("Extracted Information:")
        st.write(info_response)

        # Extract medicine names using a separate query
        medicine_response = get_gemini_response(medicine_prompt, image_data, "")
        medicine_names = extract_medicine_names_heuristic(medicine_response)

        if medicine_names:
            st.subheader("Medicine Names:")
            # Store medicine names in a list
            medicine_list = ", ".join(medicine_names)
            st.write(medicine_list)

            # Display at least 6-7 medicines with clickable links for each extracted medicine name
            st.subheader("Medicines with Links:")
            for medicine in medicine_names:
                st.markdown(f"### {medicine}")
                results_df = search_medicine_1mg(medicine)
                if results_df is not None and not results_df.empty:
                    for index, row in results_df.head(7).iterrows():
                        st.markdown(f"[{row['Product name']}]({row['Link']}) - {row['Price']} ₹")
                else:
                    st.write(f"No results found for {medicine}")
        else:
            st.write("No medicine names found using the heuristic approach.")

        st.balloons()

if __name__ == '__main__':
    presc_analyze()
