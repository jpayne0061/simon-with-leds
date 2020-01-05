from flask import Flask
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
from flask import render_template
from flask import request
import random
from flask import abort

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)

all_pins = [11,5,3]

current_sequence = []

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

@app.route('/check-sequence', methods=['POST'])
def check_sequence():
    user_sequence = request.args.get('sequence')
    print('user sequence: ' + user_sequence)
    print('current_sequence')
    print(current_sequence)
    user_sequence = user_sequence.split(',')
    user_sequence = [int(i) for i in user_sequence]
    for i in range(0, len(current_sequence)):
        try:
            if(user_sequence[i] != current_sequence[i]):
                wrong_answer()
                start_new()
                return "fail"
        except IndexError:
            wrong_answer()
            start_new()
            return "fail"

    add_to_sequence()
    sleep(1)
    display_current_sequence()
    return ""

def wrong_answer():
    for i in range(0, 5):
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        sleep(0.125)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        sleep(0.125)

def start_new():
    global current_sequence
    current_sequence = []
    rand_pin = gen_random_pin()
    current_sequence.append(rand_pin)
    GPIO.output(rand_pin, GPIO.HIGH) # Turn on
    sleep(0.5)
    GPIO.output(rand_pin, GPIO.LOW) # Turn on

def add_to_sequence():
    rand_pin = gen_random_pin()
    current_sequence.append(rand_pin)

def all_pins_low():
    for p in all_pins:
        GPIO.output(p, GPIO.LOW)

def display_current_sequence():
    for p in current_sequence:
        GPIO.output(p, GPIO.HIGH)
        sleep(0.3)
        GPIO.output(p, GPIO.LOW)
        sleep(0.3)


def gen_random_pin():
    return all_pins[random.randint(0,2)]

if __name__ == "__main__":
    start_new()
    app.run(host='0.0.0.0')
