import streamlit as st
import google.generativeai as genai
import pyttsx3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Google Generative AI with API key
genai.configure(api_key=api_key)

# Initialize Gemini model for chat
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

# Function to get response from Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function to speak the response using pyttsx3
def speak_response(response_content):
    engine = pyttsx3.init()
    engine.say(response_content)
    engine.runAndWait()

# Streamlit UI components
st.set_page_config(page_title="Gemini ChatBot")
st.title("Gemini ChatBot")

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Voice response checkbox
voice_response = st.checkbox("Enable Voice Response")

# Chat container to display messages
chat_container = st.container()

# Display chat messages from history
for message in st.session_state['messages']:
    with chat_container:
        if message["role"] == "user":
            st.image("user_avatar.png", width=50)
            st.text_area("You:", value=message["content"], height=100, disabled=True)
        elif message["role"] == "bot":
            st.image("bot_avatar.png", width=50)
            st.text_area("Bot:", value=message["content"], height=100, disabled=True)
        st.markdown("---")

# Handle user input and display bot response
if prompt := st.text_input("You:"):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Get response from Gemini model
    response = get_gemini_response(prompt)

    # Extract text from response chunks
    bot_response = "\n".join([chunk.text for chunk in response])

    # Display bot response
    with chat_container:
        st.image("bot_avatar.png", width=50)
        st.text_area("Bot:", value=bot_response, height=100, disabled=True)
        st.markdown("---")

    # Speak the response if voice response checkbox is checked
    if voice_response:
        speak_response(bot_response)

    # Add bot response to session state chat history
    st.session_state['messages'].append({"role": "bot", "content": bot_response})
