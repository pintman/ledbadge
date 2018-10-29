# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import config
#import webrepl
#webrepl.start()
gc.collect()

# import text early on due to memory fragmentation
# https://forum.micropython.org/viewtopic.php?p=28225&sid=3c4da4dea626437868dbbc8847133d97#p28225
import text

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.SSID, config.PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect()

#print('Starting network joystick')
#import network_joystick
#network_joystick.main()

#import snake
#snake.main()

#import firmware
#firmware.start()

import main
main.main()
