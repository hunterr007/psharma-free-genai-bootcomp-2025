from flask import Flask, request, jsonify
from asl_recognition import ASLRecognizer
import cv2
import numpy as np
import boto3
import json
from botocore.exceptions import NoRegionError
import logging
from flask_cors import CORS  # Add CORS support

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS
recognizer = ASLRecognizer()  # Initialize the ASL recognizer

# Initialize Bedrock client
try:
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"  # Replace with your AWS region
    )
except NoRegionError as e:
    print(f"Error configuring Bedrock client: {e}")
    bedrock_client = None
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    bedrock_client = None

@app.route("/predict_asl", methods=["POST"])
def predict_asl():
    try:
        logger.info("Received request for ASL prediction")
        
        if "image" not in request.files:
            logger.error("No image file in request")
            return jsonify({"error": "No image file provided"}), 400
            
        image_file = request.files["image"]
        if not image_file.filename:
            logger.error("Empty filename in request")
            return jsonify({"error": "Empty filename"}), 400
        
        # Read the image file
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            logger.error("Could not decode image")
            return jsonify({"error": "Could not decode image"}), 400

        logger.info(f"Successfully decoded image, shape: {image.shape}")

        # Make prediction
        predicted_letter = recognizer.predict(image)
        logger.info(f"Prediction result: {predicted_letter}")

        if predicted_letter:
            return jsonify({"letter": predicted_letter})
        else:
            logger.warning("No hand detected in image")
            return jsonify({"error": "Could not detect hand in image"}), 400

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/bedrock_query", methods=["POST"])
def bedrock_query():
    if bedrock_client is None:
        return jsonify(
            {
                "error": "Bedrock client is not initialized. Check your AWS configuration."
            }
        ), 500

    try:
        data = request.get_json()
        user_question = data.get("question")

        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        model_id = "amazon.titan-text-express-v1"  # Replace with your desired model ID
        body = json.dumps(
            {
                "inputText": user_question,
                "textGenerationConfig": {
                    "maxTokenCount": 200,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9,
                },
            }
        )

        try:
            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=body,
            )
            response_body = json.loads(response["body"].read().decode("utf-8"))
            bedrock_response = response_body["results"][0]["outputText"]
        except Exception as e:
            return jsonify({"error": f"Bedrock invocation error: {e}"}), 500

        return jsonify({"response": bedrock_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Run the Flask app 