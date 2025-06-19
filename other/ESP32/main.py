from time import sleep_ms
from button import listen_for_button_presses 
from ws_client import ws_client  

def start_button_listener():
    listen_for_button_presses()

if __name__ == "__main__":

    start_button_listener()

    while True:
        sleep_ms(1000)  

