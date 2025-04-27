from pirc522 import RFID
import time

def main():
    rdr = RFID(pin_irq=None)  # Important de désactiver IRQ sur Raspberry Pi

    print("👉 Approche ton badge devant le lecteur...")

    while True:
        (error, tag_type) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            if not error:
                uid_str = "%02X%02X%02X%02X" % (uid[0], uid[1], uid[2], uid[3])
                print(f"✅ Badge détecté : {uid_str}")
                time.sleep(2)  # Petite pause pour ne pas spammer
            else:
                print("⚠️ Erreur lecture UID")
        time.sleep(0.2)  # Attend un peu avant de relire

if __name__ == "__main__":
    main()