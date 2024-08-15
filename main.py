import TARS_Servo_Abstractor3
import TARS_Servo_Controller3
from adafruit_pca9685 import PCA9685
import board
import busio


# Initialize I2C bus
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Initialize PCA9685 on address 0x40
pwm = PCA9685(i2c_bus)
pwm.frequency = 60

#States
IDLE = 0
PORT_MAIN_PLUS = 1
PORT_MAIN_MINUS = 2
STAR_MAIN_PLUS = 3
STAR_MAIN_MINUS = 4
STEP_FORWARD = 5
TURN_RIGHT = 6
TURN_LEFT = 7
POSE = 8
UNPOSE = 9

state = IDLE

def main():
    global state
    print("Starting servo control...")

    while True:
        if state == PORT_MAIN_PLUS:
            TARS_Servo_Controller3.portMainPlus()
        elif state == PORT_MAIN_MINUS:
            TARS_Servo_Controller3.portMainMinus()
        elif state == STAR_MAIN_PLUS:
            TARS_Servo_Controller3.starMainPlus()
        elif state == STAR_MAIN_MINUS:
            TARS_Servo_Controller3.starMainMinus()
        elif state == STEP_FORWARD:
            TARS_Servo_Abstractor3.stepForward()
        elif state == TURN_RIGHT:
            TARS_Servo_Abstractor3.turnRight()
        elif state == TURN_LEFT:
            TARS_Servo_Abstractor3.turnLeft()
        elif state == POSE:
            TARS_Servo_Abstractor3.pose()
        elif state == UNPOSE:
            TARS_Servo_Abstractor3.unpose()
        else:
            print("Idle state, waiting for command...")

        time.sleep(1)  # Delay for 1 second between checks

if __name__ == "__main__":
    main()