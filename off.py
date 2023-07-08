import RPi.GPIO as GPIO

# Disable warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, 1)

# Add this at the end
GPIO.cleanup()


