import streamlit as st

def welcome():
    

    # Home page content
    st.title("Welcome to PawSome-AI 🐾")
    st.subheader("Your AI-Powered Pet Care Assistant")

    st.markdown("""
    ### About PawSome-AI
    PawSome-AI is a comprehensive web application designed to assist pet owners with various aspects of pet care using advanced AI technologies. Our app offers a range of features to help you better understand and take care of your pets.

    ### Key Features

    1. **Dog Breed Identification and Disease Detection**
       - Upload images of your dog or any infected area.
       - Our AI model identifies the breed of the dog.
       - Detects potential diseases from the images.
       - Provides symptoms, precautions, and possible medications for detected diseases.

    2. **Pet Care Chatbot**
       - Interactive chatbot for pet-care-related queries.
       - Utilizes the LLMA index to provide information from a pet-care encyclopedia.
       - Speaks responses to enhance user experience.

    3. **Future Feature: Prescription Analyzer**
       - Upload images of veterinary prescriptions.
       - Our planned feature will interpret and provide details on the medication and dosage.

    4. **Contact and Feedback**
       - Contact form for user inquiries.
       - Feedback form to collect user suggestions and improvements.

    ### How to Use
    - Navigate through the app using the sidebar.
    - Start with uploading an image on the 'Dog Breed and Disease Detection' page.
    - Interact with our pet care chatbot for any questions.
    - Stay tuned for the upcoming 'Prescription Analyzer' feature.
    - Use the 'Contact' page to reach out to us and the 'Feedback' page to provide your valuable suggestions.

    We hope PawSome-AI makes pet care easier and more effective for you. Thank you for using our app!
    """)
