"""
Networked gamepad relying on pygame library. Sending UDP packets to a host.
Each packet contains two characer of the form DB.

D is direction information: 0 (no direction) or w, a, s, d
B is information whether button is pressed (1) or not (0)
"""

import pygame
import socket
import config

HOST = config.NETWORK_JOYSTICK_HOST
PORT = config.NETWORK_JOYSTICK_PORT

print("Sending joystick information to", HOST, PORT)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.connect((HOST, PORT))


def handle_events(joystick):
    'Handle events and return direction and whether buttons is pressed'
    direction = None
    button_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            xaxis = 0
            yaxis = 1
            if joystick.get_axis(xaxis) > 0.5:
                direction = 'd'
            elif joystick.get_axis(xaxis) < -0.5:
                direction = 'a'
            elif joystick.get_axis(yaxis) > 0.5:
                direction = 's'
            elif joystick.get_axis(yaxis) < -0.5:
                direction = 'w'

        if event.type == pygame.JOYBUTTONDOWN:
            button_pressed = True
        if event.type == pygame.JOYBUTTONUP:
            button_pressed = False

        try:
            send_joystick_data(direction, button_pressed)
        except Exception as e:
            print(e)


def send_joystick_data(direction, btn_pressed):
    'send UDP packet with information about packet and button state'
    bp = '1' if btn_pressed else '0'
    di = '0' if direction is None else direction
    payload = bytes(di + bp, "ascii")
    print("sending", payload)
    sock.sendall(payload)


def main():
    pygame.init()

    clock = pygame.time.Clock()

    num_sticks = pygame.joystick.get_count()
    assert num_sticks > 0, "No Joysticks found."
    print("Found", pygame.joystick.get_count(), "joystick(s)")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Using the first joystick. name:", joystick.get_name())
    print("Using first button. numbuttons:", joystick.get_numbuttons())
    print("numaxes", joystick.get_numaxes(), "numhats", joystick.get_numhats())
    while True:
        handle_events(joystick)
        clock.tick(160)  # run at 60 Hz


if __name__ == '__main__':
    main()
