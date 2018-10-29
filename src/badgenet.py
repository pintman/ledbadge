''' 
Network two badges. Idea: The first that is turned, scans for SSIDs of other
boards (e.g. ledbadge_server). If none are present, act as server. Otherwise
connect to the (first) server that is found. 
'''
import network
import usocket as socket
import time

import utaskmanager

SERVER_SSID = 'ledbadge_server'
SERVER_PASS = 'ledbadge_server'
SERVER_IP = '192.168.4.1'
SERVER_PORT = 1011
MAX_PACKET_SIZE = 1024  # bytes
WAIT_TIME_TIL_CONNECTION = 5  # seconds


def discover_server_ssid():
    '''
    Scan for any servers. If connection to a server was possible, return
    the tuple from network.WLAN.ifconfig (ip, subnet, gateway, dns). If no 
    server was found, return None.

    http://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.ifconfig
    '''
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active()
    print('Trying to connect to a server')
    sta_if.connect(SERVER_PASS, SERVER_PASS)
    time.sleep(WAIT_TIME_TIL_CONNECTION)
    if sta_if.isconnected():
        return sta_if.ifconfig()
    else:
        return None


class BadgeNetServer(utaskmanager.Task):
    def __init__(self, ip, port):
        super().__init__()
        # connect to server
        self.ip = ip
        self.port = port
        self.clients = []  # list of client ip addresses
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init_socket()

    def _init_socket(self):
        self.sock.setblocking(False)
        self.sock.bind(self.ip, self.port)
        self.sock.listen(1)

    def task_step(self):
        # check for incoming connection
        # if register packet: register client, sent client id to new client
        # sent to all clients        
        conn, addr = socket.accept()  # TODO handle exceptions?

        if addr not in self.clients:
            print("Registering new client", addr)
            self.clients.append(addr)
            response = str(len(self.clients)-1)
        else:
            b_data = conn.recv(MAX_PACKET_SIZE)
            response = self._handle_request(str(b_data, 'ascii'))

        conn.sendall(bytes(response, 'ascii'))

    def _handle_request(self, request):
        return 'got ' + request


class BadgeNetClient(utaskmanager.Task):
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.register()

    def task_step(self):
        ''

    def register(self):
        'Register at the server and return an id.'
        return -1


def start_server():
    '''
    Start Server and act as access point for other badges.
    '''
    print("Acting as access point ", SERVER_SSID)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config('essid', SERVER_SSID)
    ap_if.config('password', SERVER_PASS)
    ap_if.active(True)

    bns = BadgeNetServer(SERVER_IP, SERVER_PORT)
    utaskmanager.add_task(bns)


def start():
    ip_subnet_gw_dns = discover_server_ssid()
    if ip_subnet_gw_dns is None:
        print("No BadgeNetServer found, starting one.")
        start_server()

    bnc = BadgeNetClient(SERVER_IP, SERVER_PORT)
    bnid = bnc.register()
    print("Registered at BadgeNetServer with bnid", bnid)
