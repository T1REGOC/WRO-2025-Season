import multiprocessing # Importing the multiprocessing module
import WRO_logic # Importing the WRO_logic module for the main logic of the program
import SerialWRO # Importing the SerialWRO module for serial communication

if __name__ == "__main__": 
    manager = multiprocessing.Manager() # Creating a manager to handle shared data between processes
    values = manager.list([0, 0, 0, 0, 0, 0, '', 0, 0])  # Shared list for sensor values
                # sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, way, blue(count), orange(count)
    p1 = multiprocessing.Process(target=WRO_logic.main, args=(values,)) # Main logic process
    p2 = multiprocessing.Process(target=SerialWRO.serial_reader, args=(values,)) # Serial reader process

    p1.start() # Starting the main logic process
    p2.start() # Starting the serial reader process

    p1.join() # Waiting for the main logic process to finish
    p2.join() # Waiting for the serial reader process to finish