from time import sleep_ms
from rfid_reader import RFID
from ws_client import ws_client  # pour init la connexion

rfid_reader = RFID()

while True:
    rfid_reader.listen()
    sleep_ms(500)

