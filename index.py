from flask import Flask, jsonify
import os
import Adafruit_DHT
import RPi.GPIO as GPIO

app = Flask(__name__)

# Temperature sensor setup
SENSOR = Adafruit_DHT.DHT11
SENSOR_PIN = 4

# Soil moisture sensor setup
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# Variable to store the soil moisture state
soil_moisture = None

def callback(channel):
    """Update the soil moisture state."""
    global soil_moisture
    if GPIO.input(channel):
        soil_moisture = "Water Detected!"
    else:
        soil_moisture = "No Water Detected!"

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

@app.route('/switch_on', methods=['GET'])
def switch_on():
    """Turn the switch on by calling the on.py script."""
    os.system('python on.py')
    return "Switch turned on"

@app.route('/switch_off', methods=['GET'])
def switch_off():
    """Turn the switch off by calling the off.py script."""
    os.system('python off.py')
    return "Switch turned off"

@app.route('/temperature', methods=['GET'])
def get_temperature():
    """Get the current temperature and humidity."""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN)
    if temperature is not None and humidity is not None:
        return jsonify({
            "temperature_C": temperature,
            "humidity": humidity,
            "sensor_status": "connected"
        })
    else:
        return jsonify({
            "error": "Failed to get temperature and humidity readings.",
            "sensor_status": "disconnected"
        })

@app.route('/soil_moisture', methods=['GET'])
def get_soil_moisture():
    """Get the soil moisture state."""
    if GPIO.input(channel):
        soil_moisture = "No Water Detected!"
    else:
        soil_moisture = " Water Detected!"
    
    return jsonify({
        "soil_moisture": soil_moisture,
        "sensor_status": "connected"
    })

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()  # Ensure all GPIO resources are cleaned up
