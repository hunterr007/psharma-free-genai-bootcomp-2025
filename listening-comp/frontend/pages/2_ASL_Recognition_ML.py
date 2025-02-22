import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import sys
import os
import time
import logging
import traceback
import asyncio
import nest_asyncio

# Apply nest_asyncio at the beginning of your script, but only once
try:
    nest_asyncio.apply()
except RuntimeError as e:
    if "There is no current event loop in thread" in str(e):
        print("Event loop already running, skipping nest_asyncio.apply()")
    else:
        raise  # Re-raise the exception if it's not the expected one

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add backend directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_dir)

def load_and_resize_image(uploaded_file, max_size=800):
    """Load and resize image while maintaining aspect ratio"""
    try:
        image = Image.open(uploaded_file)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image, None
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        return None, str(e)

# Initialize ASL recognition
@st.cache_resource
def get_asl_recognizer():
    try:
        from backend.asl_recognition_ml import ASLRecognitionML
        recognizer = ASLRecognitionML()
        logger.info("ASL recognizer initialized successfully")
        return recognizer
    except Exception as e:
        logger.error(f"Error initializing ASL recognizer: {e}\n{traceback.format_exc()}")
        st.error("Error initializing ASL recognizer. Please check the logs for details.")
        return None

def start_ml_asl_recognition():
    st.title("ASL Recognition with Machine Learning")
    
    # Initialize session state for recognized character
    if 'recognized_char' not in st.session_state:
        st.session_state.recognized_char = ""
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an ASL image...", type=['jpg', 'jpeg', 'png'])
    
    # Initialize ASL recognizer only when needed
    asl_recognizer = get_asl_recognizer()
    if asl_recognizer is None:
        st.error("Failed to initialize ASL recognition system. Please refresh the page or contact support.")
        return
    
    if uploaded_file:
        # Load and preprocess image
        image, error = load_and_resize_image(uploaded_file)
        if error:
            st.error(f"Error loading image: {error}")
            return
        
        try:
            # Display the original image
            st.subheader("Original Image")
            st.image(image, use_container_width=False)

            # Get prediction
            try:
                logger.info("Calling predict_sign...")
                prediction = asl_recognizer.predict_sign(image)
                logger.info(f"predict_sign returned: {prediction}")
                
                if isinstance(prediction, dict):
                    if "letter" in prediction:
                        # Update session state
                        st.session_state.recognized_char = prediction['letter']
                        st.write(f"### Predicted Letter: {st.session_state.recognized_char}")
                        st.write("### Confidence:")
                        
                        if "confidence" in prediction:
                            confidence = prediction["confidence"] * 100
                            st.progress(min(confidence / 100, 1.0))
                            st.text(f"Confidence: {confidence:.1f}%")
                    elif "error" in prediction:
                        st.warning(prediction["error"])
                else:
                    st.warning("Invalid prediction format")
                
            except Exception as e:
                logger.error(f"Error getting prediction: {e}\n{traceback.format_exc()}")
                st.error("Error getting prediction. Please try another image.")

        except Exception as e:
            logger.error(f"Error processing image: {e}\n{traceback.format_exc()}")
            st.error("Error processing image. Please try another image.")

if __name__ == "__main__":
    start_ml_asl_recognition()