from flask import Flask
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
from flask import render_template
from flask import request

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

all_pins = [8,11,13]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/index')
def signUp():
    return render_template('index.html')

@app.route('/light-led', methods=['POST'])
def light_up():
    pin = request.args.get('pin')
    pin = int(pin)
    for x in all_pins:
        if(x != pin):
            GPIO.output(x, GPIO.LOW)

    GPIO.output(pin, GPIO.HIGH) # Turn on
    return ""

if __name__ == "__main__":
    GPIO.output(8, GPIO.HIGH) # Turn on
    app.run(host='0.0.0.0')