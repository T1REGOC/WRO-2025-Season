import os # Import necessary libraries
import numpy as np # Import necessary libraries
import tensorflow as tf # Import necessary libraries
from tensorflow.keras.models import Sequential # Import necessary libraries
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout # Import necessary libraries
from tensorflow.keras.preprocessing.image import ImageDataGenerator # For data augmentation
from sklearn.model_selection import train_test_split # For splitting the dataset into training and testing sets
from sklearn.utils import shuffle # For shuffling the dataset
import matplotlib.pyplot as plt # For plotting

tf.random.set_seed(42) # Set random seed for reproducibility

dataset_dir = r'C:\Users\Vedran\Desktop\datasetnew\dataset' # Path to the dataset directory
red_dir = os.path.join(dataset_dir, 'red') # Path to the red images directory
green_dir = os.path.join(dataset_dir, 'green') # Path to the green images directory

IMG_SIZE = (128, 128) # Size to which images will be resized
BATCH_SIZE = 32 # Batch size for training
EPOCHS = 30 # Number of epochs for training

def load_dataset():
    images = [] # List to hold image data
    labels = [] # List to hold labels (0 for red, 1 for green)
    for img_file in os.listdir(red_dir): # Iterate through red images
        img_path = os.path.join(red_dir, img_file) # Get full path of the image
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=IMG_SIZE) # Load the image and resize it
        img_array = tf.keras.preprocessing.image.img_to_array(img) # Convert the image to an array
        images.append(img_array) # Append the image array to the list
        labels.append(0) # Append label 0 for red images
    for img_file in os.listdir(green_dir): # Iterate through green images
        img_path = os.path.join(green_dir, img_file) # Get full path of the image
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=IMG_SIZE) # Load the image and resize it
        img_array = tf.keras.preprocessing.image.img_to_array(img) # Convert the image to an array
        images.append(img_array) # Append the image array to the list
        labels.append(1) # Append label 1 for green images
    return np.array(images), np.array(labels) # Convert lists to numpy arrays

X, y = load_dataset() # Load the dataset
X, y = shuffle(X, y, random_state=42) # Shuffle the dataset to ensure randomness
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Split the dataset into training and testing sets
train_datagen = ImageDataGenerator(
    rescale=1./255, # Rescale pixel values to [0, 1]
    rotation_range=20, # Randomly rotate images in the range (degrees, 0 to 180)
    width_shift_range=0.2, # Randomly shift images horizontally (fraction of total width)
    height_shift_range=0.2, # Randomly shift images vertically (fraction of total height)
    shear_range=0.2, # Shear angle in counter-clockwise direction in degrees
    zoom_range=0.2, # Randomly zoom into images
    horizontal_flip=True, # Randomly flip images horizontally
    fill_mode='nearest' # Fill in new pixels after a transformation
    )

test_datagen = ImageDataGenerator(rescale=1./255) # Rescale pixel values to [0, 1] for test data

train_generator = train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE) # Create a generator for training data
test_generator = test_datagen.flow(X_test, y_test, batch_size=BATCH_SIZE) # Create a generator for testing data

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)), # First convolutional layer
    MaxPooling2D((2, 2)), # Max pooling layer to reduce spatial dimensions
    Conv2D(64, (3, 3), activation='relu'), # Second convolutional layer
    MaxPooling2D((2, 2)), # Max pooling layer to reduce spatial dimensions
    Conv2D(128, (3, 3), activation='relu'), # Third convolutional layer
    MaxPooling2D((2, 2)), # Max pooling layer to reduce spatial dimensions
    Flatten(), # Flatten the output from the convolutional layers
    Dense(128, activation='relu'), # Fully connected layer with 128 neurons
    Dropout(0.5), # Dropout layer to prevent overfitting
    Dense(1, activation='sigmoid') # Output layer with sigmoid activation for binary classification
])

model.compile(optimizer='adam', # Adam optimizer for training
              loss='binary_crossentropy', # Binary crossentropy loss function for binary classification
              metrics=['accuracy']) # Compile the model with the specified optimizer, loss function, and metrics

history = model.fit( # Train the model
    train_generator, # Training data generator
    steps_per_epoch=len(X_train) // BATCH_SIZE, # Number of steps per epoch
    epochs=EPOCHS, # Number of epochs to train the model
    validation_data=test_generator, # Validation data generator
    validation_steps=len(X_test) // BATCH_SIZE) # Number of validation steps

test_loss, test_acc = model.evaluate(test_generator) # Evaluate the model on the test data
print(f'\nTest accuracy: {test_acc:.4f}')

model.save('WRO2025new.keras') # Save the trained model to a file
print("Model saved")

plt.figure(figsize=(12, 4)) # Create a figure for plotting training and validation accuracy and loss
plt.subplot(1, 2, 1) # Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy') # Plot training accuracy
plt.plot(history.history['val_accuracy'], label='Validation Accuracy') # Plot validation accuracy
plt.title('Training and Validation Accuracy') # Set title for the accuracy plot
plt.legend() # Add legend to the accuracy plot

plt.subplot(1, 2, 2) # Plot training and validation loss
plt.plot(history.history['loss'], label='Training Loss') # Plot training loss
plt.plot(history.history['val_loss'], label='Validation Loss') # Plot validation loss
plt.title('Training and Validation Loss') # Set title for the loss plot
plt.legend() # Add legend to the loss plot
plt.show() # Show the plots for training and validation accuracy and loss