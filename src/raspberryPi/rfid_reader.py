import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.cleanup()

from acceptor import Acceptor
from ws_client import ws_client
from pirc522 import RFID
from time import sleep

class RFIDReader:
    def __init__(self):
        self.rdr = RFID(pin_irq=None)
        self.allowed_uid = "33A7830E19"
        self.badge_inserted = False
        self.badge_removed_ticks = 0
        self.last_read_success = 0

        self.long_scan = Acceptor(
            patterns=[[True] * 10],  # 10 ticks = 5s
            accepted_callback=self.on_long_scan,
            refused_callback=self.on_scan_refused
        )

    def on_long_scan(self):
        print("✅ Long scan VALIDE avec badge autorisé !")
        ws_client.send_long_scan()

    def on_scan_refused(self, seq):
        print("❌ Long scan échoué. Séquence:", seq)

    def read(self):
        (error, tag_type) = self.rdr.request()
        if not error:
            (error, uid) = self.rdr.anticoll()
            if not error:
                return ''.join('{:02X}'.format(x) for x in uid)
        return None

    def listen(self):
        current_uid = self.read()
        now = time.time()

        if current_uid:
            if current_uid == self.allowed_uid:
                print(f"🔍 Badge détecté: {current_uid} ✅")
                if not self.badge_inserted:
                    self.badge_inserted = True
                    print("✅ Badge inséré pour la première fois.")
                self.badge_removed_ticks = 0
                self.last_read_success = now
                self.long_scan.update(True)
            else:
                print(f"⛔️ Mauvais badge détecté: {current_uid}")
                self.long_scan.update(False)
        else:
            if self.badge_inserted and (now - self.last_read_success) < 2.0:
                # 😎 Tolérer erreurs pendant 2 secondes
                print("⏳ Pas lu, mais toléré (badge toujours présent)")
                self.long_scan.update(True)
            else:
                print("❌ Aucun badge détecté (réel)")
                if self.badge_inserted:
                    self.badge_removed_ticks += 1
                    if self.badge_removed_ticks >= 10:
                        print("❌ Badge retiré après 5 secondes.")
                        self.send_badge_removed()
                        self.badge_removed_ticks = 0
                        self.badge_inserted = False
                self.long_scan.update(False)

    def send_badge_removed(self):
        print("❌ Badge retiré. Envoi du message BADGE_REMOVED.")
        ws_client.send_badge_removed()
