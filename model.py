### Invoice extractor (modified for pet image analysis)

## Importing All the modules
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv


# Load all environment Variables
load_dotenv()

## Configuring the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Vison Pro Vision Model and Get response

def get_gemini_response(image, prompt):

  ## Loading the desired Model
  model= genai.GenerativeModel("gemini-pro-vision")
  response=model.generate_content([image[0],prompt])
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

#  Initializing our Streamlit Prompt

st.set_page_config(page_title="Pet Image Analyzer")

st.header("Analyze Your Pet's Image")

## Removed user input for text prompt

uploaded_file = st.file_uploader("Choose a pet image...", type=["jpg", "jpeg", "png","webp"])
image = None

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="Uploaded Image.", use_column_width=True)

  ## Defining a System Prompt (pre-defined)
  input_prompt = f"""Image: (content of the uploaded image)

  Text: Analyze the image and provide the following information:

  * Breed: Identify the breed of the animal in the image (if possible).
  * Disease Detection: If the image shows a diseased area, identify the specific disease (if possible).
  * Severity: If a disease is detected, assess the severity of the disease.
  * Symptoms: Describe the common symptoms associated with the detected disease.
  * Precautions: Recommend preventative measures to avoid the disease.

  Give response with headings,
  Inform the user if the image is not related to pet care.
  """

  submit = st.button("Analyze Image")
  Disclaimer ="""**Disclaimer:** 

This application uses image analysis to provide potential information about your pet's health. The results are for informational purposes only and should not be considered a replacement for professional veterinary diagnosis. 

For any concerns about your pet's health, please consult a licensed veterinarian. They can conduct a thorough examination and provide personalized recommendations for your pet's well-being."""


  if submit:
    if image:
      image_data = input_image_setup(uploaded_file)
      response = get_gemini_response(image_data, input_prompt)

      st.subheader("Analysis Result:")
      st.write(response)
      st.warning(Disclaimer)
    else:
      st.error("Please upload an image to proceed.")

else:
  st.info("Upload an image of your pet to get started!")
  
# st.balloons()
