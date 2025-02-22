from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import process_chat_input
from get_transcript import YouTubeTranscriptDownloader
from question_generator import generate_questions

app = Flask(__name__)
CORS(app)

# Initialize transcript downloader
transcript_downloader = YouTubeTranscriptDownloader()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = process_chat_input(data.get('message', ''))
    return jsonify({"response": response})

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    audio_file = request.files['file']
    transcript = transcript_downloader.process_audio_file(audio_file)
    return jsonify({"transcript": transcript})

@app.route('/generate-questions', methods=['POST'])
def create_questions():
    data = request.json
    text = data.get('text', '')
    questions = generate_questions(text)
    return jsonify({"questions": questions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
