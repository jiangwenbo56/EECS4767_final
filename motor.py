import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)    
EN2 = GPIO.PWM(Motor2['EN'], 500)

EN1.start(0)                    
EN2.start(0)                    

while True:
    for x in range(40, 70):
        print ("FORWARD MOTION")
        EN1.ChangeDutyCycle(x)
        EN2.ChangeDutyCycle(x)

        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)
        
        GPIO.output(Motor2['input1'], GPIO.HIGH)
        GPIO.output(Motor2['input2'], GPIO.LOW)

        sleep(0.1)
   
    print ("STOP")
    EN1.ChangeDutyCycle(0)
    EN2.ChangeDutyCycle(0)

    sleep(3)
     
    for x in range(40, 70):
        print ("BACKWARD MOTION")
        EN1.ChangeDutyCycle(x)
        EN2.ChangeDutyCycle(x)
        
        GPIO.output(Motor1['input1'], GPIO.LOW)
        GPIO.output(Motor1['input2'], GPIO.HIGH)

        GPIO.output(Motor2['input1'], GPIO.LOW)
        GPIO.output(Motor2['input2'], GPIO.HIGH)

        sleep(0.1)
     
    print ("STOP")
    EN1.ChangeDutyCycle(0)
    EN2.ChangeDutyCycle(0)

    sleep(3)

GPIO.cleanup()