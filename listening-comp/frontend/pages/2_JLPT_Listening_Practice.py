import streamlit as st
import sys
import os
import json
from datetime import datetime

def load_stored_questions():
    """Load previously stored questions from JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../static/stored_questions.json"
    )
    if os.path.exists(questions_file):
        with open(questions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_question(question, practice_type, topic):
    """Save a generated question to JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../static/stored_questions.json"
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
    }
    
    # Save to dictionary
    stored_questions[question_id] = question_data
    
    # Write back to file
    os.makedirs(os.path.dirname(questions_file), exist_ok=True)
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(stored_questions, f, ensure_ascii=False, indent=2)
    
    return question_id

def render_interactive_stage():
    st.title("JLPT Listening Practice")
    
    # Initialize session states if they don't exist
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
        
    # Load stored questions
    stored_questions = load_stored_questions()
    
    # Create two columns for the main layout
    col1, col2 = st.columns([2, 1])
    
    # Main content area (left column)
    with col1:
        if st.session_state.current_question:
            st.header(f"Current Practice: {st.session_state.current_topic}")
            
            # Display current question
            st.subheader("Question:")
            st.write(st.session_state.current_question)
            
            # Clear button
            if st.button("Clear Current Question"):
                st.session_state.current_question = None
                st.session_state.current_topic = None
                st.rerun()
        else:
            st.info("Click 'Generate New Question' to start practicing!")
        
        # Practice History
        st.header("Practice History")
        if stored_questions:
            for qid, qdata in stored_questions.items():
                with st.expander(f"{qdata['practice_type']} - {qdata['topic']}"):
                    st.write(qdata['question'])
        else:
            st.info("No practice history yet. Generate some questions to get started!")
    
    # Settings panel (right column)
    with col2:
        st.header("Practice Settings")
        
        # Practice type selection
        practice_type = st.selectbox(
            "Select Practice Type",
            ["Vocabulary", "Grammar", "Conversation"]
        )
        
        # Topic selection based on practice type
        topics = {
            "Vocabulary": ["Daily Life", "Work", "Study", "Travel"],
            "Grammar": ["Particles", "Verb Forms", "Adjectives", "Sentence Patterns"],
            "Conversation": ["Greetings", "Shopping", "Directions", "Restaurant"]
        }
        
        topic = st.selectbox(
            "Select Topic",
            topics[practice_type]
        )
        
        # Sample questions for each combination
        sample_questions = {
            "Vocabulary": {
                "Daily Life": "What is the Japanese word for 'breakfast'? (朝ご飯/あさごはん)",
                "Work": "How do you say 'meeting' in Japanese? (会議/かいぎ)",
                "Study": "What is the word for 'textbook'? (教科書/きょうかしょ)",
                "Travel": "How do you say 'ticket' in Japanese? (切符/きっぷ)"
            },
            "Grammar": {
                "Particles": "Which particle should be used to mark the subject? (は vs が)",
                "Verb Forms": "Convert the verb 食べる to past tense (食べました)",
                "Adjectives": "How do you make the adjective 高い negative? (高くない)",
                "Sentence Patterns": "Complete the pattern: ～てもいいです (Permission)"
            },
            "Conversation": {
                "Greetings": "What is the appropriate evening greeting? (こんばんは)",
                "Shopping": "How do you ask for the price? (いくらですか)",
                "Directions": "How do you ask where the station is? (駅はどこですか)",
                "Restaurant": "How do you order food politely? (〜をお願いします)"
            }
        }
        
        # Generate new question button
        if st.button("Generate New Question", type="primary"):
            question = sample_questions[practice_type][topic]
            save_question(question, practice_type, topic)
            st.session_state.current_question = question
            st.session_state.current_topic = topic
            st.rerun()

if __name__ == "__main__":
    render_interactive_stage()
