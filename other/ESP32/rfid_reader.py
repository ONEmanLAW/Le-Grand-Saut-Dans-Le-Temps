from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
from acceptor import Acceptor

from ws_client import ws_client

class RFID:
    def __init__(self):
        # SPI config pour MFRC522
        self.sck = Pin(18, Pin.OUT)
        self.mosi = Pin(23, Pin.OUT)
        self.miso = Pin(19, Pin.OUT)
        self.spi = SPI(baudrate=1000000, polarity=0, phase=0,
                       sck=self.sck, mosi=self.mosi, miso=self.miso)
        self.sda = Pin(5, Pin.OUT)

        # lE BADGE autorisé autorisé
        self.allowed_uid = "33A7830E"

        self.long_scan = Acceptor(
            patterns=[[True] * 10],  # 10 ticks = 5s
            accepted_callback=self.on_long_scan,
            refused_callback=self.on_scan_refused
        )

        self.badge_inserted = False

        self.badge_removed_ticks = 0

    def on_long_scan(self):
        print("✅ Long scan validate CHACAL avec badge autorisé !")
        ws_client.send_long_scan()

    def on_scan_refused(self, seq):
        print("❌ Long scan échoué. Séquence:", seq)

    def read(self):
        rdr = MFRC522(self.spi, self.sda)
        uid = None
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
        return uid

    def listen(self):
        current_uid = self.read()

        if current_uid:
            print(f"🔍 Badge détecté: {current_uid}")
            if current_uid == self.allowed_uid:
                print("✅ Badge autorisé détecté")
                if not self.badge_inserted:
                   
                    self.badge_inserted = True
                    print("✅ Badge inséré pour la première fois.")
                
                self.badge_removed_ticks = 0
                self.long_scan.update(True)  
            else:
                print("⛔️ Mauvais badge ")
                self.long_scan.update(False)  
        else:
            print("❌ Pas de badge ")
           
           # pour debug
            if self.badge_inserted:
                self.badge_removed_ticks += 1
                if self.badge_removed_ticks >= 10:  # 5 secondes
                    print("❌ Badge retiré ")
                    self.send_badge_removed()
                    self.badge_removed_ticks = 0 
            self.long_scan.update(False)

    def send_badge_removed(self):
        """Envoie un message indiquant que le badge a été retiré"""
        print("❌ Badge retiré. Envoi du message BADGE_REMOVED.")
        ws_client.send_badge_removed()

