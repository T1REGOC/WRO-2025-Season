import RPi.GPIO as GPIO # for GPIO control
import time # for delays
import cv2  # for computer vision
import numpy as np # for image processing
import os # to check if the model file exists
from picamera2 import Picamera2 #picamera2 import for computer vision
import tflite_runtime.interpreter as tflite  # tflite import

GPIO.setmode(GPIO.BOARD) # The pin numbers are not GPIO numbers but board numbers!!!!

# Define GPIO pins for speed and steering
s1 = 3
s2 = 5
m1 = 29
m2 = 31
m3 = 36
m4 = 38

GPIO.setup(s1, GPIO.OUT) # speed 1
GPIO.setup(s2, GPIO.OUT) # speed 2
GPIO.setup(m1, GPIO.OUT) # steer 1
GPIO.setup(m2, GPIO.OUT) # steer 2
GPIO.setup(m3, GPIO.OUT) # steer 3
GPIO.setup(m4, GPIO.OUT) # steer 4

model_path = 'WROtest2025new.tflite'

picam2 = Picamera2() # Initialize the Picamera2
config = picam2.create_preview_configuration(main={"size": (640, 480)}) # Create a preview configuration with the desired resolution
picam2.configure(config) # Configure the camera
picam2.start() # Start the camera

# Check if the model file exists
if not os.path.exists(model_path):
    print(f"Model file '{model_path}' not found!")
    exit(1)

interpreter = tflite.Interpreter(model_path=model_path) # Load the TFLite model
interpreter.allocate_tensors() # Allocate tensors for the model
input_details = interpreter.get_input_details() # Get input details of the model
output_details = interpreter.get_output_details() # Get output details of the model

# Define HSV color ranges for pillar detection
HSV_RANGES = {
    'red': [
        ([0, 50, 40], [12, 255, 255]),      
        ([165, 50, 40], [180, 255, 255])    
    ],
    'green': [
        ([25, 30, 30], [95, 255, 255])
    ]
}
# Define colors for display
DISPLAY_COLORS = {'red': (0, 0, 255), 'green': (0, 255, 0)}
# Define the width and height for processing frames
PROCESS_WIDTH = 640
PROCESS_HEIGHT = 480


def initialize(values):
    blue = 0
    orange = 0
    for i in range(5):
        #read left and right sensors and then decide which way to go
        left = values[3] + values[4] # left sensor
        right = values[1] + values[2] # right sensor
        if left < right:
            orange += 1
        else:
            blue += 1
        time.sleep(0.1)
    if orange > blue:
        way = "orange"
    else:
        way = "blue"   
    return way
    

