# Projet Objet Connecté pour les EHPAD

## 📌 Contexte du projet

Dans le cadre de notre projet de fin d’année, nous avions eu **6 mois** pour concevoir un **objet connecté à destination des personnes âgées en EHPAD**.  
L’objectif principal était de créer une solution à la fois ludique, intuitive et bénéfique pour les résidents, en favorisant leur autonomie bien-être et la stimulation cognitive.

---

## 🧠 Concept

Notre projet repose sur **deux objets physiques principaux** :

- 📺 Une **télévision** qui va contenir la tablette pour l'affichage.
- 📱 Une **tablette** qui permet d'afficher le contenu.
- 🍓 Un **Raspberry Pi** connecté à des **capteurs**, et un **breadbord** permettant de choisir les époques.
- ⚡ Un **ESP32** installé sur une **breadboard**, qui sert à activer des buzzers et gérer le retour sonore.

Ces éléments sont interconnectés pour créer une **expérience immersive** à destination des résidents en EHPAD.

> ![Installation dans l'EHPAD](images/installation-ephad.jpg)

---

## 🔬 Méthodologie

Nous avons eu l'opportunité de faire **3 visites stratégiques dans un EHPAD Fondation du Parmelan** :

1. Une **visite d'observation** pour comprendre le quotidien des résidents et leurs besoins spécifiques.
2. Deux **visites de tests utilisateurs** avec notre prototype pour recueillir des retours terrain et ajuster notre produit.

Ces visites nous ont permis de prendre en compte :

- L’ergonomie (boutons larges, navigation simple)
- L’accessibilité (interface visuelle claire, peu de texte)
- Les attentes émotionnelles (souvenirs, nostalgie, plaisir d’écoute)

> ![Session de test](images/test-utilisateur.jpg)

---

## 🌐 Fonctionnement technique (1/2)

L’application web est développée avec **Vue.js**. Elle est hébergée localement et accessible sur le réseau interne via une **IP locale et un port spécifique**, ce qui permet à la tablette de s’y connecter automatiquement.

La **tablette Android** est configurée avec **Fully Kiosk Browser** pour :

- Démarrer directement l’application au démarrage
- Forcer le mode plein écran
- Empêcher toute sortie ou manipulation involontaire

> ![Tablette connectée](images/tablette-connectee.jpg)

## 🌐 Fonctionnement technique (2/2)

L’application utilise un réseau local :

- L'interface Vue.js est accessible à l'adresse : NETWORK : http://192.168.X.X:PORT

- Elle est consultée depuis la tablette grâce à **Fully Kiosk Browser**, configuré pour :
- Ouvrir l'URL automatiquement au démarrage
- Rester en plein écran sans barre de navigation
- Désactiver les interactions non prévues (tactile limité, verrouillage)

> 💡 Cette configuration permet une **expérience fluide et sans interruption** pour les résidents, même sans encadrement technique.

---

## 🔗 Accès à l'application

### 🛠️ Étapes de configuration

Avant de pouvoir utiliser l'application sur la tablette, il faut configurer correctement les **adresses IP** et les **ports** sur l'ensemble des éléments du projet.

---

### 1. 📥 Cloner le dépôt

Commencez par cloner ce dépôt sur votre machine :

```bash
git clone https://github.com/votre-utilisateur/projet-ephad.git
cd projet-ephad
```

### 2. ⚙️ Configurer le serveur WebSocket
Rendez-vous dans le fichier d'exemple suivant :
## ATTENTION il faut que tout les élements soit connécter au meme résaux (Peut avoir des promblème avec IOS, utiliser donc un routeur ou un android)

```
bash
Copier
Modifier
other/server/serverWbExample.py
Modifiez les lignes où apparaissent l'adresse IP et le port, par exemple :

python
Copier
Modifier
IP = "ip"
PORT = port
Ensuite, renommez le fichier en :

Copier
Modifier
serverWb.py
```
Ce fichier est celui que vous devrez exécuter pour lancer le serveur WebSocket Python qui fait le lien entre tous les appareils.

```bash
Copier
Modifier
mv other/server/serverWbExample.py other/server/serverWb.py
python3 other/server/serverWb.py
```

### 3. 💻 Modifier l'interface web (Vue.js)
Allez dans le fichier suivant :

```bash
Copier
Modifier
src/components/WebSocketClientExample.vue
Dans ce composant Vue.js, cherchez la ligne contenant l’URL WebSocket :

js
Copier
Modifier
const socket = new WebSocket("ws://IP:PORT"):
Modifiez l'adresse IP et le port selon votre configuration réseau.
Puis renommez le fichier en :

Copier
Modifier
WebSocketClient.vue
```

### 4. 📡 Configurer les clients Raspberry Pi et ESP32
Dans les scripts WebSocket des deux objets (capteurs et buzzers), il faut également définir la même IP et le même port que le serveur WebSocket.

### ⚡ ESP32 :

Ouvrir le fichier ws_client.ino (ou équivalent) dans le dossier :

```bash
Copier
Modifier
other/ESP32/
Modifier la ligne du WebSocket client pour correspondre à l’adresse IP/port du serveur :

cpp
Copier
Modifier
const char* ws_server = "ip";
const int ws_port = PORT;
```

### 🍓 Raspberry Pi :

Ouvrir le script Python du client WebSocket dans :

```bash
Copier
Modifier
other/RaspberryPi/
Modifier les valeurs IP et port dans le fichier (ex. ws_client.py) :

python
Copier
Modifier
IP = "IP"
PORT = PORT
Pour modifier et exécuter les scripts sur le Raspberry Pi, nous vous conseillons Thonny (simple et adapté pour ce type de projet).
```

✅ Connexion finale
Une fois toutes les IP et ports synchronisés :

Lancez le serveur WebSocket (serverWb.py)

Démarrez l’interface Vue.js sur la bonne ip et port

Allumez la tablette avec Fully Kiosk Browser pointé sur l'URL :

```bash
Copier
Modifier
http://ip:PORT
Branchez l’ESP32 et le Raspberry Pi avec leurs scripts respectifs


Le système est maintenant entièrement connecté en local et opérationnel !

yaml
Copier
Modifie
```

---

## 📷 Galerie du projet

Voici quelques photos de notre installation :

> ![Prototype général](images/prototype.jpg)  
> ![Montage Breadboard + ESP32](images/breadboard-esp32.jpg)  
> ![Tablette affichant l'application](images/interface-tablette.jpg)

---

## 📁 Structure du dépôt

```plaintext
📦 projet-ephad
├── src/
│   └── components/           # Composants Vue.js (interface utilisateur)
│       ├── WebSocketClientExample.vue
│       ├── ...
│       └── ...
│
└── other/
    ├── server/
    │   └── serverWb.py      # Serveur Python (communication réseau)
    │
    ├── ESP32/
    │   ├── main.py           # Code pour gérer les buzzers
    │   └── ...               # Autres fichiers liés à l'ESP32
    │
    └── RaspberryPi/
        ├── main.py           # Script pour les capteurs de sélection d’époque
        └── ...               # Autres scripts et config du Raspberry Pi


