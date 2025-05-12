import uwebsockets.client
import ujson
import time
import _thread

#SERVER_URL = "ws://192.168.1.96:8080" #Pour reseau chez moi
#SERVER_URL  = "ws://172.28.59.65:8080" # Reseau école
SERVER_URL  = "ws://192.168.208.50:8080" # Partage de connection


CLIENT_NAME = "esp32"
TARGET = "browser"

class WSClient:
    def __init__(self):
        self.ws = None
        self.connected = False
        self._lock = False 
        _thread.start_new_thread(self._maintain_connection, ())

    def _maintain_connection(self):
        while True:
            if not self.connected and not self._lock:
                self._lock = True
                self._connect()
                self._lock = False
            time.sleep(2)

    def _connect(self):
        try:
            print("🔌 Tentative de connexion au serveur WebSocket...")
            self.ws = uwebsockets.client.connect(SERVER_URL)
            print("✅ Connexion réussie au serveur WebSocket")
            self.ws.send(ujson.dumps({"client_name": CLIENT_NAME}))

            while True:
                try:
                    msg = self.ws.recv()
                    if msg:
                        print(f"📩 Message reçu: {msg}")
                        data = ujson.loads(msg)
                        if "status" in data and data["status"] == "PRESENTATION_OK":
                            print(f"✅ Le serveur a confirmé {CLIENT_NAME}")
                            self.connected = True
                        elif "status" in data and data["status"] == "ERREUR_FORMAT_MESSAGE":
                            print("❌ Erreur de format dans le message reçu")
                    time.sleep(0.1)
                except Exception as e:
                    print(f"❌ Erreur dans la réception du message: {e}")
                    self.connected = False
                    break

        except Exception as e:
            print(f"❌ Erreur de connexion WebSocket: {e}")
            self.connected = False
            try:
                if self.ws:
                    self.ws.close()
            except:
                pass
            self.ws = None

    def _send(self, message):
        if self.ws and self.connected:
            try:
                self.ws.send(ujson.dumps(message))
                print(f"📤 Message envoyé: {message['data']}")
            except Exception as e:
                print("⚠️ Erreur d'envoi, marquage comme déconnecté:", e)
                self.connected = False

    def send_button_press(self, button_id):
        """Envoie un message lorsque le bouton est pressé"""
        if button_id == 1:
            data = "A"
        elif button_id == 2:
            data = "B"
        elif button_id == 3:
            data = "C"
        elif button_id == 4:
            data = "D"
        else:
            return
        
        self._send({
            "src": CLIENT_NAME,
            "dest": TARGET,
            "data": data  
        })

ws_client = WSClient()

