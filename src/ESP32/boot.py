import network
import time


#SSID = "Bbox-4EC72811"
#PASSWORD = "GRWchTt56FfkC2nsCM"

#SSID = "WIFI Pedagogie"
#PASSWORD = "8bcaud7d2h"

SSID = "POURSDFTKT"
PASSWORD = "CodePromo2004"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connection to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print("Waiting for connection")
    print("Connected to Wi-Fi :", wlan.ifconfig())
connect_wifi()
