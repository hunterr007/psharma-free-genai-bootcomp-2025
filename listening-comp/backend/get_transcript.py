import sys  # Import the sys module
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict
import os


class YouTubeTranscriptDownloader:
    def __init__(self, languages: List[str] = ["ja", "en"]):
        self.languages = languages

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        if "v=" in url:
            return url.split("v=")[1][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        return None

    def get_transcript(self, video_id: str) -> Optional[List[Dict]]:
        """
        Download YouTube Transcript
        
        Args:
            video_id (str): YouTube video ID or URL
            
        Returns:
            Optional[List[Dict]]: Transcript if successful, None otherwise
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        if not video_id:
            print("Invalid video ID or URL")
            return None

        print(f"Downloading transcript for video ID: {video_id}")
        
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=self.languages)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            filename (str): Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Ensure the directory exists
        transcript_dir = "backend/data/transcripts"
        os.makedirs(transcript_dir, exist_ok=True)
        
        filename = os.path.join(transcript_dir, f"{filename}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False

    def process_audio_file(self, audio_file) -> str:
        """
        Process uploaded audio file and return transcript
        
        Args:
            audio_file: Flask file object
            
        Returns:
            str: Transcript text
        """
        # TODO: Implement actual audio processing
        # For now, return a placeholder
        return "Audio file processed successfully. Transcript will be implemented soon."

def main(video_url):
    # Initialize downloader
    downloader = YouTubeTranscriptDownloader()
    
    # Get transcript
    transcript = downloader.get_transcript(video_url)
    # downloader.save_transcript(transcript, video_url)
    if transcript:
        # Save transcript
        video_id = downloader.extract_video_id(video_url)
        if downloader.save_transcript(transcript, video_id):
            print(f"Transcript saved successfully to backend/data/transcripts/{video_id}.txt")
        else:
            print("Failed to save transcript")
        
    else:
        print("Failed to get transcript")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        main(video_url)
    else:
        print("Please provide a YouTube URL as a command-line argument.")