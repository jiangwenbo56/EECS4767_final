from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import time, io, os
from socket import *

# set the GPIO to BCM mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# use pin 16 to read message from esp8266
GPIO.setup(16, GPIO.IN)

# create camera object
camera = PiCamera()

# set the camera to the max resolution
# camera.resolution = (2592, 1944)
camera.resolution = (2592, 900)
camera.framerate = 15

severName = '54.83.98.170'
serverPort = 4745

# motor for push and pull plate
Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}

# motor for car
Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}

trash_can = ["dry", "wet", "recyclable", "hazard"]

current_location = 0

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)
EN2 = GPIO.PWM(Motor2['EN'], 100)

while True:

    # check message from light sensor from esp8266
    if (GPIO.input(16) == 1):

        # start taking picture
        camera.start_preview()
        time.sleep(1)
        camera.capture('image.jpg')
        camera.stop_preview()

        # Loads the image into memory
        image = open('image.jpg', 'rb')

        clientsocket = socket(AF_INET, SOCK_STREAM)
        clientsocket.connect((severName, serverPort))
        temp = "end of image".encode()

        content = image.read(4096)

        # send message to the cloud
        while content:
            clientsocket.send(content)
            content = image.read(4096)
        print("done")
        image.close()
        time.sleep(1)
        clientsocket.send(temp)

        # receive the result from the cloud
        result = clientsocket.recv(4096).decode()
        print(result)

        # Analyze the result
        if result:
            # activa the car motor
            EN2.start(0)

            destination = trash_can.index(result)
            offset = destination - current_location

            for x in range(40, 50 + abs(offset) * 10):
                print("Car moving")
                EN2.ChangeDutyCycle(x)

                if (offset > 0):
                    GPIO.output(Motor2['input1'], GPIO.HIGH)
                    GPIO.output(Motor2['input2'], GPIO.LOW)

                else:
                    GPIO.output(Motor2['input1'], GPIO.LOW)
                    GPIO.output(Motor2['input2'], GPIO.HIGH)

                sleep(0.1)

            print("STOP")
            EN2.ChangeDutyCycle(0)

            # update current location
            current_location = destination
            sleep(2)

            # activate the push and pull plate
            EN1.start(0)
            for x in range(40, 80):
                print("FORWARD MOTION")
                EN1.ChangeDutyCycle(x)

                GPIO.output(Motor1['input1'], GPIO.HIGH)
                GPIO.output(Motor1['input2'], GPIO.LOW)

                sleep(0.1)

            print("STOP")
            EN1.ChangeDutyCycle(0)

            sleep(1)

            for x in range(40, 60):
                print("BACKWARD MOTION")
                EN1.ChangeDutyCycle(x)

                GPIO.output(Motor1['input1'], GPIO.LOW)
                GPIO.output(Motor1['input2'], GPIO.HIGH)

                sleep(0.1)

            print("STOP")
            EN1.ChangeDutyCycle(0)
