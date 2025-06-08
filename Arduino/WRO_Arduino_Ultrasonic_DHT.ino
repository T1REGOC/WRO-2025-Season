#include <DHT11.h>  // Include the DHT sensor library to read temperature and humidity data.
#include <NewPing.h>  // Include the NewPing library to control ultrasonic sensors.
#include <Wire.h>
#include <Servo.h>

#define APDS9960_ADDR 0x39 // I2C address for the APDS9960 sensor.
#define ENABLE_REG 0x80 // Register address for enabling the APDS9960 sensor.
#define ATIME_REG 0x81 // Register address for the APDS9960 sensor's integration time.
#define CONTROL_REG 0x8F // Register address for controlling the APDS9960 sensors gain and other settings.
#define CDATAL_REG 0x94 // Register address for reading color data from the APDS9960 sensor.
#define trigPin 2  // The trigger pin for all the ultrasonic sensors (sending the pulse).
#define echoPin1 3  // The echo pin for the first ultrasonic sensor.
#define echoPin2 5  // The echo pin for the second ultrasonic sensor.
#define echoPin3 6  // The echo pin for the third ultrasonic sensor.
#define echoPin4 7  // The echo pin for the fourth ultrasonic sensor.
#define echoPin5 8  // The echo pin for the fifth ultrasonic sensor.
#define echoPin6 9  // The echo pin for the sixth ultrasonic sensor.
#define dhtPin 4  // The data pin for the DHT22 sensor.
#define maximum 400  // Maximum range of the ultrasonic sensors in cm.

DHT11 dht11(4); // Initialize the DHT11 sensor object on pin 4.

Servo stmotor;
//steering motors for detection
#define m1 12
#define m2 A0
#define m3 A1
#define m4 A2

//speed motors
#define s1 10
#define s2 11

// power pins for speed
#define p A3

NewPing sonar1(trigPin, echoPin1, maximum);  // Initialize the first ultrasonic sensor.
NewPing sonar2(trigPin, echoPin2, maximum);  // Initialize the second ultrasonic sensor.
NewPing sonar3(trigPin, echoPin3, maximum);  // Initialize the third ultrasonic sensor.
NewPing sonar4(trigPin, echoPin4, maximum);  // Initialize the fourth ultrasonic sensor.
NewPing sonar5(trigPin, echoPin5, maximum);  // Initialize the fifth ultrasonic sensor.
NewPing sonar6(trigPin, echoPin6, maximum);  // Initialize the sixth ultrasonic sensor.

int readDHT, temp, hum, SoS;  // Variables for reading temperature and humidity, and calculating speed of sound.
float duration1, duration2, duration3, duration4, duration5, duration6;  // Variables to store the pulse duration from each ultrasonic sensor.
float distance1, distance2, distance3, distance4, distance5, distance6;  // Variables to store the calculated distance from each sensor.
int prev_r = 0, prev_g = 0, prev_b = 0; // Previous detected colors

void setup() {
  Serial.begin(9600);  // Start serial communication for debugging and output.

  Wire.begin(); // Initialize I2C communication.

  apds_write(ENABLE_REG, 0b00000011); // Enable the APDS9960 sensor.
  apds_write(ATIME_REG, 0xDB); // Set the integration time for the APDS9960 sensor.
  apds_write(CONTROL_REG, 0x01); // Set the gain for the APDS9960 sensor.
  // Read data from the DHT22 sensor.
  readDHT = dht11.readTemperatureAndHumidity(temp, hum);  
  
  // Calculate the speed of sound based on temperature and humidity using the formula.
  SoS = 331.4 + (0.6 * temp) + (0.0124 * hum);

}

