from machine import Pin
import time
from ws_client import ws_client  

button_pin_1 = Pin(19, Pin.IN, Pin.PULL_UP)  # Bouton A
button_pin_2 = Pin(18, Pin.IN, Pin.PULL_UP)   # Bouton B
button_pin_3 = Pin(4, Pin.IN, Pin.PULL_UP)  ## Bouton C
button_pin_4 = Pin(23, Pin.IN, Pin.PULL_UP)  # Bouton D

button_1_pressed = False
button_2_pressed = False
button_3_pressed = False
button_4_pressed = False

def listen_for_button_presses():
    global button_1_pressed, button_2_pressed, button_3_pressed, button_4_pressed

    while True:
        # Bouton A
        if button_pin_1.value() == 0 and not button_1_pressed:
            print("Bouton A pressé")
            ws_client.send_button_press(1)
            button_1_pressed = True
            time.sleep(0.2)
        elif button_pin_1.value() == 1:
            button_1_pressed = False

        # Bouton B
        if button_pin_2.value() == 0 and not button_2_pressed:
            print("Bouton B pressé")
            ws_client.send_button_press(2)
            button_2_pressed = True
            time.sleep(0.2)
        elif button_pin_2.value() == 1:
            button_2_pressed = False

        # Bouton C
        if button_pin_3.value() == 0 and not button_3_pressed:
            print("Bouton C pressé")
            ws_client.send_button_press(3)
            button_3_pressed = True
            time.sleep(0.2)
        elif button_pin_3.value() == 1:
            button_3_pressed = False

        # Bouton D
        if button_pin_4.value() == 0 and not button_4_pressed:
            print("Bouton D pressé")
            ws_client.send_button_press(4)
            button_4_pressed = True
            time.sleep(0.2)
        elif button_pin_4.value() == 1:
            button_4_pressed = False

        time.sleep(0.01)

