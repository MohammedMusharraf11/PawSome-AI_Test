###        Invoice extractor

##Importing All the modules
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv


# Load all environment Variables
load_dotenv()

##Configuring the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Vison Pro Vision Model and Get response

def get_gemini_response(input,image,prompt):

    ##Loading the desired Model
    model= genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image[0],prompt])
    return response.text

## Function to extract data from Image Uploaded
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
#       Initializing our Streamlit Prompt

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

##  DEFINING A SYSTEM PROMPT

input_prompt = "You are an expert in Disease detection in pets mostly in Dogs.You will receive infected regions of pets as input images and you will have to answer question based on the input image.and along with if it is possible to detect breed and do tell about symptoms and initial precautions to be taken care-of."

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)

    st.subheader("The Response Generated by your model Gemini Pro Vision is: ")
    st.write(response)

    st.balloons()