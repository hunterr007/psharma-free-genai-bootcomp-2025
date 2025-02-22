import tensorflow as tf
import numpy as np

# Create a simple model for ASL recognition
def create_asl_model():
    # Input shape: 63 features (21 landmarks * 3 coordinates)
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(63,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(26, activation='softmax')  # 26 classes for A-Z
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Create and save the model
model = create_asl_model()

# Convert the model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('backend/models/asl_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model created and saved as asl_model.tflite")
