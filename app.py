from dotenv import load_dotenv

load_dotenv() # load the env variables from .env
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("API_KEY"))

## FUNCTION TO LOAD GEMINI PRO VISION

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text



def input_image_details(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()

        image_part = [{
            "mime_type": upload_file.type,
            "data": bytes_data
        }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file Uploaded")




#  Initialize our streamlit app
st.set_page_config(page_title="Multi invoice Extractor")
st.header("Multi invoice Extractor")
input = st.text_input("input Prompt:  ",key='input')
uploaded_file = st.file_uploader("Choose an image... ",type=['jpg','jpeg','png'])

image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image Uploaded", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt= """
You are expert in understanding invoices. We will upload a image as invoices and you will have to answer any question based on the uploaded invoice image
"""

# if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is ")
    st.write(response)