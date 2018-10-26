''' 
Network two badges. Idea: The first that is turned, scans for SSIDs of other
boards (e.g. ledbadge_server). If none are present, act as server. Otherwise
connect to the (first) server that is found. 
'''
import network
import time

SERVER_SSID = 'ledbadge_server'
SERVER_PASS = 'ledbadge_server'
WAIT_TIME_TIL_CONNECTION = 5  # seconds


def discover_server():
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

def start_server():
    '''
    Start Server and act as access point for other badges.
    '''
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config('essid', SERVER_SSID)
    ap_if.config('password', SERVER_PASS)
    ap_if.active(True)
