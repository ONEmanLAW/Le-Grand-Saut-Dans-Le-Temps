# rfid_reader.py

import time
import RPi.GPIO as GPIO
from pirc522 import RFID
from acceptor import Acceptor
from ws_client import ws_client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ALLOWED_UID = "33A7830E19"

class RFIDReader:
    def __init__(self, label, cs, rst, device=0):
        self.label = label
        self.reader = RFID(bus=0, device=device, pin_rst=rst, pin_ce=cs, pin_irq=None, pin_mode=GPIO.BCM)
        self.allowed_uid = ALLOWED_UID
        self.badge_present = False
        self.last_seen = 0
        self.long_scan_triggered = False

        self.long_scan = Acceptor(
            patterns=[[True] * 5],  # 5s (10 x 0.5s)
            accepted_callback=self.on_long_scan,
            refused_callback=self.on_scan_refused
        )

    def on_long_scan(self):
        print(f"✅ Long scan autorisé sur {self.label}")
        self.long_scan_triggered = True
        ws_client.send_long_scan(self.label)

    def on_scan_refused(self, seq):
        print(f"❌ Long scan refusé sur {self.label}. Séquence : {seq}")

    def read_uid(self):
        err, _ = self.reader.request()
        if err:
            return None
        err, uid = self.reader.anticoll()
        if err:
            return None
        return ''.join(f"{x:02X}" for x in uid)

    def tick(self):
        now = time.time()
        uid = self.read_uid()

        if uid == self.allowed_uid:
            if not self.badge_present:
                print(f"🔍 Badge détecté sur {self.label} : {uid}")
            self.badge_present = True
            self.last_seen = now
            self.long_scan.update(True)

        elif uid:
            print(f"⛔️ Mauvais badge sur {self.label} : {uid}")
            self.long_scan.update(False)

        else:
            if self.badge_present and (now - self.last_seen) < 2.0:
                print(f"⏳ Badge encore détecté (tolérance) sur {self.label}")
                self.long_scan.update(True)
            elif self.badge_present:
                print(f" Badge retiré sur {self.label}")
                self.badge_present = False
                self.long_scan_triggered = False
                self.long_scan.update(False)
            else:
                self.long_scan.update(False)

