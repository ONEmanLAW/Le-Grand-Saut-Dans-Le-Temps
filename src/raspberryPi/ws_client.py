# ws_client.py

import websocket
import json
import threading
import time

SERVER_URL = "ws://192.168.1.96:8080"
CLIENT_NAME = "raspberry"
TARGET = "browser"

class WSClient:
    def __init__(self):
        self.ws = None
        self.connected = False
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._maintain_connection)
        self.thread.start()

    def _maintain_connection(self):
        while True:
            if not self.connected:
                self._connect()
            time.sleep(2)

    def _connect(self):
        try:
            print("🔌 Connexion au serveur WebSocket...")
            self.ws = websocket.create_connection(SERVER_URL)
            self.connected = True
            print("✅ Connecté au serveur WebSocket")
            self.send({"client_name": CLIENT_NAME})

            while True:
                msg = self.ws.recv()
                if msg:
                    print(f"📩 Reçu: {msg}")
                    data = json.loads(msg)
                    if "status" in data and data["status"] == "PRESENTATION_OK":
                        print(f"✅ Le serveur a confirmé {CLIENT_NAME}")
                time.sleep(0.1)

        except Exception as e:
            print("❌ Erreur WebSocket:", e)
            self.connected = False
            if self.ws:
                try:
                    self.ws.close()
                except:
                    pass
            self.ws = None

    def send(self, message):
        if self.connected and self.ws:
            try:
                self.ws.send(json.dumps(message))
                print(f"📤 Message envoyé: {message}")
            except Exception as e:
                print("⚠️ Erreur d'envoi:", e)
                self.connected = False

    def send_long_scan(self, reader_label):
        self.send({
            "src": CLIENT_NAME,
            "dest": TARGET,
            "data": f"LONG_SCAN_OK_{reader_label}"
        })

    def send_badge_removed(self, reader_label):
        self.send({
            "src": CLIENT_NAME,
            "dest": TARGET,
            "data": f"BADGE_REMOVED_{reader_label}"
        })

# Instance globale
ws_client = WSClient()
