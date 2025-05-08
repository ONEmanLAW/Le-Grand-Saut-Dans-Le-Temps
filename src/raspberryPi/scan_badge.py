from pirc522 import RFID
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

READERS = {
    "RFID_1": {"cs": 8, "rst": 25, "device": 0},
    "RFID_2": {"cs": 7, "rst": 27, "device": 1},
}

def init_reader(cs_pin, rst_pin, device_num):
    return RFID(bus=0, device=device_num, pin_rst=rst_pin, pin_ce=cs_pin, pin_irq=None, pin_mode=None)

def get_uid_str(rdr):
    (error, tag_type) = rdr.request()
    if error:
        return None
    (error, uid) = rdr.anticoll()
    if error:
        return None
    return "%02X%02X%02X%02X" % (uid[0], uid[1], uid[2], uid[3])

def main():
    print("👉 Approche un badge devant un des deux lecteurs...")

    readers = {
        label: init_reader(info["cs"], info["rst"], info["device"])
        for label, info in READERS.items()
    }

    last_uid = {label: None for label in readers}
    stable_count = {label: 0 for label in readers}
    removal_count = {label: 0 for label in readers}
    STABLE_THRESHOLD = 2  # nombre de lectures stables nécessaires

    try:
        while True:
            for label, rdr in readers.items():
                uid = get_uid_str(rdr)

                if uid:
                    if uid != last_uid[label]:
                        stable_count[label] = 1
                        last_uid[label] = uid
                    else:
                        stable_count[label] += 1

                    removal_count[label] = 0

                    if stable_count[label] == STABLE_THRESHOLD:
                        print(f"✅ Badge détecté : {uid} via {label}")
                else:
                    if last_uid[label]:
                        removal_count[label] += 1
                        if removal_count[label] == STABLE_THRESHOLD:
                            print(f"❌ Badge retiré de {label}. Attente d'un nouveau badge...")
                            last_uid[label] = None
                            stable_count[label] = 0
                    else:
                        stable_count[label] = 0

            time.sleep(0.2)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
