import serial # Import the serial library
import RPi.GPIO as GPIO # Import the GPIO library

# GPIO pin numbers for the Raspberry Pi
# These pins are used for controlling the motors and reading sensors
s1 = 3
s2 = 5
m1 = 29
m2 = 31
m3 = 36
m4 = 38
GPIO.setmode(GPIO.BOARD) # Board mode for GPIO pins

GPIO.setup(s1, GPIO.OUT) # speed 1
GPIO.setup(s2, GPIO.OUT) # speed 2
GPIO.setup(m1, GPIO.OUT) # steer 1
GPIO.setup(m2, GPIO.OUT) # steer 2
GPIO.setup(m3, GPIO.OUT) # steer 3
GPIO.setup(m4, GPIO.OUT) # steer 4

def serial_reader(values):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Open serial port
    a = 0 # Counter for detection
    o = 0 # Orange counter
    b = 0 # Blue counter

    try:
        while True:

            line = ser.readline().decode('utf-8').strip() # Read a line from the serial port
            if line:
                try:
                    data = [int(x) for x in line.split(',')] # Split the line into integers
                    if len(data) == 7:
                        values[:7] = data  # Update the shared list
                        if values[6] == 'b':
                            b += 1
                        if values[6] == 'o':
                            o += 1
                        values[7] = b # Blue counter in shared list
                        values[8] = o # Orange counter in shared list
                        print(f"Ultrasonic sensor readings: {values}")
                        if values[0] < 10 or values[3] < 10 or values[4] < 10: 
                            #0111
                            GPIO.output(m1, GPIO.LOW)
                            GPIO.output(m2, GPIO.HIGH)
                            GPIO.output(m3, GPIO.HIGH)
                            GPIO.output(m4, GPIO.HIGH)
                        if values[0] < 10 or values[1] < 10 or values[2] < 10:
                            #0011
                            GPIO.output(m1, GPIO.LOW)
                            GPIO.output(m2, GPIO.LOW)
                            GPIO.output(m3, GPIO.HIGH)
                            GPIO.output(m4, GPIO.HIGH)
                        if values[6] == 'b' or values[6] == 'o': # Blue or Orange detected
                            a = a + 1
                        if a >= 12: # If 12 detections of blue or orange
                            detection(values)
                except ValueError:
                    print(f"Received malformed data: {line}")
    except KeyboardInterrupt:
        print("exiting")
 

def detection(values):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Open serial port

    try:
        while True:

            line = ser.readline().decode('utf-8').strip() # Read a line from the serial port
            if line:
                try:
                    data = [int(x) for x in line.split(',')] # Split the line into integers
                    if len(data) == 7:
                        values[:7] = data  # Update the shared list
                        print(f"Ultrasonic sensor readings: {values}")
                except ValueError:
                    print(f"Received malformed data: {line}")
    except KeyboardInterrupt:
        print("exiting")
    finally:
        ser.close() # Ensure the serial port is closed when done