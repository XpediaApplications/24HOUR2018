# https://github.com/Pithikos/python-websocket-server
# import logging
from websocket_server import WebsocketServer
import json
import RPi.GPIO as GPIO

Motor1A = 3
Motor1B = 5
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)

GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(0)

def SetAngle(angle,pwm):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)

def new_client(client, server):
    print('connected!')
    server.send_message_to_all("Hey all, a new client has joined us")

def message_received(client, server, message):
    json = message
    parsed_json = json.loads(json_string)
    direction = parsed_json['direction']
    throttle = int(parsed_json['throttle'])
    print("Throttle " + throttle)
    print("Direction " + direction)
    if throttle == 0:
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.LOW)
    elif direction == 'Forward':
        # Forwards
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)

message_received("", "", '{"throttle": 0,"rudder": 0,"rudderTrim": 0,"throttleMultiply": 1,"direction": "Forward","maxThrottle": 10,"minThrottle": 0,"maxRudder": 10,"minRudder": -10,"maxMultiplier": 10,"minMultiplier": 1,"maxRudderTrim": 10,"minRudderTrim": -10}')

server = WebsocketServer(5005, host='127.0.0.1')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received,Motor1A,Motor1B,pwm)
server.run_forever()