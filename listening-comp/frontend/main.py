import streamlit as st
import sys
import os
import json
from datetime import datetime
import cv2
import numpy as np
import requests  # To send images to the backend
from PIL import Image
import io
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.question_generator import QuestionGenerator
from backend.audio_generator import AudioGenerator
from frontend import home

# Page config
st.set_page_config(
    page_title="JLPT Listening Practice",
    page_icon="🎧",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000"  # Replace with your backend URL

def load_stored_questions():
    """Load previously stored questions from JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backend/data/stored_questions.json"
    )
    if os.path.exists(questions_file):
        with open(questions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_question(question, practice_type, topic, audio_file=None):
    """Save a generated question to JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backend/data/stored_questions.json"
    )
    
    # Load existing questions
    stored_questions = load_stored_questions()
    
    # Create a unique ID for the question using timestamp
    question_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Add metadata
    question_data = {
        "question": question,
        "practice_type": practice_type,
        "topic": topic,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audio_file": audio_file
    }
    
    # Add to stored questions
    stored_questions[question_id] = question_data
    
    # Save back to file
    os.makedirs(os.path.dirname(questions_file), exist_ok=True)
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(stored_questions, f, ensure_ascii=False, indent=2)
    
    return question_id

def render_interactive_stage():
    """Render the interactive learning stage"""
    # Initialize session state
    if 'question_generator' not in st.session_state:
        st.session_state.question_generator = QuestionGenerator()
    if 'audio_generator' not in st.session_state:
        st.session_state.audio_generator = AudioGenerator()
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'current_practice_type' not in st.session_state:
        st.session_state.current_practice_type = None
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'show_asl' not in st.session_state:
        st.session_state.show_asl = False
    if 'predicted_letter' not in st.session_state:
        st.session_state.predicted_letter = ""
        
    # Load stored questions for sidebar
    stored_questions = load_stored_questions()
    
    # Create sidebar
    with st.sidebar:
        st.header("Saved Questions")
        if stored_questions:
            for qid, qdata in stored_questions.items():
                # Create a button for each question
                button_label = f"{qdata['practice_type']} - {qdata['topic']}\n{qdata['created_at']}"
                if st.button(button_label, key=qid):
                    st.session_state.current_question = qdata['question']
                    st.session_state.current_practice_type = qdata['practice_type']
                    st.session_state.current_topic = qdata['topic']
                    st.session_state.current_audio = qdata.get('audio_file')
                    st.session_state.feedback = None
                    st.rerun()
        else:
            st.info("No saved questions yet. Generate some questions to see them here!")
    
    # Practice type selection
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Phrase Matching"]
    )
    
    # Topic selection
    topics = {
        "Dialogue Practice": ["Daily Conversation", "Shopping", "Restaurant", "Travel", "School/Work"],
        "Phrase Matching": ["Announcements", "Instructions", "Weather Reports", "News Updates"]
    }
    
    topic = st.selectbox(
        "Select Topic",
        topics[practice_type]
    )
    
    # Generate new question button
    if st.button("Generate New Question"):
        section_num = 2 if practice_type == "Dialogue Practice" else 3
        new_question = st.session_state.question_generator.generate_similar_question(
            section_num, topic
        )
        st.session_state.current_question = new_question
        st.session_state.current_practice_type = practice_type
        st.session_state.current_topic = topic
        st.session_state.feedback = None
        
        # Save the generated question
        save_question(new_question, practice_type, topic)
        st.session_state.current_audio = None
    
    if st.session_state.current_question:
        st.subheader("Practice Scenario")
        
        # Display question components
        if practice_type == "Dialogue Practice":
            st.write("**Introduction:**")
            st.write(st.session_state.current_question['Introduction'])
            st.write("**Conversation:**")
            st.write(st.session_state.current_question['Conversation'])
        else:
            st.write("**Situation:**")
            st.write(st.session_state.current_question['Situation'])
        
        st.write("**Question:**")
        st.write(st.session_state.current_question['Question'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display options
            options = st.session_state.current_question['Options']
            
            # If we have feedback, show which answers were correct/incorrect
            if st.session_state.feedback:
                correct = st.session_state.feedback.get('correct', False)
                correct_answer = st.session_state.feedback.get('correct_answer', 1) - 1
                selected_index = st.session_state.selected_answer - 1 if hasattr(st.session_state, 'selected_answer') else -1
                
                st.write("\n**Your Answer:**")
                for i, option in enumerate(options):
                    if i == correct_answer and i == selected_index:
                        st.success(f"{i+1}. {option} ✓ (Correct!)")
                    elif i == correct_answer:
                        st.success(f"{i+1}. {option} ✓ (This was the correct answer)")
                    elif i == selected_index:
                        st.error(f"{i+1}. {option} ✗ (Your answer)")
                    else:
                        st.write(f"{i+1}. {option}")
                
                # Show explanation
                st.write("\n**Explanation:**")
                explanation = st.session_state.feedback.get('explanation', 'No feedback available')
                if correct:
                    st.success(explanation)
                else:
                    st.error(explanation)
                
                # Add button to try new question
                if st.button("Try Another Question"):
                    st.session_state.feedback = None
                    st.rerun()
            else:
                # Display options as radio buttons when no feedback yet
                selected = st.radio(
                    "Choose your answer:",
                    options,
                    index=None,
                    format_func=lambda x: f"{options.index(x) + 1}. {x}"
                )
                
                # Submit answer button
                if selected and st.button("Submit Answer"):
                    selected_index = options.index(selected) + 1
                    st.session_state.selected_answer = selected_index
                    st.session_state.feedback = st.session_state.question_generator.get_feedback(
                        st.session_state.current_question,
                        selected_index
                    )
                    st.rerun()
        
        with col2:
            st.subheader("Audio")
            if st.session_state.current_audio:
                # Display audio player
                st.audio(st.session_state.current_audio)
            elif st.session_state.current_question:
                # Show generate audio button
                if st.button("Generate Audio"):
                    with st.spinner("Generating audio..."):
                        try:
                            # Clear any previous audio
                            if st.session_state.current_audio and os.path.exists(st.session_state.current_audio):
                                try:
                                    os.unlink(st.session_state.current_audio)
                                except Exception:
                                    pass
                            st.session_state.current_audio = None
                            
                            # Generate new audio
                            audio_file = st.session_state.audio_generator.generate_audio(
                                st.session_state.current_question
                            )
                            
                            # Verify the audio file exists
                            if not os.path.exists(audio_file):
                                raise Exception("Audio file was not created")
                                
                            st.session_state.current_audio = audio_file
                            
                            # Update stored question with audio file
                            save_question(
                                st.session_state.current_question,
                                st.session_state.current_practice_type,
                                st.session_state.current_topic,
                                audio_file
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating audio: {str(e)}")
                            # Clear the audio state on error
                            st.session_state.current_audio = None
            else:
                st.info("Generate a question to create audio.")
    
    # Button to toggle ASL section
    if st.button("Start ASL Recognition"):
        st.session_state.show_asl = True
    
    # ASL Recognition section
    if st.session_state.show_asl:
        start_asl_recognition()

def start_asl_recognition():
    """Handles ASL image upload and recognition."""
    with st.container():
        st.subheader("ASL Sign Recognition")
        st.write("Upload an image of an ASL hand sign to recognize the letter.")
        
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
        
        # Add a button to close the ASL section if needed
        if st.button("Close ASL Recognition"):
            st.session_state.show_asl = False
            st.session_state.predicted_letter = ""
            st.rerun()

def main():
    st.set_page_config(
        page_title="Language Learning Assistant",
        page_icon="🌏",
        layout="wide"
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    options = ["Home", "ASL Recognition", "ASL Recognition with ML", "JLPT Listening Practice", "YouTube Transcriber"]
    selected_option = st.sidebar.selectbox("Choose an option:", options)
    st.session_state["selected_option"] = selected_option

    if selected_option == "Home":
        home.main()
    elif selected_option == "ASL Recognition":
        start_asl_recognition() # Replace with your ASL Recognition function
    elif selected_option == "ASL Recognition with ML":
        #start_asl_recognition_ml() # Replace with your ASL Recognition with ML function
        st.write("ASL Recognition with ML content here")
    elif selected_option == "JLPT Listening Practice":
        render_interactive_stage() # Replace with your JLPT Listening Practice function
    elif selected_option == "YouTube Transcriber":
        home.render_youtube_transcriber()

if __name__ == "__main__":
    main()
