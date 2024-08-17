import requests
import os
import time
import threading
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import board
import busio

# Initialize I2C bus and PCA9685
i2c_bus = busio.I2C(board.SCL, board.SDA)
pwm = PCA9685(i2c_bus)
pwm.frequency = 60

# Initialize servos
servo_0 = servo.Servo(pwm.channels[0])
servo_1 = servo.Servo(pwm.channels[1])
servo_2 = servo.Servo(pwm.channels[2])

# States
IDLE = 0
STEP_FORWARD = 1
TURN_RIGHT = 2
TURN_LEFT = 3
POSE = 4
UNPOSE = 5

# Current state
state = IDLE


# Function to record audio using arecord
def record(MIC_INDEX=0, DURATION=5):
    '''
    Record audio using the specified microphone.
    MIC_INDEX: Microphone ID (use `arecord -l` to find the ID)
    DURATION: Duration of the recording in seconds
    '''
    print(f'Starting {DURATION} seconds of recording...')
    os.system(f'sudo arecord -D "plughw:{MIC_INDEX}" -f dat -c 1 -r 16000 -d {DURATION} temp/speech_record.wav')
    print('Recording finished')


# Function to play audio on Raspberry Pi
def play_audio(filename):
    os.system(f'aplay {filename}')


# Intranet Penetration
upload_url = 'https://7d9c-202-66-60-166.ngrok-free.app/upload'
download_url = 'https://7d9c-202-66-60-166.ngrok-free.app/download'

# File paths
input_file = 'temp/speech_record.wav'
response_file = 'response.wav'


def perform_action(action):
    global state
    if action == STEP_FORWARD:
        state = STEP_FORWARD
        TARS_Servo_Abstractor3.stepForward()
    elif action == TURN_RIGHT:
        state = TURN_RIGHT
        TARS_Servo_Abstractor3.turnRight()
    elif action == TURN_LEFT:
        state = TURN_LEFT
        TARS_Servo_Abstractor3.turnLeft()
    elif action == POSE:
        state = POSE
        TARS_Servo_Abstractor3.pose()
    elif action == UNPOSE:
        state = UNPOSE
        TARS_Servo_Abstractor3.unpose()
    else:
        state = IDLE
        print("Idle state, waiting for command...")


def main():
    global state
    global servo_0, servo_1, servo_2
    print("TARS awaken...")

    while True:
        # Record audio from microphone using arecord
        record(MIC_INDEX=0, DURATION=5)

        # Upload audio to the server
        with open(input_file, 'rb') as file:
            files = {'file': file}
            response = requests.post(upload_url, files=files, verify=False)

        # Handle the response
        if response.status_code == 200:
            json_response = response.json()
            print("Server response:", json_response['response'])

            filename = json_response['file_url']
            file_response = requests.post(download_url, json={'filename': filename}, verify=False)

            with open(response_file, 'wb') as f:
                f.write(file_response.content)

            action = json_response.get('action', IDLE)

            # Create threads for action and audio playback simultaneously
            action_thread = threading.Thread(target=perform_action, args=(action,))
            audio_thread = threading.Thread(target=play_audio, args=(response_file,))

            action_thread.start()
            audio_thread.start()

            action_thread.join()
            audio_thread.join()

        else:
            print(f"Failed to upload audio. Status code: {response.status_code}")

        time.sleep(1)


if __name__ == "__main__":
    main()
