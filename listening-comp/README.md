## How to run frontend

```sh
streamlit run frontend/main.py
```

## How to run backend

```sh
cd backend
pip install -r requirements.txt
cd ..
python backend/main.py
```
# ASL Recognition

## Project Structure
### Frontend Files:
    - frontend/Home.py: Main landing page that introduces the application features
    - frontend/pages/1_ASL_Recognition.py: Handles ASL image upload and display
    - frontend/main.py: Original implementation (now moved to pages structure)
### Backend Files:
    - backend/api.py: Flask API server handling image processing requests
    - backend/asl_recognition.py: Core ASL recognition logic using geometric approach

## Technical Libraries and Their Purposes
### Frontend Libraries:
    - streamlit: Web interface framework for creating the UI
    - PIL (Python Imaging Library): Image processing, resizing, and format handling
    - requests: Making HTTP requests to the backend API
    - io: Handling byte streams for image processing

### Backend Libraries:
    - Flask: Web server framework for the API
    - Flask-CORS: Handling cross-origin requests
    - mediapipe: Hand landmark detection
    - numpy: Mathematical operations and array handling
    - cv2 (OpenCV): Image processing and computer vision tasks