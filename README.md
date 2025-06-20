# WRO-2025-Season
Respitory of the code, 3d files of the robot and some documents for the 2025 WRO Future Engineers competition from T1 REGOČ, Prigorje Brdovečko, Croatia.

About the Robot:

Introduction:

For the “Future Engineers” category, our team was given the challenge of building and programming a robot that could complete two specific tasks: the “Open Challenge” and the “Obstacle Challenge.” However, this was not just about making something that worked—we also had to follow a strict set of rules laid out in the competition guidelines. These rules covered everything from dimensions and sensors to motors and power sources. One of the most important limitations was the rule about the drive system. We couldn’t design our own custom solution from scratch. Instead, we had to choose from a set of approved drive systems listed in the rules document.
After reviewing the available options and doing research on each of them, we carefully considered which one would be the most efficient and reliable for our tasks. We eventually chose the one that best fit both challenges, and the rest of our design was built around that choice. This document explains the choices we made in terms of mechanical construction, electronics, sensors, and how the robot performs in practice.
________________________________________
Mechanical Construction and Electronics

One of the first decisions we made during the design process was about the drive system. After comparing the performance of different systems, we chose a differential drive system, which is commonly used in robotics for its simplicity and reliability. This type of system allows the robot to turn by varying the speed of the wheels on each side. Within the differential options, there are open and closed types. Open differential systems are more suitable for off-road or rough terrain. But since our robot will operate mostly on flat, indoor surfaces, we decided to use a closed differential system, which offers more stability and control.
In this setup, one TT Gear Motor is used to spin a gear, which then drives another gear connected to the wheels. This allows smooth and balanced movement. The TT Gear Motor is a compact and efficient DC motor that delivers good torque even at low voltages. Although it can run at 3V, we’ve chosen to power it using a 5V supply through an L298N motor driver to improve speed and torque. The L298N module also allows us to control the motor’s direction and speed using PWM signals.
When it came to steering our team designed a custom version of the Ackermann steering system, which is commonly used in real cars. In our design, there is a fixed base segment attached to the robot’s body. On either side of this segment, we placed two vertical pillars. Attached to these pillars are motor holders—these are the parts that actually move the wheels which are attached with a piece connecting them together. That piece, that holds them together is spun by a servo.
A SG90 servo motor is connected to this segment. When the servo turns left or right, it rotates the entire upper part of the system, causing both motor holders to turn together. This moves the front wheels in the correct direction, just like in a car. The SG90 was chosen because it is small, affordable, and operates perfectly at 5V. It is also known for its reliability.
For processing and control, we decided to utilize both the microcontroller board Arduino Uno and a Raspberry Pi 4 single-board computer. Each of them serving distinct roles within the system. The Arduino Uno is responsible for interacting with analog and real-time digital sensors, including six HC-SR04 ultrasonic distance sensors, APDS-9960 color sensor and a DHT22 temperature and humidity sensor. Its low-latency response makes it ideal for handling time-sensitive sensor readings. On the other side of our robots „brain“ we have the Raspberry Pi 4 used for high-level processing tasks, such as camera based vision processing and overall system coordination. We can compare the Raspberry Pi 4 and the Arduino Uno as the brain and nervous system. The Arduino Uno is used for sensing and reacting while the Raspberry Pi 4 is like the brain by thinking, seeing and deciding. The Raspberry Pi 4 was the perfect choice providing over 600 times the computational power of the Arduino Uno, making it perfect for demanding tasks.
To improve the accuracy of the ultrasonic readings, we added a DHT22 temperature and humidity sensor. The speed of sound can change based on air temperature and humidity, which affects the accuracy of distance readings from ultrasonic sensors. By using the data from the DHT22, we can apply corrections to the ultrasonic sensor calculations, making our readings more reliable under different conditions.
For processing and control, we decided to use a microcontroller Arduino Uno and a single board computer Raspberry Pi 4. Each of them serves a different role. The Arduino Uno is used for reading sensors that require analog inputs—something the Raspberry Pi doesn’t have. On the other hand, the Raspberry Pi 4 is here because of its processing speed and camera control. Both of these boards operate at 5V.
To power everything, we use a 3.7V 1200mAh lithium-ion battery. However, since most of our components require a 5V power supply, we use a step-up voltage regulator (S13V20F5) to convert 3.7V from the battery up to a stable 5V output. This regulator is efficient and powerful enough to handle the load from our system.

![image](https://github.com/user-attachments/assets/97a3729f-8817-4d37-a062-a4e2b6a05da8)

Bill of materials. 



________________________________________
Practical Use of the Robotic Solution

Now let’s talk about how the robot works in real situations. As soon as the start button is pressed, the robot begins moving forward. It looks for a colored line on the ground—either orange or blue. Depending on which color it detects first, the robot will turn left or right. Every time it crosses a colored line, a counter in the code increases. Once the counter reaches twelve, that means the robot has completed three laps around the course. At that point, the current movement code ends, and the robot either begins its parking sequence or returns to the starting area.
When the robot encounters obstacles, it uses the Raspberry Pi Camera to recognize and avoid them.
For the parallel parking task, the process is broken down into two parts: lining up and parking. First, the robot uses the two side ultrasonic sensors to make sure it is lined up perfectly parallel to the wall. It keeps adjusting until both side sensors give almost the same reading. Once the robot is aligned, it begins a classic parallel parking process, which includes moving backward at an angle, straightening out, and then moving forward to complete the parking.

![image](https://github.com/user-attachments/assets/1c51d363-3c81-4b05-8dcd-12d7d6b6e8db)

Electrical Scheme


