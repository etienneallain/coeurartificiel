# Jeu des Coeurs - IA

Ce projet est une implémentation du jeu des Coeurs et de plusieurs intelligences artificielles. Le jeu comprend un client Flutter pour jouer contre l'IA et un serveur Python qui gère la logique de l'IA.

# Etapes d’installation

# Etape 1 : Clonage du projet

— Cloner le projet à partir de l’adresse suivante sur la branche main :
https://gitlab.insa-rennes.fr/projet coeur/hearts.git.

# Etape 2 : Lancement du serveur

— Naviguer vers le répertoire cloné, puis dans le dossier serveur.
— Ouvrir un terminal et exécuter la commande py coeurs_serveur.py. Cela lance le serveur.

# Etape 3 : Configuration de l’adresse IP du serveur

— Naviguer vers le répertoire cloné, puis dans le dossier serveur.
— Ouvrir le fichier "coeurs_serveur.py" et mettre l’IP souhaitée du serveur dans le main.
— Naviguer vers le répertoire cloné, puis dans le dossier client.
— Ouvrir le fichier "heart_game.dart" et mettre la bonne adresse IP du serveur dans la méthode
"card_to_play".
— Ouvrir le fichier "settingspage.dart" et mettre la bonne adresse IP du serveur dans la méthode "sendInitializationRequest()".

# Etape 4 : Lancement de l’application

Pour utiliser le format web :
— Naviguer vers le dossier client.
— Ouvrir un terminal et exécuter la commande "flutter run".
— Choisir le navigateur de votre choix lorsque cela vous est demandé. L’application se lance ensuite.
Pour utiliser le format mobile :
— Lancer Android Studio.
— Lancer l’émulateur Android.
— Lancer l’application, elle se lance automatiquement sur l'émulateur.

