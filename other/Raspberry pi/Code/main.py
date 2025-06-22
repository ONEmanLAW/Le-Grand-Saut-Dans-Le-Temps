# main.py

import os
import sys
from time import sleep
from rfid_reader import RFIDReader


if "--restarted" not in sys.argv:
    print("♻️ Redémarrage pour initialisation complète...")
    os.execv(sys.executable, [sys.executable] + sys.argv + ["--restarted"])


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.append(script_dir)


READER_CONFIG = {
    "RFID_1": {"cs": 5,  "rst": 17},
    "RFID_2": {"cs": 6,  "rst": 27},
    "RFID_3": {"cs": 13, "rst": 22},
    "RFID_4": {"cs": 19, "rst": 23},
    "RFID_5": {"cs": 26, "rst": 24},
    "RFID_6": {"cs": 12, "rst": 25},
}

readers = {
    label: RFIDReader(label, **config)
    for label, config in READER_CONFIG.items()
}

print("📡 En attente de badges RFID...")


try:
    while True:
        for reader in readers.values():
            reader.tick()
            sleep(0.05)
        sleep(0.2)  
finally:
    import RPi.GPIO as GPIO
    GPIO.cleanup()
