Application Listening Comp works with LLM and Deep Learning Models to support following features:

- ASL Recognition - Rule Based
- ASL Recognition - Machine Learning
- JLPT Listening Practice
- YouTube Transcriber

# JLPT Listening Practice
clear
Uses Amazon Bedrock to generate JLPT Listening Practice questions and Save them in JSON file.

# ASL Recognition

Uses Mediapipe and OpenCV to detect hand landmarks and recognize ASL signs. Following Libraries are used:
    - Flask: Web server framework for the API
    - Flask-CORS: Handling cross-origin requests
    - mediapipe: Hand landmark detection
    - numpy: Mathematical operations and array handling
    - cv2 (OpenCV): Image processing and computer vision tasks

![image](https://github.com/user-attachments/assets/4c885189-fdc2-405c-857c-93c2a558ab86)

[Demo](https://github.com/hunterr007/psharma-free-genai-bootcomp-2025/blob/b46231008725701e394743de2132a4b0031eeb98/listening-comp/ASL%20Recongnition%202025-02-22%20at%206.44.11%E2%80%AFPM.mov)

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

***It is learnt that training data quality is very important in order to correctly identify the characters.***

![image](https://github.com/user-attachments/assets/e11ba04d-5375-4d07-828f-2485626eea86)

# How to start front end
```sh
streamlit run frontend/home.py
```

# How to start back end
```sh
cd backend
pip install -r requirements.txt
cd ..
python backend/main.py
```
