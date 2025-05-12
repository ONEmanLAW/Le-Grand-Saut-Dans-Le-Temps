from time import sleep_ms
from button import listen_for_button_presses  # Importation du fichier button.py pour écouter les boutons
from ws_client import ws_client  # Importation du fichier ws_client.py pour gérer la connexion WebSocket

# Lancer l'écoute des boutons dans un thread séparé
def start_button_listener():
    listen_for_button_presses()

if __name__ == "__main__":
    # Démarre l'écoute des boutons
    start_button_listener()

    # Ce programme reste en fonctionnement, écoute les boutons et gère la connexion WebSocket
    while True:
        sleep_ms(1000)  # Attente dans la boucle principale (nous pourrions ajouter d'autres tâches ici)

