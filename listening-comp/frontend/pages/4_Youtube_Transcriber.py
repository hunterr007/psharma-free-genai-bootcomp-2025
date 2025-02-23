import streamlit as st
import subprocess  # Import the subprocess module

def render_youtube_transcriber():
    st.header("YouTube Transcriber")
    youtube_url = st.text_input("Provide YouTube video URL:")
    if st.button("Transcribe"):
        if youtube_url:
            try:
                # Call the backend script to download the transcript
                subprocess.run(["python", "backend/get_transcript.py", youtube_url], check=True, capture_output=True, text=True)
                
                # Read the transcript from the file
                video_id = youtube_url.split("v=")[1][:11] if "v=" in youtube_url else youtube_url.split("youtu.be/")[1][:11] if "youtu.be/" in youtube_url else None
                if video_id:
                    transcript_file = f"backend/data/transcripts/{video_id}.txt"
                    try:
                        with open(transcript_file, "r", encoding="utf-8") as f:
                            transcript = f.read()
                        st.success("Transcription generated successfully!")
                        st.text_area("Transcription:", transcript, height=300)
                    except FileNotFoundError:
                        st.error("Transcription file not found. There might have been an error during transcription.")
                else:
                    st.error("Could not extract video ID from URL.")
            except subprocess.CalledProcessError as e:
                st.error(f"An error occurred: {e.stderr}")
        else:
            st.warning("Please enter a YouTube URL.")

def main():
    st.set_page_config(
        page_title="YouTube Transcriber",
        page_icon="🎬",
        layout="wide"
    )
    render_youtube_transcriber()

if __name__ == "__main__":
    main()
