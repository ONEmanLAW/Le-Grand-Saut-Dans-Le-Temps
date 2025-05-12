# ws_server.py

import asyncio
import websockets
import json

class WSServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.clients = {}  # client_name -> websocket
        self.host = host
        self.port = port

    async def handler(self, websocket):
        client_id = id(websocket)
        print(f"🟢 Nouveau client connecté: {client_id}")
        try:
            async for message in websocket:
                print(f"📩 Message reçu: {message}")  # Log pour voir ce qui est reçu
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    print("❌ Erreur JSON dans le message reçu")
                    await websocket.send(json.dumps({"status": "ERREUR_FORMAT_MESSAGE"}))
                    continue

                # Présentation du client
                if "client_name" in data:
                    client_name = data["client_name"]
                    # Si le client est déjà enregistré, on ne le réenregistre pas
                    if client_name not in self.clients:
                        self.clients[client_name] = websocket
                        print(f"✅ Client {client_name} enregistré")

                        # Réponse pour la présentation
                        response = {"status": "PRESENTATION_OK"}
                        await websocket.send(json.dumps(response))
                        print(f"✅ Message de présentation envoyé à {client_name}")
                    else:
                        print(f"⚠️ Client {client_name} déjà connecté.")

                elif "src" in data and "dest" in data:
                    dest = data["dest"]
                    if dest in self.clients:
                        payload = {
                            "src": data["src"],
                            "data": data["data"]
                        }
                        # Si le message vient du navigateur, on ajoute speak:true
                        if data["src"] == "browser" and dest == "raspberry":
                            payload["speak"] = True

                        await self.clients[dest].send(json.dumps(payload))
                        await websocket.send(json.dumps({"status": "MESSAGE_SEND"}))
                        print(f"📤 Message de {data['src']} envoyé à {dest}")
                    else:
                        print(f"⚠️ Destinataire {dest} non trouvé")
                        await websocket.send(json.dumps({"status": "DESTINATAIRE_NON_TROUVE"}))

        except websockets.exceptions.ConnectionClosed:
            print(f"🔴 Client {client_id} déconnecté")
            for name, ws in list(self.clients.items()):
                if ws == websocket:
                    del self.clients[name]
                    print(f"🛑 Client {name} supprimé des clients")

    async def start(self):
        print(f"🚀 Serveur WebSocket en écoute sur {self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port, max_size=None):
            await asyncio.Future()  # run forever

# Lancement du serveur
if __name__ == "__main__":
    # ws_server = WSServer(host="192.168.1.96", port=8080)  # chez moi
    # ws_server = WSServer(host="172.28.59.65", port=8080)   # Ecole
    ws_server = WSServer(host="192.168.208.50", port=8080) # Partage
    asyncio.run(ws_server.start())
