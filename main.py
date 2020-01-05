from flask import Flask
import RPi.GPIO as GPIO
from time import sleep
from flask import render_template
from flask import request
import random
from flask import abort

PIN_ELEVEN = 11
PIN_FIVE = 5
PIN_THREE = 3

ALL_PINS = [PIN_ELEVEN, PIN_FIVE, PIN_THREE]

CURRENT_SEQUENCE = []

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(PIN_ELEVEN, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(PIN_FIVE, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(PIN_THREE, GPIO.OUT, initial=GPIO.LOW) 

app = Flask(__name__)

@app.route('/')
def signUp():
    return render_template('index.html')

@app.route('/check-sequence', methods=['POST'])
def check_sequence():
    user_sequence = request.args.get('sequence')
    user_sequence = user_sequence.split(',')
    user_sequence = [int(i) for i in user_sequence]

    for i in range(0, len(CURRENT_SEQUENCE)):
        try:
            if(user_sequence[i] != CURRENT_SEQUENCE[i]):
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
    for _i in range(0, 5):
        GPIO.output(PIN_ELEVEN, GPIO.HIGH)
        GPIO.output(PIN_FIVE, GPIO.HIGH)
        GPIO.output(PIN_THREE, GPIO.HIGH)
        sleep(0.125)
        GPIO.output(PIN_ELEVEN, GPIO.LOW)
        GPIO.output(PIN_FIVE, GPIO.LOW)
        GPIO.output(PIN_THREE, GPIO.LOW)
        sleep(0.125)

def start_new():
    global CURRENT_SEQUENCE
    CURRENT_SEQUENCE = []
    rand_pin = gen_random_pin()
    CURRENT_SEQUENCE.append(rand_pin)
    GPIO.output(rand_pin, GPIO.HIGH) # Turn on
    sleep(0.5)
    GPIO.output(rand_pin, GPIO.LOW) # Turn on

def add_to_sequence():
    rand_pin = gen_random_pin()
    CURRENT_SEQUENCE.append(rand_pin)

def all_pins_low():
    for p in ALL_PINS:
        GPIO.output(p, GPIO.LOW)

def display_current_sequence():
    for p in CURRENT_SEQUENCE:
        GPIO.output(p, GPIO.HIGH)
        sleep(0.3)
        GPIO.output(p, GPIO.LOW)
        sleep(0.3)

def gen_random_pin():
    return ALL_PINS[random.randint(0,2)]

if __name__ == "__main__":
    start_new()
    app.run(host='0.0.0.0')
