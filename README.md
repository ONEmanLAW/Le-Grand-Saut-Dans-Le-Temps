# 🎵 Projet Objet Connecté pour les EHPAD

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

📱 Lien local à adapter : NETWORK : http://192.168.X.X:PORT

🌐 Lien web (si hébergé en ligne) : 

> ![Interface principale](images/interface-app.jpg)

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
│       ├── Home.vue
│       ├── ...
│       └── ...
│
└── other/
    ├── server/
    │   └── serverWeb.py      # Serveur Python (communication réseau)
    │
    ├── ESP32/
    │   ├── main.py           # Code pour gérer les buzzers
    │   └── ...               # Autres fichiers liés à l'ESP32
    │
    └── RaspberryPi/
        ├── main.py           # Script pour les capteurs de sélection d’époque
        └── ...               # Autres scripts et config du Raspberry Pi


