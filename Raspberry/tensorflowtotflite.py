import tensorflow as tf # Import TensorFlow
# Load the Keras model and convert it to TensorFlow Lite format
model = tf.keras.models.load_model('WRO2025new.keras') # Load the Keras model from file
converter = tf.lite.TFLiteConverter.from_keras_model(model) # Create a TFLiteConverter object from the Keras model
tflite_model = converter.convert() # Convert the Keras model to TensorFlow Lite format
with open('WRO2025new.tflite', 'wb') as f: # Open a file to write the TFLite model
    f.write(tflite_model) # Write the converted model to the file