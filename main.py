from picamera import PiCamera
import time, io, os
from socket import *

# create camera object
camera = PiCamera()

# set the camera to the max resolution
# camera.resolution = (2592, 1944)
camera.resolution = (2000, 980)
camera.framerate = 15

# start taking picture
camera.start_preview()
time.sleep(5)
camera.capture('image.jpg')
camera.stop_preview()

# Loads the image into memory
# image = open('bulb.png', 'rb')
image = open('image.jpg', 'rb')


severName = '54.83.98.170'
serverPort = 4736
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

