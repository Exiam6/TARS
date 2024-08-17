from __future__ import division
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from threading import Thread

# Initialize I2C bus and PCA9685 on address 0x40
i2c_bus = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c_bus)
pwm.frequency = 60  # Set frequency to 60hz, good for servos.

servo_0 = servo.Servo(pwm.channels[0])
servo_1 = servo.Servo(pwm.channels[1])
servo_2 = servo.Servo(pwm.channels[2])
angles = {
    'default': 90,
    'neutralHeight': 90,
    'upHeight': 120,
    'downHeight': 60,
    'neutralPort': 90,
    'forwardPort': 90,
    'backPort': 60,
    'neutralStarboard': 90,
    'forwardStarboard': 120,
    'backStarboard': 60
}


# Moves the torso from a neutral position upwards
def height_neutral_to_up():
    print('Setting center servo (0) from Neutral to Up position')
    try:
        while servo_0.angle > angles['upHeight']:
            servo_0.angle -= 1
            time.sleep(0.001)
    except:
        return
    print('Center servo (0) set to Up position\n')


# Rotates the torso outwards to pivot and land flush with the ground
def torso_neutral_to_forwards():
    print('Setting port and starboard servos (1)(2) from Neutral to Forward')

    servo_1.angle = 120
    servo_2.angle = 60

    # time.sleep(0.0001)
    print('Port and starboard servos (1)(2) set to Forward position\n')


# Rotates the torso backwards to pivot and land
def torso_neutral_to_backwards():
    print('Setting port and starboard servos (1)(2) from Neutral to Backward')
    while servo_1.angle > angles['backPort']:
        servo_1.angle -= 1
        servo_2.angle += 1
        time.sleep(0.0001)
    print('Port and starboard servos (1)(2) set to Backward position\n')


# Rapidly shifts the torso height up and down, causing TARS to pivot
def torso_bump():
    print('Performing a torso bump')
    print('Setting center servo (0) Up to Down position FAST')
    try:
        while servo_0.angle < angles['downHeight']:
            servo_0.angle += 2
            time.sleep(0.000001)
        print('Setting center servo (0) Down to Up position FAST')
        while servo_0.angle > angles['upHeight']:
            servo_0.angle -= 1
            time.sleep(0.0001)
        print('Center servo (0) returned to Up position\n')
    except:
        return


# Returns the torso to a neutral position
def torso_return():
    t1 = Thread(target=torso_return_rotation)
    t2 = Thread(target=torso_return_vertical)
    t1.start()
    t2.start()


# Returns torso's rotation to neutral from forward
def torso_return_rotation():
    print('Setting port and starboard servos (1)(2) from Forward to Neutral position')
    while servo_1.angle > angles['neutralPort']:
        servo_1.angle -= 1
        servo_2.angle += 1
        time.sleep(0.005)
    print('Port and starboard servos (1)(2) set to Neutral position\n')


# Returns torso's vertical height to neutral from up
def torso_return_vertical():
    print('Setting center servo (0) from Up to Neutral position')
    try:
        while servo_0.angle < angles['downHeight']:
            servo_0.angle += 1
            time.sleep(0.00005)
        while servo_0.angle > angles['neutralHeight']:
            servo_0.angle -= 1
            time.sleep(0.00001)
        print('Center servo (0) set to Neutral position\n')
    except:
        return


# Moves the torso from neutral position to down
def neutral_to_down():
    print('Setting center servo (0) from Neutral to Down position')
    while servo_0.angle < angles['downHeight']:
        servo_0.angle += 1
        time.sleep(0.001)


# Moves the torso from down to up
def down_to_up():
    print('Setting center servo (0) from Down to Up position')
    while servo_0.angle > angles['upHeight']:
        servo_0.angle -= 1
        time.sleep(0.001)


# Moves the torso from down to neutral
def down_to_neutral():
    print('Setting center servo (0) from Down to Neutral position')
    while servo_0.angle > angles['neutralHeight']:
        servo_0.angle -= 1
        time.sleep(0.001)


# Turns the torso to the right
def turn_right():
    print('Turning right')
    while servo_1.angle < angles['forwardPort']:
        servo_1.angle += 1
        servo_2.angle += 1
        time.sleep(0.001)


# Turns the torso to the left
def turn_left():
    print('Turning left')
    while servo_1.angle > angles['backPort']:
        servo_1.angle -= 1
        servo_2.angle -= 1
        time.sleep(0.001)


# Returns the torso to neutral from the right
def neutral_from_right():
    print('Returning from right to neutral')
    while servo_1.angle > angles['neutralPort']:
        servo_1.angle -= 1
        servo_2.angle -= 1
        time.sleep(0.005)
    servo_1.angle = angles['neutralPort']
    servo_2.angle = angles['neutralStarboard']


# Returns the torso to neutral from the left
def neutral_from_left():
    print('Returning from left to neutral')
    while servo_1.angle < angles['neutralPort']:
        servo_1.angle += 1
        servo_2.angle += 1
        time.sleep(0.005)
    servo_1.angle = angles['neutralPort']
    servo_2.angle = angles['neutralStarboard']
