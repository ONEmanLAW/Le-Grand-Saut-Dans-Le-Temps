import uwebsockets.client
import ujson
import time
import _thread

SERVER_URL = "ws://192.168.1.96:8080"
CLIENT_NAME = "esp32"
TARGET = "browser"

class WSClient:
    def __init__(self):
        self.ws = None
        self.connected = False
        self._lock = False  # Pour éviter plusieurs connexions simultanées
        _thread.start_new_thread(self._maintain_connection, ())

    def _maintain_connection(self):
        """Thread séparé qui gère la connexion en boucle"""
        while True:
            if not self.connected and not self._lock:
                self._lock = True
                self._connect()
                self._lock = False
            time.sleep(2)  # Évite de spammer les tentatives de reconnexion

    def _connect(self):
        try:
            print("🔌 Connexion au serveur WebSocket...")
            self.ws = uwebsockets.client.connect(SERVER_URL)
            print("✅ Connecté au serveur WebSocket")
            self.ws.send(ujson.dumps({"client_name": CLIENT_NAME}))

            # Boucle de réception (bloquante tant que ça marche)
            while True:
                msg = self.ws.recv()
                if msg:
                    print(f"📩 Reçu: {msg}")
                    data = ujson.loads(msg)
                    if "status" in data and data["status"] == "PRESENTATION_OK":
                        print(f"✅ Le serveur a confirmé {CLIENT_NAME}")
                        self.connected = True
                time.sleep(0.1)

        except Exception as e:
            print("❌ Perte de connexion WebSocket:", e)
            self.connected = False
            try:
                if self.ws:
                    self.ws.close()
            except:
                pass
            self.ws = None

    def _send(self, message):
        """Envoie un message si connecté, sinon ignore"""
        if self.ws and self.connected:
            try:
                self.ws.send(ujson.dumps(message))
                print(f"📤 Message envoyé: {message['data']}")
            except Exception as e:
                print("⚠️ Erreur d'envoi, marquage comme déconnecté:", e)
                self.connected = False  # Forcer reconnexion

    def send_long_scan(self):
        self._send({
            "src": CLIENT_NAME,
            "dest": TARGET,
            "data": "LONG_SCAN_OK"
        })

    def send_badge_removed(self):
        self._send({
            "src": CLIENT_NAME,
            "dest": TARGET,
            "data": "BADGE_REMOVED"
        })

# Instance globale
ws_client = WSClient()

