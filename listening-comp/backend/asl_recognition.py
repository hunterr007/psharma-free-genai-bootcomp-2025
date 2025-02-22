import cv2
import mediapipe as mp
import numpy as np
import logging
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ASLRecognizer:
    def __init__(self):
        """
        Initializes the ASL recognizer using MediaPipe hands and rule-based recognition
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def calculate_finger_angles(self, landmarks):
        """Calculate angles between finger joints"""
        # Define finger joint connections
        fingers = {
            'thumb': [1, 2, 3, 4],
            'index': [5, 6, 7, 8],
            'middle': [9, 10, 11, 12],
            'ring': [13, 14, 15, 16],
            'pinky': [17, 18, 19, 20]
        }
        
        angles = {}
        for finger, points in fingers.items():
            # Calculate two angles for each finger
            # First angle: between first and second joint
            # Second angle: between second and third joint
            angles[finger] = []
            
            for i in range(len(points)-2):
                p1 = np.array([landmarks[points[i]].x, landmarks[points[i]].y])
                p2 = np.array([landmarks[points[i+1]].x, landmarks[points[i+1]].y])
                p3 = np.array([landmarks[points[i+2]].x, landmarks[points[i+2]].y])
                
                # Calculate vectors
                v1 = p1 - p2
                v2 = p3 - p2
                
                # Calculate angle
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
                angles[finger].append(math.degrees(angle))
        
        return angles

    def is_finger_extended(self, angles, finger):
        """Check if a finger is extended based on its angles"""
        # More lenient threshold for considering a finger extended
        EXTENSION_THRESHOLD = 130  # degrees (was 160)
        
        # Log the angles for debugging
        logger.info(f"{finger} finger angles: {angles[finger]}")
        
        # A finger is considered extended if its average angle is above threshold
        avg_angle = sum(angles[finger]) / len(angles[finger])
        is_extended = avg_angle > EXTENSION_THRESHOLD
        logger.info(f"{finger} finger extended: {is_extended} (avg angle: {avg_angle:.2f})")
        return is_extended

    def is_finger_closed(self, angles, finger):
        """Check if a finger is closed (bent towards palm)"""
        # More lenient threshold for considering a finger closed
        CLOSED_THRESHOLD = 120  # degrees (was 90)
        
        # Log the angles for debugging
        logger.info(f"{finger} finger angles: {angles[finger]}")
        
        # A finger is considered closed if its average angle is below threshold
        avg_angle = sum(angles[finger]) / len(angles[finger])
        is_closed = avg_angle < CLOSED_THRESHOLD
        logger.info(f"{finger} finger closed: {is_closed} (avg angle: {avg_angle:.2f})")
        return is_closed

    def predict(self, image):
        """
        Predicts the ASL letter from an image using rule-based recognition
        """
        try:
            # Convert the color space from BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image with MediaPipe Hands
            results = self.hands.process(image_rgb)
            
            if not results.multi_hand_landmarks:
                logger.warning("No hand landmarks detected")
                return None
            
            # Get the first detected hand landmarks
            landmarks = results.multi_hand_landmarks[0].landmark
            
            # Calculate angles for all fingers
            angles = self.calculate_finger_angles(landmarks)
            logger.info("Calculated finger angles:")
            for finger, angle_list in angles.items():
                logger.info(f"{finger}: {angle_list}")
            
            # Check for A (closed fist)
            closed_fingers = all(self.is_finger_closed(angles, finger) 
                               for finger in ['index', 'middle', 'ring', 'pinky'])
            if closed_fingers:
                logger.info("Detected 'A' sign - closed fist")
                return 'A'
            
            # Check for B (all fingers extended)
            extended_fingers = all(self.is_finger_extended(angles, finger) 
                                 for finger in ['index', 'middle', 'ring', 'pinky'])
            if extended_fingers:
                logger.info("Detected 'B' sign - all fingers extended")
                return 'B'
            
            # Check for L (index extended, others closed)
            if (self.is_finger_extended(angles, 'index') and
                all(self.is_finger_closed(angles, finger) 
                    for finger in ['middle', 'ring', 'pinky'])):
                logger.info("Detected 'L' sign - index extended")
                return 'L'
            
            # Check for Y (pinky extended, others closed)
            if (self.is_finger_extended(angles, 'pinky') and
                all(self.is_finger_closed(angles, finger) 
                    for finger in ['index', 'middle', 'ring'])):
                logger.info("Detected 'Y' sign - pinky extended")
                return 'Y'
            
            # Check for I (pinky extended only)
            if (self.is_finger_extended(angles, 'pinky') and
                all(self.is_finger_closed(angles, finger) 
                    for finger in ['index', 'middle', 'ring'])):
                logger.info("Detected 'I' sign - pinky only")
                return 'I'
            
            # Check for D (index extended only)
            if (self.is_finger_extended(angles, 'index') and
                all(self.is_finger_closed(angles, finger) 
                    for finger in ['middle', 'ring', 'pinky'])):
                logger.info("Detected 'D' sign - index only")
                return 'D'
            
            # Check for F (index and middle fingers close together)
            middle_tip = landmarks[12]
            index_tip = landmarks[8]
            distance = math.dist([middle_tip.x, middle_tip.y], [index_tip.x, index_tip.y])
            logger.info(f"Distance between index and middle fingers: {distance}")
            if distance < 0.1:  # Increased threshold
                logger.info("Detected 'F' sign - index and middle together")
                return 'F'
            
            # Check for U (index and middle extended)
            if (self.is_finger_extended(angles, 'index') and
                self.is_finger_extended(angles, 'middle') and
                all(self.is_finger_closed(angles, finger) 
                    for finger in ['ring', 'pinky'])):
                logger.info("Detected 'U' sign - index and middle extended")
                return 'U'
            
            logger.info("No matching ASL letter pattern found")
            return '?'
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}", exc_info=True)
            return None

    def recognize_from_camera(self):
        """
        Opens the camera and continuously recognizes ASL letters.
        """
        cap = cv2.VideoCapture(0)  # Use 0 for the default camera

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            predicted_letter = self.predict(frame)

            if predicted_letter:
                cv2.putText(frame, f"Predicted: {predicted_letter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('ASL Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    recognizer = ASLRecognizer()
    recognizer.recognize_from_camera() 