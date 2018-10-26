'''
This package contains a joystick that can be trigered via UDP packets over the
network.
'''

import uasyncio as asyncio
import usocket as socket
import config
import network

sta_if = network.WLAN(network.STA_IF)

HOST = sta_if.ifconfig()[0]  # take ip address
PORT = config.NETWORK_JOYSTICK_PORT


class NetworkedJoystick:
    def __init__(self):
        'create joystick with given pins for directions and button.'
        self._direction = None
        self._btn_pressed = False

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


joy = NetworkedJoystick()


async def as_handle_udp_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    print("Binding socket to ", HOST, PORT)
    sock.bind((HOST, PORT))

    while True:
        try:
            dir_btn = sock.recv(1024)
        except Exception:
            await asyncio.sleep_ms(10)
            continue

        print("received", dir_btn)
        dir_btn = str(dir_btn, "ascii")
        joy.set(dir_btn[0], dir_btn[1] == '1')
        await asyncio.sleep_ms(5)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(as_handle_udp_packets())
    loop.run_forever()
