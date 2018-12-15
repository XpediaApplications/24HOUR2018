# https://github.com/Pithikos/python-websocket-server
import logging
import threading
import json
import RPi.GPIO as GPIO
from websocket_server import WebsocketServer
from time import sleep

rudder_pin = 7
motor_pin1 = 3
motor_pin2 = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(0)


def new_client(client, server):
    print('connected!')
    server.send_message_to_all("Hey all, a new client has joined us")


def message_received(client, server, message):
    print("Message: " + message + "\r\n")
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(message,)
    )
    client_handler.start()


#    handle_client_connection(message)

def handle_client_connection(message):
    try:
        data = json.loads(message)
    except:
        print("No JSON object to decode")
        return
    print(data["throttle"])
    print(data["rudder"])
    try:
        print("motor")
        start_motors(data["throttle"], data["direction"])
    except:
        print("start motors exception")
    try:
        print("angle")
        # set_angle(data["rudder"])
    except:
        print("set_angle exception")
    print ("Client connection handled")


def calculate_angle(angle_value):
    print("Entered calc angle", angle_value)
    ##    start_position = 85
    ##    max_rudder_rotation = 25
    ##    max_angle = 110
    ##    min_angle = 60
    ##
    ##    print("angle -1")
    ##    if angle_value == 0:
    ##        print("angle 0")
    ##        return start_position
    ##
    ##    print("angle 1")
    ##    angle = start_position+((max_rudder_rotation/max_angle_value)*angle_value)
    ##    print("angle 2")
    ##    if angle > max_angle:
    ##        angle = max_angle
    ##    elif angle < min_angle:
    ##        angle = min_angle
    ##    print("angle 3")
    angle = 85 + 5 * angle_value
    return angle


def set_angle(angle_value):
    print("Entered set angle")
    angle = calculate_angle(angle_value)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(rudder_pin, GPIO.OUT)
    pwm = GPIO.PWM(rudder_pin, 50)
    pwm.start(0)
    degree = int(angle) / 18 + 2
    GPIO.output(rudder_pin, True)
    pwm.ChangeDutyCycle(degree)
    sleep(0.1)
    GPIO.output(rudder_pin, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    print("Set angle complete")


def start_motors(direction_value, direction):
    print("Entered start motors, direction: ", direction_value)
    forward = True
    is_stopped = False

    if direction_value == 0:
        is_stopped = True
    elif direction == 'Forward':
        forward = True
        is_stopped = False
    else:
        forward = True
        is_stopped = False

    print("Moving forward: {}", forward)

    if is_stopped:
        print("Stop")
        GPIO.output(3, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)
    else:
        print("start")
        GPIO.output(3, forward)
        GPIO.output(5, not forward)
    print("Motor done")


server = WebsocketServer(5005, host='0.0.0.0')
start_motors(0, 'Forward')
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()
# pwm.stop()
# GPIO.cleanup()
