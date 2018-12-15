# https://github.com/Pithikos/python-websocket-server
# import logging
from websocket_server import WebsocketServer
import json
import threading
import RPi.GPIO as GPIO
import time
from time import sleep

Motor1A = 3
Motor1B = 5
global prevAngle
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)

GPIO.setup(12, GPIO.OUT)
global pwm
pwm = GPIO.PWM(12, 50)
pwm.start(0)

global pwmAngle


def doPWM():
    global pwm
    global pwmAngle

    duty = pwmAngle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

def setAngle(angle, pwm):
    print("Rudder " + str(angle))
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

def new_client(client, server):
    print('connected!')
    server.send_message_to_all("Hey all, a new client has joined us")


def message_received(client, server, message):
    global prevAngle
    print(message)
    if message[0] == '{':
        parsed_json = json.loads(message)
        direction = parsed_json['direction']
        throttle = parsed_json['throttle']
        rudder = parsed_json['rudder']
        maxRudder = parsed_json['maxRudder']
        minRudder = parsed_json['minRudder']
        rudderTrim = parsed_json['rudderTrim']
        print("Throttle " + str(throttle))
        print("Direction " + direction)
        percentageRudder = 0
        if (rudderTrim + rudder) > 0:
            percentageRudder = (rudderTrim + rudder) / maxRudder

        print("PercentageRudder : " + str(percentageRudder))
        print("Rudder Trim : " + str(rudderTrim))

        adjustedRudder = rudder

        if (rudder) < 0:
            rudder = 150#90 + (percentageRudder * 60)
            adjustedRudder = 150
        elif (rudder) > 0:
            rudder = 30 #90 - (-1 * percentageRudder * 60)
            adjustedRudder = 30
        else:
            adjustedRudder = 90 + rudderTrim
            rudder = 90

        if prevAngle != rudder:
            prevAngle = rudder
            setAngle(adjustedRudder, pwm)

        print("Rudder : " + str(rudder))

        if throttle == 0:
            GPIO.output(Motor1A, GPIO.LOW)
            GPIO.output(Motor1B, GPIO.LOW)
        elif direction == 'Forward':
            # Forwards
            GPIO.output(Motor1A, GPIO.LOW)
            GPIO.output(Motor1B, GPIO.HIGH)
        elif direction == 'Reverse':
            GPIO.output(Motor1A, GPIO.HIGH)
            GPIO.output(Motor1B, GPIO.LOW)
    else:
        print("\n\nNo Json!")


# message_received("", "", '{"throttle": 0,"rudder": 0,"rudderTrim": 0,"throttleMultiply": 1,"direction": "Forward","maxThrottle": 10,"minThrottle": 0,"maxRudder": 10,"minRudder": -10,"maxMultiplier": 10,"minMultiplier": 1,"maxRudderTrim": 10,"minRudderTrim": -10}')
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.LOW)
prevAngle = 90
pwmAngle = 90
#threading.Thread(target=doPWM).start()
# setAngle(prevAngle, pwm)
server = WebsocketServer(5005, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