void loop() {
  delay(120);

  uint16_t c = read16(CDATAL_REG); // Read the color data from the APDS9960 sensor.
  uint16_t r= read16(CDATAL_REG + 2); // Read the red color data.
  uint16_t g= read16(CDATAL_REG + 4); // Read the green color data.
  uint16_t b= read16(CDATAL_REG + 6); // Read the blue color data.

  int r255 = (c > 0) ? constrain((float)r / c * 255, 0, 255) : 0; // Convert the red color data to a value between 0 and 255.
  int g255 = (c > 0) ? constrain((float)g / c * 255, 0, 255) : 0; // Convert the green color data to a value between 0 and 255.
  int b255 = (c > 0) ? constrain((float)b / c * 255, 0, 255) : 0; // Convert the blue color data to a value between 0 and 255.

  int diff = abs(r255 - prev_r) + abs(g255 - prev_g) + abs(b255 - prev_b); // Calculate the difference in color values to detect significant changes.
  
  // Get the pulse duration from the first ultrasonic sensor and convert it to seconds.
  duration1 = sonar1.ping_median(2);  // Use median of 2 pings to avoid .
  duration1 = duration1 / 1000000;  // Convert microseconds to seconds.
  
  // Calculate the distance using the formula: distance = (speed of sound * duration) / 2.
  distance1 = (SoS * duration1) / 2;

  // Repeat the process for the other five ultrasonic sensors.
  duration2 = sonar2.ping_median(2);
  duration2 = duration2 / 1000000;
  distance2 = (SoS * duration2) / 2;
  
  duration3 = sonar3.ping_median(2);
  duration3 = duration3 / 1000000;
  distance3 = (SoS * duration3) / 2;
  
  duration4 = sonar4.ping_median(2);
  duration4 = duration4 / 1000000;
  distance4 = (SoS * duration4) / 2;
  
  duration5 = sonar5.ping_median(2);
  duration5 = duration5 / 1000000;
  distance5 = (SoS * duration5) / 2;
  
  duration6 = sonar6.ping_median(2);
  duration6 = duration6 / 1000000;
  distance6 = (SoS * duration6) / 2;

  if (diff > 60) { // Only check color if a big change happened
    if (b255 > 120 && r255 < 80 && g255 < 100) {
      Serial.println(String(distance1) + "," + String(distance2) + "," + String(distance3) + "," + String(distance4) + "," + String(distance5) + "," + String(distance6) + "b");
    } else if (r255 > 140 && g255 > 60 && g255 < 160 && b255 < 80) {
      Serial.println(String(distance1) + "," + String(distance2) + "," + String(distance3) + "," + String(distance4) + "," + String(distance5) + "," + String(distance6) + "o");
    } else {
      Serial.println(String(distance1) + "," + String(distance2) + "," + String(distance3) + "," + String(distance4) + "," + String(distance5) + "," + String(distance6) + "w");
    }
  }

  prev_r = r255;
  prev_g = g255;
  prev_b = b255;

  speed();
  if (speed != prev_speed){ // Check if speed has changed
    switch(speed){
      case "01":
        analogWrite(p, 64); // Set speed to 25%
        break;
      
      case "10":
        analogWrite(p, 128); // Set speed to 50%
        break;
      
      case "11":
        analogWrite(p, 255); // Set speed to 100%
        break;
    }
  }

  steering();
  if (steering != prev_steering){ // Check if steering has changed
    switch(steering){
      case "0000":
        //off
        break;

      case "0001":
        //l(low)
        stmotor(75); // Set steering motor to low left
        break;

      case "0010":
        //l(mid)
        stmotor(60); // Set steering motor to mid left
        break;

      case "0011":
        //l(full)
        stmotor(45); // Set steering motor to full left
        break;

      case "0100":
        //s(straight)
        stmotor(90); // Set steering motor to straight
        break;

      case "0101":
        //r(low)
        stmotor(105); // Set steering motor to low right
        break;

      case "0110":
        //r(mid)
        stmotor(120); // Set steering motor to mid right
        break;

      case "0111":
        //r(full)
        stmotor(135); // Set steering motor to full right
        break;
    }

  }
  prev_speed = speed; 
  prev_steering = steering;
}

void apds_write(uint8_t reg, uint8_t value) { // Function to write a value to a specific register of the APDS9960 sensor.
  Wire.beginTransmission(APDS9960_ADDR); // Start I2C transmission to the APDS9960 sensor.
  Wire.write(reg); // Write the register address.
  Wire.write(value); // Write the value to the register.
  Wire.endTransmission(); // End the I2C transmission.
}

void speed(){
  if (analogRead(s1) > 40){
    s1 = 1; // If the analog reading from s1 is greater than 40, set s1 to 1.
  }
  if (analogRead(s2) > 40){
    s2 = 1; // If the analog reading from s2 is greater than 40, set s2 to 1.
  }
  speed = String(String(m1) + String(m2)); // Combine the values of s1 and s2 to form the speed string.
  return speed
}

void steering(){
  if(analogRead(m1) > 40){
    m1 = 1; // If the analog reading from m1 is greater than 40, set m1 to 1.
  }
  if(analogRead(m2) > 40){
    m2 = 1; // If the analog reading from m2 is greater than 40, set m2 to 1.
  }
  if(analogRead(m3) > 40){
    m3 = 1; // If the analog reading from m3 is greater than 40, set m3 to 1.
  }
  if(analogRead(m4) > 40){
    m4 = 1; // If the analog reading from m4 is greater than 40, set m4 to 1.
  }
  steering = String(String(m1)+String(m2)+String(m3)+String(m4)); // Combine the values of m1, m2, m3, and m4 to form the steering string.
  return steering
}

uint16_t read16(uint8_t reg) { // Function to read a 16-bit value from a specific register of the APDS9960 sensor.
  Wire.beginTransmission(APDS9960_ADDR); // Start I2C transmission to the APDS9960 sensor.
  Wire.write(0x80 | reg); // Write the register address with the read command bit set.
  Wire.endTransmission(false); // End the transmission but keep the connection open for reading.
  Wire.requestFrom(APDS9960_ADDR, 2); // Request 2 bytes of data from the sensor.
  if (Wire.available() < 2) return 0; // If less than 2 bytes are available, return 0 (error).
  uint8_t lsb = Wire.read(); // Read the least significant byte.
  uint8_t msb = Wire.read(); // Read the most significant byte.
  return ((uint16_t)msb << 8) | lsb; // Combine the two bytes into a 16-bit value and return it.
}
