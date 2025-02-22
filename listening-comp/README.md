Application Listening Comp works with LLM and Deep Learning Models to support following features:

- ASL Recognition - Rule Based
- ASL Recognition - Machine Learning
- JLPT Listening Practice

# JLPT Listening Practice

Uses Amazon Bedrock to generate JLPT Listening Practice questions and Save them in JSON file.

# ASL Recognition

Uses Mediapipe and OpenCV to detect hand landmarks and recognize ASL signs. Following Libraries are used:
    - Flask: Web server framework for the API
    - Flask-CORS: Handling cross-origin requests
    - mediapipe: Hand landmark detection
    - numpy: Mathematical operations and array handling
    - cv2 (OpenCV): Image processing and computer vision tasks

# ASL Recognition - Machine Learning

Uses Streamlit to create an interactive web interface, image processing libraries to prepare the input images, and a PyTorch-based deep learning model in the backend to perform the ASL recognition. 

Machine Learning Model -  ResNet18 which is configured to recognize 24 distinct classes or categories of ASL signs. This likely corresponds to 24 letters of the alphabet, excluding 'J' and 'Z' which typically involve motion
Streamlit: Creates the user interface, handles file uploads, displays images, and presents the prediction results.
Image Handling (PIL, OpenCV, NumPy)
ASL Recognition Model (PyTorch, torchvision, mediapipe)
    - Load a pre-trained ResNet model.
    - Modify the model for ASL classification (24 letters).
    - Preprocess images to be compatible with the model.
    - Use the model to predict the ASL sign in the image.
    - Determine the confidence of the prediction.

## How to run frontend

```sh
streamlit run frontend/home.py
```

## How to run backend

```sh
cd backend
pip install -r requirements.txt
cd ..
python backend/main.py
```