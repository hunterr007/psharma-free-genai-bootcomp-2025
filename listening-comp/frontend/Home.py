import streamlit as st

def main():
    st.set_page_config(
        page_title="Language Learning Assistant",
        page_icon="🌏",
        layout="wide"
    )
    
    st.title("Welcome to Language Learning Assistant! 👋")
    st.markdown("""
    ### Choose Your Learning Path
    
    This application offers two main features to help you in your language learning journey:
    
    #### 1. ASL (American Sign Language) Recognition - Rule Based 🤟
    - Upload images of ASL hand signs
    - Get real-time recognition of letters with Mediapiple and OpenCV
    - Practice and improve your signing skills
                
    #### 2. ASL (American Sign Language) Recognition - Machine Learning 
    - Upload images of ASL hand signs
    - Get real-time recognition of letters
    - Practice and improve your signing skills
    
    #### 3. JLPT Listening Practice 🎧
    - Practice with various JLPT-style listening exercises
    - Choose from different topics and difficulty levels
    - Track your progress over time

    """)

if __name__ == "__main__":
    main()
