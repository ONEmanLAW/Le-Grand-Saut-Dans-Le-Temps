from rfid_reader import RFIDReader
from time import sleep

rfid_reader = RFIDReader()

while True:
    rfid_reader.listen()
    sleep(0.5)  # 500ms entre chaque écoute
