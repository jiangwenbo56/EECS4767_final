from picamera import PiCamera

# create camera object
camera = PiCamera()

# start taking picture
camera.start_preview()

# test