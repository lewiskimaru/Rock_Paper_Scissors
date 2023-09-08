import streamlit as st
import cv2
import numpy as np

# Create a Streamlit web app
st.title('OpenCV and Streamlit Example')

# Upload an image using Streamlit's file uploader
image = st.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

if image is not None:
    # Read the uploaded image using OpenCV
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), 1)

    # Perform some image processing using OpenCV (e.g., resize, filter, etc.)
    # For example, you could apply a grayscale filter:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the original and processed images using Streamlit
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(gray_image, caption='Grayscale Image', use_column_width=True)
