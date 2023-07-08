import RPi.GPIO as GPIO
#This means we will refer to the GPIO pins
#by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BOARD)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(11, GPIO.OUT)

GPIO.output(11, 0)
# Add this at the end
#GPIO.cleanup()
