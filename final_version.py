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

Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)

while True:

    # check message from light sensor from esp8266
    if (GPIO.input(16) == 1):

        # start taking picture
        camera.start_preview()
        time.sleep(5)
        camera.capture('image.jpg')
        camera.stop_preview()

        # Loads the image into memory
        # image = open('bulb.png', 'rb')
        image = open('image.jpg', 'rb')

        clientsocket = socket(AF_INET, SOCK_STREAM)
        clientsocket.connect((severName, serverPort))
        temp = "end of image".encode()

        content = image.read(4096)
        while content:
            clientsocket.send(content)
            content = image.read(4096)
        print("done")
        image.close()
        time.sleep(2)
        clientsocket.send(temp)
        # clientsocket.sendall(temp)

        result = clientsocket.recv(4096)
        print(result.decode())


        if result:
            EN1.start(0)

            for x in range(40, 70):
                print("FORWARD MOTION")
                EN1.ChangeDutyCycle(x)

                GPIO.output(Motor1['input1'], GPIO.HIGH)
                GPIO.output(Motor1['input2'], GPIO.LOW)

                sleep(0.1)

            print("STOP")
            EN1.ChangeDutyCycle(0)

            sleep(3)

            for x in range(40, 70):
                print("BACKWARD MOTION")
                EN1.ChangeDutyCycle(x)

                GPIO.output(Motor1['input1'], GPIO.LOW)
                GPIO.output(Motor1['input2'], GPIO.HIGH)

                sleep(0.1)

            print("STOP")
            EN1.ChangeDutyCycle(0)

