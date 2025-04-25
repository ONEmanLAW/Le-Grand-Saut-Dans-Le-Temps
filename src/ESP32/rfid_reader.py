from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
from acceptor import Acceptor

from ws_client import ws_client  # Importer le client WebSocket

class RFID:
    def __init__(self):
        # SPI config pour MFRC522
        self.sck = Pin(18, Pin.OUT)
        self.mosi = Pin(23, Pin.OUT)
        self.miso = Pin(19, Pin.OUT)
        self.spi = SPI(baudrate=1000000, polarity=0, phase=0,
                       sck=self.sck, mosi=self.mosi, miso=self.miso)
        self.sda = Pin(5, Pin.OUT)

        # UID autorisé
        self.allowed_uid = "33A7830E"

        # Initialisation de l'accepteur de long scan
        self.long_scan = Acceptor(
            patterns=[[True] * 10],  # 10 ticks = 5s
            accepted_callback=self.on_long_scan,
            refused_callback=self.on_scan_refused
        )

        # État pour savoir si un badge a été inséré au moins une fois
        self.badge_inserted = False

        # Compteur pour le nombre de ticks sans badge
        self.badge_removed_ticks = 0

    def on_long_scan(self):
        """Callback appelé lorsqu'un long scan est valide"""
        print("✅ Long scan VALIDE avec badge autorisé !")
        # Envoyer le message de long scan après la validation
        ws_client.send_long_scan()

    def on_scan_refused(self, seq):
        """Callback appelé si le long scan échoue"""
        print("❌ Long scan échoué. Séquence:", seq)

    def read(self):
        """Lecture du badge RFID"""
        rdr = MFRC522(self.spi, self.sda)
        uid = None
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
        return uid

    def listen(self):
        """Écoute continue des badges RFID"""
        current_uid = self.read()

        if current_uid:
            print(f"🔍 Badge détecté: {current_uid}")
            if current_uid == self.allowed_uid:
                print("✅ Badge autorisé détecté")
                if not self.badge_inserted:
                    # Premier scan du badge, on marque qu'il a été inséré
                    self.badge_inserted = True
                    print("✅ Badge inséré pour la première fois.")
                
                # Réinitialiser le compteur de ticks si le badge est inséré
                self.badge_removed_ticks = 0
                self.long_scan.update(True)  # Si le badge est autorisé, tenter un long scan
            else:
                print("⛔️ Mauvais badge, refusé.")
                self.long_scan.update(False)  # Si le badge est incorrect, refuse le long scan
        else:
            print("❌ Aucun badge détecté")
            # Si aucun badge n'est détecté et que le badge a été inséré au moins une fois
            if self.badge_inserted:
                # Incrémenter le compteur de ticks pour détecter l'absence du badge
                self.badge_removed_ticks += 1
                if self.badge_removed_ticks >= 10:  # Si 10 ticks (5 secondes) se sont écoulés
                    print("❌ Badge retiré après 5 secondes.")
                    self.send_badge_removed()
                    self.badge_removed_ticks = 0  # Réinitialiser le compteur de ticks
            self.long_scan.update(False)  # Aucun badge, refuse le long scan

    def send_badge_removed(self):
        """Envoie un message indiquant que le badge a été retiré"""
        print("❌ Badge retiré. Envoi du message BADGE_REMOVED.")
        ws_client.send_badge_removed()

