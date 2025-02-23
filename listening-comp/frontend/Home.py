import streamlit as st

def main():
    st.set_page_config(
        page_title="Language Learning Assistant",
        page_icon="🌏",
        layout="wide"
    )
    
    st.title("Welcome to Prashant's Language Learning Assistant! 👋")
    st.markdown("""
    ### Choose Your Learning Path
    
    This application offers several features to help you in your language learning journey:
    
    - **1) ASL (American Sign Language) Recognition**: Upload images of ASL hand signs and get real-time recognition using Rule Based Model.
                
    - **2) ASL (American Sign Language)  Recognition with Machine Learning Model**: Use a machine learning model for ASL sign recognition.
                
    - **3) JLPT Listening Practice**: Practice with JLPT-style listening exercises.
                
    - **4) YouTube Transcriber**: Transcribe YouTube videos and get the text.
    """)

if __name__ == "__main__":
    main()
