# rfid_reader.py

import time
import RPi.GPIO as GPIO
from pirc522 import RFID
from acceptor import Acceptor
from ws_client import ws_client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()  # Nettoyage au démarrage pour éviter les erreurs GPIO (ex: E2)

READERS = {
    "RFID_1": {"cs": 8, "rst": 25, "device": 0},
    "RFID_2": {"cs": 7, "rst": 27, "device": 1},
}

ALLOWED_UID = "33A7830E19"

class RFIDReader:
    def __init__(self, label, cs, rst, device):
        self.label = label
        self.rdr = RFID(bus=0, device=device, pin_rst=rst, pin_ce=cs, pin_irq=None, pin_mode=GPIO.BCM)
        self.allowed_uid = ALLOWED_UID
        self.badge_inserted = False
        self.badge_removed_ticks = 0
        self.last_read_success = 0
        self.long_scan_triggered = False

        self.long_scan = Acceptor(
            patterns=[[True] * 10],  # 5 secondes de présence continue
            accepted_callback=self.on_long_scan,
            refused_callback=self.on_scan_refused
        )

    def on_long_scan(self):
        print(f"✅ Long scan VALIDE avec badge autorisé sur {self.label} !")
        self.long_scan_triggered = True
        ws_client.send_long_scan(self.label)

    def on_scan_refused(self, seq):
        print(f"❌ Long scan échoué sur {self.label}. Séquence: {seq}")

    def read_uid(self):
        (error, tag_type) = self.rdr.request()
        if error:
            return None
        (error, uid) = self.rdr.anticoll()
        if error:
            return None
        return ''.join('{:02X}'.format(x) for x in uid)

    def listen(self):
        uid = self.read_uid()
        now = time.time()

        if uid:
            if uid == self.allowed_uid:
                if not self.badge_inserted:
                    print(f"🔍 Badge détecté sur {self.label} : {uid} ✅")
                self.badge_inserted = True
                self.badge_removed_ticks = 0
                self.last_read_success = now
                self.long_scan.update(True)
            else:
                print(f"⛔️ Mauvais badge détecté sur {self.label} : {uid}")
                self.long_scan.update(False)
        else:
            if self.badge_inserted and (now - self.last_read_success) < 2.0:
                print(f"⏳ Badge toujours présent sur {self.label} (lecture tolérée)")
                self.long_scan.update(True)
            else:
                if self.badge_inserted:
                    self.badge_removed_ticks += 1
                    if self.badge_removed_ticks >= 10:
                        if self.long_scan_triggered:
                            print(f"❌ Badge retiré de {self.label}. Envoi du message BADGE_REMOVED.")
                            ws_client.send_badge_removed(self.label)
                        else:
                            print(f"⚠️ Badge retiré de {self.label} sans long scan — aucun message envoyé.")
                        self.badge_inserted = False
                        self.badge_removed_ticks = 0
                        self.long_scan_triggered = False
                self.long_scan.update(False)


def main():
    readers = {
        label: RFIDReader(label, info["cs"], info["rst"], info["device"])
        for label, info in READERS.items()
    }

    print("📡 En attente de badges sur RFID_1 et RFID_2...")
    try:
        while True:
            for reader in readers.values():
                reader.listen()
            time.sleep(0.5)
    finally:
        GPIO.cleanup()
