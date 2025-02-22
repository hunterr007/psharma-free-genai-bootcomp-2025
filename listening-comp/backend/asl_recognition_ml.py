import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import logging
import os

class ASLRecognitionML:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize MediaPipe
        try:
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            self.hands = self.mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.3,
                min_tracking_confidence=0.3
            )
            self.logger.info("MediaPipe initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing MediaPipe: {e}")
            raise
        
        # Initialize the model
        try:
            # Use ResNet18 as base model with pretrained weights
            self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            
            # Modify the final layer for ASL classification (24 classes)
            num_features = self.model.fc.in_features
            self.model.fc = torch.nn.Sequential(
                torch.nn.Linear(num_features, 512),
                torch.nn.BatchNorm1d(512),  # Add batch normalization
                torch.nn.ReLU(),
                torch.nn.Dropout(0.3),  # Reduced dropout for better stability
                torch.nn.Linear(512, 24)  # 24 ASL letters (excluding J and Z)
            )
            
            # Move model to CPU and optimize for inference
            self.device = torch.device('cpu')
            self.model = self.model.to(self.device)
            self.model.eval()
            
            # Enable inference optimizations
            torch.set_grad_enabled(False)
            
            # Setup image transforms with efficient operations
            self.transform = transforms.Compose([
                transforms.Resize(256),  # Resize to slightly larger
                transforms.CenterCrop(224),  # Then center crop
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            
            self.logger.info(f"Model initialized successfully on {self.device}")
        except Exception as e:
            self.logger.error(f"Error initializing model: {e}")
            raise
        
        # ASL alphabet labels (excluding J and Z which require motion)
        self.labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 
                      'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    
    def preprocess_image(self, image):
        """Convert image to RGB and normalize"""
        try:
            if isinstance(image, np.ndarray):
                # Convert OpenCV BGR to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
            elif not isinstance(image, Image.Image):
                raise ValueError("Image must be either a numpy array or PIL Image")
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Efficient resizing with antialiasing
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
        except Exception as e:
            self.logger.error(f"Error in preprocess_image: {e}")
            raise
    
    def predict_sign(self, image):
        """Predict the ASL sign from an image"""
        self.logger.info(f"predict_sign called with image: {type(image)}, {image.size if hasattr(image, 'size') else image.shape}")
        try:
            # Preprocess image
            image = self.preprocess_image(image)
            self.logger.info("Image preprocessed successfully")
            
            try:
                # Convert to tensor and normalize
                image_tensor = self.transform(image).unsqueeze(0)
                
                # Ensure we're using CPU tensors
                image_tensor = image_tensor.to(self.device)
                
                # Get prediction efficiently
                with torch.inference_mode():  # More efficient than no_grad
                    outputs = self.model(image_tensor)
                    probabilities = torch.nn.functional.softmax(outputs, dim=1)
                    confidence, predicted_class = torch.max(probabilities, 1)
                
                # Get the predicted letter and confidence
                predicted_letter = self.labels[predicted_class.item()]
                confidence_value = float(confidence.item())  # Convert to Python float
                
                self.logger.info(f"Predicted letter: {predicted_letter} with confidence: {confidence_value:.4f}")
                
                return {
                    "letter": predicted_letter,
                    "confidence": confidence_value
                }
            except Exception as e:
                self.logger.error(f"Error during model inference: {e}")
                return {"error": f"Error during prediction: {str(e)}"}
            
        except Exception as e:
            self.logger.error(f"Error in prediction: {e}")
            return {"error": str(e)}
    
    def process_frame(self, frame):
        """Process a video frame and return the annotated frame with prediction"""
        try:
            # Get prediction
            prediction = self.predict_sign(frame)
            
            return frame, prediction
            
        except Exception as e:
            self.logger.error(f"Error processing frame: {e}")
            return frame, {"error": str(e)}