def find_pillar(frame, color):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV color space
        hsv = cv2.GaussianBlur(hsv, (7, 7), 0) # Apply Gaussian blur to reduce noise
        mask = np.zeros(frame.shape[:2], dtype=np.uint8) # Initialize mask for detected color
        for lower, upper in HSV_RANGES[color]: # Iterate through the defined HSV ranges
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, np.array(lower), np.array(upper))) # Create a binary mask for the color
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7,7), np.uint8), iterations=2) # Remove noise from the mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8), iterations=1) # Close small holes in the mask
        mask = cv2.dilate(mask, np.ones((9,9), np.uint8), iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours in the mask
        if not contours:
            return None
        best = max(contours, key=cv2.contourArea) # Find the largest contour
        area = cv2.contourArea(best) # Calculate the area of the largest contour
        if area < 1000:
            return None
        x, y, w, h = cv2.boundingRect(best) # Get the rectangle of the largest contour
        aspect = w / h if h > 0 else 0 # Calculate the aspect ratio of the rectangle
        if aspect < 0.15 or aspect > 2.5:
            return None
        rect = cv2.minAreaRect(best) # Get the minimum area rectangle that can fit the contour
        box = cv2.boxPoints(rect) # Get the four corners of the rectangle
        box = np.int0(box) # Convert the corners to integer coordinates
        return (x, y, x+w, y+h), box

def navigation_logic(values):
    frame_count = 0
    while values[7] < 12 or values[8] < 12: # While the orange_count and blue_count are less than 12

        frame = picam2.capture_array() # Capture a frame from the camera
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # Convert the frame from RGB to BGR color space
        if frame is None:
            print("Can't read the frame.")
            break

        frame_count += 1
        color, conf = classify_color(frame) # Classify the color of the pillar in the frame
        result = find_pillar(frame, color) # Find the pillar in the frame based on the classified color
        display = frame.copy() 

        if result:
            (x1, y1, x2, y2), box = result # Get the coordinates of the bounding box and the box points
            cv2.rectangle(display, (x1, y1), (x2, y2), DISPLAY_COLORS[color], 2) # Draw a rectangle around the detected pillar
            cv2.drawContours(display, [box], 0, (255, 255, 0), 2) # Draw the minimum area rectangle around the contour
            print(f"[Frame {frame_count}] {color.upper()} pillar: Top-Left=({x1}, {y1}), Bottom-Right=({x2}, {y2}), Confidence={conf:.2f}")
            half_width = frame.shape[1] // 2 # Calculate the half width of the frame
            sixth = frame.shape[1] // 6 # Calculate one-sixth of the frame width
            center_x = (x1 + x2) // 2 # Calculate the center x-coordinate of the detected pillar
            if color == 'red':
                if center_x > (sixth*3):
                    #0101
                    GPIO.output(m1, GPIO.LOW)
                    GPIO.output(m2, GPIO.HIGH)
                    GPIO.output(m3, GPIO.LOW)
                    GPIO.output(m4, GPIO.HIGH)
                    if center_x > (sixth*4):
                        #0110
                        GPIO.output(m1, GPIO.LOW)
                        GPIO.output(m2, GPIO.HIGH)
                        GPIO.output(m3, GPIO.HIGH)
                        GPIO.output(m4, GPIO.LOW)
                        if center_x > (sixth*5):
                            #0111
                            GPIO.output(m1, GPIO.LOW)
                            GPIO.output(m2, GPIO.HIGH)
                            GPIO.output(m3, GPIO.HIGH)
                            GPIO.output(m4, GPIO.HIGH)
                    
                elif center_x < half_width:
                            #0111
                            GPIO.output(m1, GPIO.LOW)
                            GPIO.output(m2, GPIO.HIGH)
                            GPIO.output(m3, GPIO.HIGH)
                            GPIO.output(m4, GPIO.HIGH)
            if color == 'green':
                if center_x < (sixth*3):
                    #0001
                    GPIO.output(m1, GPIO.LOW)
                    GPIO.output(m2, GPIO.LOW)
                    GPIO.output(m3, GPIO.LOW)
                    GPIO.output(m4, GPIO.HIGH)
                    if center_x < (sixth*2):
                        #0010
                        GPIO.output(m1, GPIO.LOW)
                        GPIO.output(m2, GPIO.LOW)
                        GPIO.output(m3, GPIO.HIGH)
                        GPIO.output(m4, GPIO.LOW)
                        if center_x < (sixth*1):
                            #0011
                            GPIO.output(m1, GPIO.LOW)
                            GPIO.output(m2, GPIO.LOW)
                            GPIO.output(m3, GPIO.HIGH)
                            GPIO.output(m4, GPIO.HIGH)
                elif center_x > half_width:
                    #0100
                    GPIO.output(m1, GPIO.LOW)
                    GPIO.output(m2, GPIO.HIGH)
                    GPIO.output(m3, GPIO.LOW)
                    GPIO.output(m4, GPIO.LOW)
        display_small = cv2.resize(display, (PROCESS_WIDTH, PROCESS_HEIGHT))
        cv2.imshow('Pillar Detection', display_small)
        
def exit_parking():
    # exit parking logic
    print("exit parking")      

def parking_in():
    # parking in logic
    print("parking in")

def classify_color(frame):
    img = cv2.resize(frame, (128, 128))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img) # Set the input tensor with the preprocessed image
    interpreter.invoke() # Invoke the interpreter to run the model
    pred = interpreter.get_tensor(output_details[0]['index'])[0][0] # Get the output tensor prediction
    return ('green' if pred > 0.5 else 'red'), float(pred) # confidence score of the prediction

def line_up(way, values):
    if way == "blue":
        a = 1
    else:
        a = 3
    delta = 6
    while(delta > 5):
        x1 = values[a] # Sensor 1(front right) or sensor 3(front left)
        x2 = values[a+1] # Sensor 2(back right) or sensor 4(back left)

        delta = abs(x1 - x2) # Delta is the difference between the two sensor values
        if way == "blue": # If the parking is on the right side
            if x1 > x2:
                #0101
                GPIO.output(m1, GPIO.LOW)
                GPIO.output(m2, GPIO.HIGH)
                GPIO.output(m3, GPIO.LOW)
                GPIO.output(m4, GPIO.HIGH)
            else:
                #0001
                GPIO.output(m1, GPIO.LOW)
                GPIO.output(m2, GPIO.LOW)
                GPIO.output(m3, GPIO.LOW)
                GPIO.output(m4, GPIO.HIGH)
        else:
                if x1 > x2: # If parking on the left side:
                    #0001
                    GPIO.output(m1, GPIO.LOW)
                    GPIO.output(m2, GPIO.LOW)
                    GPIO.output(m3, GPIO.LOW)
                    GPIO.output(m4, GPIO.HIGH)
                else:
                    #0101
                    GPIO.output(m1, GPIO.LOW)
                    GPIO.output(m2, GPIO.HIGH)
                    GPIO.output(m3, GPIO.LOW)
                    GPIO.output(m4, GPIO.HIGH)


def main(values):
    way = initialize(values) # Determine the way to park based on sensor readings
    exit_parking() # Exit parking logic
    # Set the motor speed to 100%
    GPIO.output(s1, GPIO.HIGH) 
    GPIO.output(s2, GPIO.HIGH)
    navigation_logic(values)
    # Set the motor speed to 50% for lining up
    GPIO.output(s1, GPIO.HIGH)
    GPIO.output(s2, GPIO.LOW)
    line_up(way, values)
    # Set the motor speed to 25% for parking
    GPIO.output(s1, GPIO.LOW)
    GPIO.output(s2, GPIO.HIGH)
    parking_in() # Parking in logic
    cv2.destroyAllWindows() # Close all OpenCV windows
    GPIO.cleanup() # Clean up GPIO settings

