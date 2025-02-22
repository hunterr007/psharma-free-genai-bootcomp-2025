import streamlit as st
import requests
import traceback
from PIL import Image
import io
import numpy as np

BACKEND_URL = "http://localhost:8000"

def start_asl_recognition():
    """Handles ASL image upload and recognition."""
    st.title("ASL Sign Recognition")
    st.write("Upload an image of an ASL hand sign to recognize the letter.")
    
    # Initialize session state for prediction if it doesn't exist
    if 'predicted_letter' not in st.session_state:
        st.session_state.predicted_letter = ""
    
    # Create a placeholder for the prediction text box
    prediction_container = st.empty()
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an ASL image...", type=['jpg', 'jpeg', 'png'], key="asl_uploader")
    
    # Clear prediction if no file is uploaded
    if not uploaded_file:
        st.session_state.predicted_letter = ""
    
    # Process uploaded file
    if uploaded_file:
        try:
            # Read the file as bytes
            image_bytes = uploaded_file.getvalue()
            
            # Convert bytes to numpy array
            image = Image.open(io.BytesIO(image_bytes))
            
            # Resize the image
            aspect_ratio = image.height / image.width
            new_width = 200
            new_height = int(new_width * aspect_ratio)
            image = image.resize((new_width, new_height))
            
            # Display the image directly
            st.image(image, caption='Uploaded ASL Sign', use_container_width=False)
            
            # Send the original image to the backend for ASL recognition
            files = {'image': uploaded_file}
            response = requests.post(f"{BACKEND_URL}/predict_asl", files=files)
            response.raise_for_status()
            result = response.json()
            
            # Update the predicted letter in session state
            st.session_state.predicted_letter = result.get("letter", "No prediction")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error sending image to backend: {e}")
            st.session_state.predicted_letter = "Error in prediction"
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.error(traceback.format_exc())
            st.session_state.predicted_letter = "Error in prediction"
    
    # Always show the text box with the current prediction
    prediction_container.text_input(
        "Identified Character",
        value=st.session_state.predicted_letter,
        disabled=True,
        key="prediction_display"
    )

if __name__ == "__main__":
    start_asl_recognition()
