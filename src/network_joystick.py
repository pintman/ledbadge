'''
This package contains a joystick that can be trigered via UDP packets over the
network.
'''

import usocket as socket
import network

import config
import utaskmanager


sta_if = network.WLAN(network.STA_IF)

HOST = sta_if.ifconfig()[0]  # take ip address
PORT = config.NETWORK_JOYSTICK_PORT


class NetworkedJoystick(utaskmanager.Task):
    def __init__(self, host, port):
        'create joystick with given pins for directions and button.'
        super().__init__()
        self.host = host
        self.port = port
        self._direction = None
        self._btn_pressed = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        print("Binding socket to ", self.host, self.port)
        self.sock.bind((self.host, self.port))

    def task_step(self):        
        try:
            # trying to fetch from socket
            dir_btn = self.sock.recv(1024)
        except Exception:
            return

        print("received", dir_btn)
        dir_btn = str(dir_btn, "ascii")
        d = None if dir_btn[0] == '0' else dir_btn[0]
        self.set(d, dir_btn[1] == '1')

    def btn_pressed(self):
        'Return whether button is pressed.'
        return self._btn_pressed

    def direction(self):
        'get the current direction. One of w, a, s, d or None.'
        return self._direction

    def set(self, direction, btn_pressed):
        self._direction = direction
        self._btn_pressed = btn_pressed

        # fix upside down
        if direction == 'w':
            self._direction = 's'
        elif direction == 's':
            self._direction = 'w'


joy = NetworkedJoystick(HOST, PORT)
