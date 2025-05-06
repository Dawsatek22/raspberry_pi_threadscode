# This is a python3 file to to control 2 differrent motor I2c motor hats stacked together

import motoron # To control the motor hat
from time import sleep # To use the sleep function
import board 
import threading
from threading import Thread
# more info on pololu motoron boards here:https://www.pololu.com/docs/0J84/all
# More info about using the adafruit_motorkit here:https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper # to control the stepper motor

kit = MotorKit(i2c=board.I2C()) 
mc = motoron.MotoronI2C()

# Reset the controller to its default settings, then disable CRC.  The bytes for
# each of these commands are shown here in case you want to implement them on
# your own without using the library.
mc.reinitialize()  # Bytes: 0x96 0x74
mc.disable_crc()   # Bytes: 0x8B 0x04 0x7B 0x43

# Clear the reset flag, which is set after the controller reinitializes and
# counts as an error.
mc.clear_reset_flag()  # Bytes: 0xA9 0x00 0x04

# By default, the Motoron is configured to stop the motors if it does not get
# a motor control command for 1500 ms.  You can uncomment a line below to
# adjust this time or disable the timeout feature.
# mc.set_command_timeout_milliseconds(1000)
# mc.disable_command_timeout()

# Configure motor 1.
mc.set_max_acceleration(1, 140)
mc.set_max_deceleration(1, 300)

# Configure motor 2.
mc.set_max_acceleration(2, 200)
mc.set_max_deceleration(2, 300)

# Function below controls the stepper motor.
def runstepper1():
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE) # stepper moves backward    print("Stepper is spining")
    sleep(0.5)
 # Function below controls 2 dc motors.   
def rundc2x():
    mc.set_speed(1, 200)
    mc.set_speed(2,-200)
    print("Motors are moving forward")
    sleep(2)
    mc.set_speed(1,0)
    mc.set_speed(2,0)
    print("Motors are stopping")
    sleep(2)
    
    mc.set_speed(1,-200)
    mc.set_speed(2,200)
    print("Motors are moving backward")
    sleep(2)
    

    
while True:
    # The threads are created.
    t1 = Thread(target=runstepper1(), args=(10,) )
    t2 = Thread(target=rundc2x() , args=(10,))
    # The threads are starting.
    t1.start()
    t2.start()
    

    print("Done!")
 

    