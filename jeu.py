import itertools
import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


class ReseauJoueurIA(nn.Module):
    def __init__(self, input_size, output_size):
        super(ReseauJoueurIA, self).__init__()

        # Utilisation de nn.Sequential pour définir les couches en séquence
        self.couches = nn.Sequential(
            nn.Linear(input_size, 384),
            nn.ELU(),
            nn.Linear(384, 384),
            nn.ELU(),
            nn.Linear(384, 256),
            nn.ELU(),
            nn.Linear(256, 128),
            nn.ELU(),
            nn.Linear(128, 32),
            nn.Tanh()
        )

        # Couche de sortie
        self.sortie = nn.Linear(32, output_size)
        self.activation_sortie = nn.Softmax(dim=1)  # Softmax pour obtenir des probabilités

        # Définir requires_grad sur True pour tous les paramètres du modèle
        for param in self.parameters():
            param.requires_grad_()

    def forward(self, x):
        x = self.couches(x)
        x = self.sortie(x)
        x = self.activation_sortie(x)
        return x


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []
        self.nombre_coeurs = 0


class JoueurIA(Joueur):
    def __init__(self, nom, modele_reseau, optimizer):
        super().__init__(nom)
        self.modele_reseau = modele_reseau
        self.optimizer = optimizer

    def parameters(self):
        return self.modele_reseau.parameters()

    def choisir_carte(self, jeu, game_state):
        index_cartes_choisies = []
        max_main_joueur = 8
        while True:
            # Convertir l'état du jeu en un vecteur utilisable par le réseau de neurones
            input_vector = self.preparer_input_vector(game_state)

            # Convertir le vecteur en tenseur PyTorch
            input_tensor = torch.tensor(input_vector, dtype=torch.float).unsqueeze(0)

            # Passer le vecteur à travers le réseau de neurones
            output_tensor = self.modele_reseau(input_tensor)
            print(output_tensor)
            print(self.main)
            # Utiliser les probabilités de sortie du réseau pour prendre une décision
            proba_cartes = nn.functional.softmax(output_tensor, dim=1).squeeze().detach().numpy()
            print(proba_cartes)

            # Appliquer un masque pour ignorer les valeurs de padding
            mask = np.array(
                [1 if len(carte) > 1 else 0 for carte in self.main] + [0] * (max_main_joueur - len(self.main)))
            mask_2 = np.ones_like(proba_cartes)
            mask_2[index_cartes_choisies] = 0

            proba_cartes *= mask
            print(proba_cartes)
            proba_cartes *= mask_2
            print(proba_cartes)
            # Choisir la carte avec la probabilité la plus élevée
            carte_choisie_index = np.argmax(proba_cartes)
            print(carte_choisie_index)
            proba_max = proba_cartes[carte_choisie_index]
            carte_choisie = self.main[np.argmax(proba_cartes)]

            # Vérifier si le numero_pli > 1
            if game_state.numero_pli > 1:
                # Vérifier si la carte choisie est de la couleur demandée
                if carte_choisie[1] == game_state.couleur_demandee:
                    index_cartes_choisies.clear()
                    print(carte_choisie)
                    return carte_choisie, proba_max
                elif any(carte[1] == game_state.couleur_demandee for carte in self.main):
                    # Si le joueur a des cartes de la couleur demandée, sortir de la boucle
                    print(f"Le joueur {self.nom} a choisi une carte de mauvaise couleur. Refaites le choix.")
                    index_cartes_choisies.append(carte_choisie_index)
                else:
                    # Si le joueur n'a pas de cartes de la couleur demandée, sortir de la boucle
                    print(f"Le joueur {self.nom} n'a pas de cartes de la couleur demandée. Carte par défaut.")
                    index_cartes_choisies.clear()
                    return carte_choisie, proba_max  # Ou vous pouvez choisir une carte par défaut ici
            else:
                return carte_choisie, proba_max  # Si numero_pli <= 1, retourner la carte choisie sans vérification

    def preparer_input_vector(self, game_state):
        max_cartes_restantes = 24
        max_cartes_jouee = 3
        max_main_joueur = 8
        input_vector = [
            [game_state.numero_pli],
            self.encode_main(game_state.main_joueur, max_main_joueur),
            [game_state.coeurs_tombes],
            game_state.nombre_coeurs_joueurs,
            self.encode_couleur(game_state.couleur_demandee),
            self.encode_cartes_deja_jouees(game_state.cartes_deja_jouees, max_cartes_jouee),
            self.encode_cartes_restantes_autres_joueurs(game_state.cartes_restantes_autres_joueurs,
                                                        max_cartes_restantes),
        ]
        print("Input Vector:")
        print(input_vector)
        print(len(input_vector))

        def flatten_recursive(item):
            if isinstance(item, list):
                return [subitem for sublist in item for subitem in flatten_recursive(sublist)]
            else:
                return [item]

        flat_input_vector = flatten_recursive(input_vector)
        # Print statements for debugging
        print("Flat Input Vector:")
        print(flat_input_vector)
        print(len(flat_input_vector))
        return flat_input_vector

    def encode_main(self, main_joueur, max_size):
        print("main_joueur")
        print(main_joueur)
        # Encodage one-hot pour chaque carte dans la main
        encoded_main = [self.encode_carte(carte) for carte in main_joueur]
        while len(encoded_main) < max_size:
            encoded_main.append([0] * len(encoded_main[0]))
        return encoded_main

    def encode_carte(self, carte):
        # Encodage one-hot pour la couleur et la hauteur de la carte
        encoded_carte = self.encode_couleur(carte[1]) + self.encode_hauteur(carte[0])
        return encoded_carte

    def encode_couleur(self, couleur):
        # Encodage one-hot pour la couleur
        couleurs = ['Piques', 'Trèfles', 'Carreaux', 'Cœurs']
        encoded_couleur = [1 if couleur == c else 0 for c in couleurs]
        return encoded_couleur

    def encode_hauteur(self, hauteur):
        # Encodage one-hot pour la hauteur
        hauteurs = ['1', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi']
        encoded_hauteur = [1 if hauteur == h else 0 for h in hauteurs]
        return encoded_hauteur

    def encode_cartes_deja_jouees(self, cartes_deja_jouees, max_size):
        # Encodage one-hot pour chaque carte déjà jouée
        encoded_cartes_deja_jouees = [self.encode_carte(carte[0]) for carte in cartes_deja_jouees]

        # Fill with zeros to reach the maximum size
        while len(encoded_cartes_deja_jouees) < max_size:
            if encoded_cartes_deja_jouees:
                encoded_cartes_deja_jouees.append(
                    [0] * len(encoded_cartes_deja_jouees[0]))

            # Special case for initializing to three cards of zeros
            if not encoded_cartes_deja_jouees and max_size == 3:
                encoded_cartes_deja_jouees = [[0] * len(self.encode_carte([0, 0])) for _ in range(3)]

        return encoded_cartes_deja_jouees

    def encode_cartes_restantes_autres_joueurs(self, cartes_restantes_autres_joueurs, max_size):
        if len(cartes_restantes_autres_joueurs) > 0:
            # Encodage one-hot pour chaque carte restante des autres joueurs
            encoded_cartes_restantes = [self.encode_carte(carte) for carte in cartes_restantes_autres_joueurs]
            # Remplir avec des zéros pour atteindre la taille maximale
            while len(encoded_cartes_restantes) < max_size:
                encoded_cartes_restantes.append([0] * len(encoded_cartes_restantes[0]))
            return encoded_cartes_restantes
        elif len(cartes_restantes_autres_joueurs) == 0:
            # Si la liste est vide, créer un vecteur de zéros de la taille maximale
            return [[0] * 12] * max_size


class JeuDesCoeurs:
    def __init__(self):
        hauteurs = ['1', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi']
        couleurs = ['Piques', 'Trèfles', 'Carreaux', 'Cœurs']

        # Génération du paquet de cartes
        self.paquet = list(itertools.product(hauteurs, couleurs))

    def distribuer_cartes(self, nombre_cartes=8):
        # Vérifiez si la liste des cartes est vide et réinitialisez-la si nécessaire
        if not self.paquet:
            self.initialiser_paquet()

        # Distribuez le nombre spécifié de cartes de manière aléatoire
        cartes_distribuees = random.sample(self.paquet, nombre_cartes)

        # Retirez les cartes distribuées de la liste des cartes
        self.paquet = [carte for carte in self.paquet if carte not in cartes_distribuees]

        return cartes_distribuees

    def initialiser_paquet(self):
        hauteurs = ['1', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi']
        couleurs = ['Piques', 'Trèfles', 'Carreaux', 'Cœurs']
        self.paquet = list(itertools.product(hauteurs, couleurs))


class BarbuGameState:
    def __init__(self, jeu, joueurs):
        self.numero_pli = 0
        self.main_joueur = []
        self.coeurs_tombes = 0  # Durant le pli
        self.nombre_coeurs_joueurs = [0, 0, 0, 0]
        self.couleur_demandee = ""
        self.cartes_deja_jouees = []  # Durant un pli
        self.cartes_restantes_autres_joueurs = []
        self.jeu = jeu
        self.joueurs = joueurs
        self.dernier_joueur_gagnant = joueurs[0]
        self.points_joueur = 0

    def etat_jeu(self):
        return {
            'numero_pli': self.numero_pli,
            'main_joueur': self.main_joueur,
            'coeurs_tombes': self.coeurs_tombes,
            'nombre_coeurs_joueurs': self.nombre_coeurs_joueurs,
            'couleur_demandee': self.couleur_demandee,
            'cartes_deja_jouees': self.cartes_deja_jouees,
            'cartes_restantes_autres_joueurs': self.cartes_restantes_autres_joueurs
        }

    def demarrer_partie(self):
        self.numero_pli += 1
        if self.numero_pli == 1:
            for joueur in self.joueurs:
                joueur.main = self.jeu.distribuer_cartes()
                print(f"numero du {joueur.nom}")
                print(joueur.main)
            # Choisir une carte aléatoire du joueur d'index 0 pour déterminer la couleur demandée
            self.main_joueur = self.joueurs[0].main
            for joueur in self.joueurs:
                if joueur.main != self.main_joueur:
                    self.cartes_restantes_autres_joueurs.extend(joueur.main)
            print("carte restantes des autres joueurs à l'état initial")
            print(self.cartes_restantes_autres_joueurs)

    def simuler_partie(self):
        # Début d'un nouveau pli
        self.demarrer_partie()

        # Liste pour stocker les actions et les états du joueurIA
        actions_etats_joueurIA = []

        while self.numero_pli <= 8:  # Simulation de 8 plis

            index_joueur_gagnant = self.joueurs.index(self.dernier_joueur_gagnant) if self.numero_pli > 1 else 0
            joueur = self.joueurs[index_joueur_gagnant]

            # Si le joueur est le joueurIA
            if isinstance(joueur, JoueurIA):
                # Collecter l'état avant que le joueur agisse
                etat_actuel = self.etat_jeu()

                carte_choisie, proba_max = joueur.choisir_carte(self.jeu, self)
                couleur_choisie = carte_choisie[1]
                self.couleur_demandee = couleur_choisie
                print(f"Le joueur {joueur.nom} choisit la couleur : {self.couleur_demandee}")
                self.effectuer_action_joueur(carte_choisie, joueur)
                # Collecter l'action prise par le joueur
                action_joueur = carte_choisie
                # Ajouter l'action et l'état dans la liste
                actions_etats_joueurIA.append((etat_actuel, action_joueur, proba_max))
                # Créer la liste des joueurs excluant le dernier joueur gagnant
                joueurs1 = self.joueurs[index_joueur_gagnant + 1:] + self.joueurs[:index_joueur_gagnant]

                # Simulation des actions des joueurs (en commençant par le joueur suivant dans l'ordre initial)
                for joueur in joueurs1:
                    print(joueur.nom)
                    if isinstance(joueur, JoueurIA):
                        carte_choisie = joueur.choisir_carte(self.jeu, self)
                        self.effectuer_action_joueur(carte_choisie, joueur)
                    action_joueur = self.simuler_action_joueur(joueur)
                    self.effectuer_action_joueur(action_joueur, joueur)

            else:
                carte_choisie = random.choice(self.dernier_joueur_gagnant.main)
                couleur_choisie = carte_choisie[1]
                self.couleur_demandee = couleur_choisie
                print(f"Le joueur {self.dernier_joueur_gagnant.nom} choisit la couleur : {self.couleur_demandee}")
                self.effectuer_action_joueur(carte_choisie, self.joueurs[index_joueur_gagnant])
                # Créer la liste des joueurs excluant le dernier joueur gagnant
                joueurs1 = self.joueurs[index_joueur_gagnant + 1:] + self.joueurs[:index_joueur_gagnant]
                # Simulation des actions des joueurs (en commençant par le joueur suivant dans l'ordre initial)
                for joueur in joueurs1:
                    print(joueur.nom)
                    if isinstance(joueur, JoueurIA):
                        # Collecter l'état avant que le joueur agisse
                        etat_actuel = self.etat_jeu()
                        carte_choisie, proba_max = joueur.choisir_carte(self.jeu, self)
                        print("carte choisie de la fonction simu")
                        print(carte_choisie)
                        self.effectuer_action_joueur(carte_choisie, joueur)
                        # Collecter l'action prise par le joueur
                        action_joueur = carte_choisie
                        # Ajouter l'action et l'état dans la liste
                        actions_etats_joueurIA.append((etat_actuel, action_joueur, proba_max))
                    else:
                        action_joueur = self.simuler_action_joueur(joueur)
                        self.effectuer_action_joueur(action_joueur, joueur)
                # Fin du pli
            self.terminer_pli()
        # Retourner la liste d'actions et d'états du joueurIA
        return actions_etats_joueurIA

    def simuler_action_joueur(self, joueur):
        # Rechercher une carte de la couleur demandée dans la main du joueur
        cartes_couleur_demandee = [carte for carte in joueur.main if carte[1] == self.couleur_demandee]
        print(f"les cartes du{joueur.nom} de la même couleur demandée {self.couleur_demandee}")
        print(cartes_couleur_demandee)

        if cartes_couleur_demandee:
            # Choisir la première carte de la couleur demandée
            carte_choisie = cartes_couleur_demandee[0]
        else:
            # Choisir n'importe quelle carte de sa main
            carte_choisie = random.choice(joueur.main)
        print(f"carte choisie par le joueur {joueur.nom} :")
        print(carte_choisie)
        return carte_choisie

    def effectuer_action_joueur(self, action_joueur, joueur):
        # Retirer la carte de la main du joueur
        print(f"la main du {joueur.nom} qui va effectuer une action")
        print(joueur.main)
        joueur.main.remove(action_joueur)
        print(f"la main du {joueur.nom} qui a effectuer une action")
        print(joueur.main)

        # Ajouter la carte aux cartes déjà jouées
        self.cartes_deja_jouees.append((action_joueur, joueur))
        print("les cartes déjà jouées jusqu'à maintenant")
        print(self.cartes_deja_jouees)

        print("hola")
        # Retirer la carte de la liste des cartes restantes des autres joueurs
        if action_joueur in self.cartes_restantes_autres_joueurs:
            self.cartes_restantes_autres_joueurs.remove(action_joueur)

        # Vérifier si la carte est un cœur et incrémenter le nombre de cœurs tombés
        if action_joueur[1] == 'Cœurs':
            self.coeurs_tombes += 1

        print("hola")

    def terminer_pli(self):

        # Récupérer la couleur demandée pour ce pli
        couleur_demandee = self.couleur_demandee

        # Récupérer les cartes jouées dans la couleur demandée
        cartes_couleur_demandee = [carte for carte in self.cartes_deja_jouees if carte[0][1] == couleur_demandee]
        print(f"Toutes les cartes de la couleur demandée à la fin du pli {self.numero_pli} :")
        print(cartes_couleur_demandee)

        # Fonction pour obtenir la valeur d'une carte dans l'ordre croissant des hauteurs
        def valeur_carte(carte):
            hauteurs = ['7', '8', '9', '10', 'Valet', 'Dame', 'Roi', '1']
            return hauteurs.index(carte[0])

        # Trouver la carte la plus haute parmi celles jouées
        carte_plus_haute = max(cartes_couleur_demandee, key=lambda x: valeur_carte(x[0]))
        print(f"La carte la plus haute du pli {self.numero_pli}")
        print(carte_plus_haute)

        # Trouver le joueur ayant joué la carte la plus haute
        joueur_gagnant = carte_plus_haute[1]
        print(f"joueur remportant le pli {self.numero_pli}")
        print(joueur_gagnant)
        # Incrémenter le nombre de cœurs du joueur gagnant par le nombre de cœurs tombés
        self.nombre_coeurs_joueurs[self.joueurs.index(joueur_gagnant)] += self.coeurs_tombes
        print(f"nombre de coeurs par joueurs du pli {self.numero_pli}")
        print(self.nombre_coeurs_joueurs)

        # Réinitialiser les valeurs pour le pli suivant
        self.cartes_deja_jouees = []
        self.coeurs_tombes = 0
        self.couleur_demandee = ""
        self.dernier_joueur_gagnant = joueur_gagnant
        print(self.dernier_joueur_gagnant.nom)

        if self.numero_pli < 8:
            self.demarrer_partie()
        else:
            print(game_state.etat_jeu())
            points = self.calculer_points()
            print(points)
            print(self.points_joueur)
            self.demarrer_partie()

    def calculer_points(self):
        points_joueurs = []
        for nombre_coeurs in self.nombre_coeurs_joueurs:
            points = -5 * nombre_coeurs  # Chaque coeur vaut -5 points
            if nombre_coeurs == 8:  # Si le joueur a tous les coeurs, bonus de +40 points
                points = 40
            points_joueurs.append(points)
        self.points_joueur = points_joueurs[0]
        print(self.points_joueur)
        print(points_joueurs)
        return points_joueurs


class Entrainement:

    def __init__(self, jeu, joueur_ia, joueur_ia_cible):
        self.jeu = jeu
        self.joueur_ia = joueur_ia
        self.joueur_ia_cible = joueur_ia_cible
        self.actions_etats = []
        self.predict_q_values = []
        self.real_q_values = []
        self.normalized_q_values =[]
        self.points = []
        self.reward = 0
        self.gamma = 1
        self.var = 0
        self.lr = 0.1
        # self.optimizer = optim.Adam(modele_reseau.parameters(), self.lr)
        self.loss_function = torch.nn.MSELoss()
        self.loss = 0.0
        self.predict_q_tensor = []
        self.real_q_tensor = []
        self.returns = []

    def collecter_actions_etats(self, actions_etats_joueurIA):
        self.actions_etats = actions_etats_joueurIA
        print(len(self.actions_etats))

    # def loss_function(self):
    #     # Calcul de l'erreur quadratique moyenne (MSE) entre les valeurs Q prédites et les valeurs Q réelles
    #     if len(self.predict_q_values) > 0 and len(self.real_q_values) > 0:
    #         predict_q_tensor = torch.tensor(self.predict_q_values, requires_grad=True)
    #         real_q_tensor = torch.tensor(self.real_q_values, requires_grad=True)
    #         mse = self.loss_function(predict_q_tensor, real_q_tensor)
    #         print(mse)
    #         return mse
    #     else:
    #         return torch.tensor(0.0)  # Si les listes sont vides, retourner un tenseur avec une perte nulle

    def calculer_recompense(self, points_joueurs):
        self.points = points_joueurs

        recompense = 0

        if self.points[0] == 0:
            recompense = 0
        if self.points[0] == 40:
            recompense = 40
        if self.points[0] < 0:
            recompense = self.points[0]

        return recompense

    def compute_returns(self, points_joueurs):
        self.reward = self.calculer_recompense(points_joueurs)
        # La récompense totale obtenue à la fin de l'épisode est déjà connue (self.reward)
        # et tu souhaites attribuer cette récompense de façon équitable à chaque action.

        # Initialiser les retours pour chaque action à 0
        self.returns = [0 for _ in range(len(self.actions_etats))]  # Assure la même taille que actions_etats

        # Calculer les retours pour chaque action, en partant de la fin
        G = 0  # Valeur initiale du retour
        for t in range(len(self.actions_etats) - 1, -1, -1):
            # Pour une approche Monte Carlo, on commence par la fin et on remonte.
            # La récompense est divisée également, donc cette approche spécifique peut être ajustée selon le besoin.
            # Dans ton cas, chaque action reçoit une partie de la récompense totale.
            G = self.reward / len(
                self.actions_etats) + self.gamma * G  # Mise à jour de G pour inclure la récompense et le discount
            self.returns[t] = G  # Stocker le retour calculé pour cette action

        print("LONGUEUR DE RETURNS")
        print(len(self.returns))
        print(self.returns)

    def entrainer_modele(self, points_joueurs):
        self.compute_returns(points_joueurs)
        print(self.reward)

        # Parcours de chaque état/action dans la liste
        for etat_actuel, action, proba_max in self.actions_etats:
            self.predict_q_values.append(proba_max)
            print(self.predict_q_values)

        for etat in self.actions_etats:
            print(etat)
            self.var = self.var + 1
            print(self.var)
            if self.var <= 8:
                real_qvalue = self.predict_q_values[self.var - 1] + self.gamma * (
                            self.returns[self.var - 1] - self.predict_q_values[self.var - 1])
                self.real_q_values.append(real_qvalue)
            # if self.var == 8:
            #     real_qvalue = (self.reward / 8) + self.gamma * 0
            #     self.real_q_values.append(real_qvalue)

        # Conversion des listes en tenseurs PyTorch
        self.predict_q_tensor = torch.tensor(self.predict_q_values, dtype=torch.float32, requires_grad=True)
        self.real_q_tensor = torch.tensor(self.real_q_values, dtype=torch.float32, requires_grad=True)

        self.loss = self.loss_function(self.predict_q_tensor, self.real_q_tensor)
        return self.loss

    def mise_à_jour_réseau(self, joueur_ia_cible=False):
        if joueur_ia_cible:
            network = self.joueur_ia_cible

        # Rétropropagation (backpropagation)
        network.optimizer.zero_grad()
        self.loss.backward()

        # Mise à jour des paramètres du modèle
        network.optimizer.step()


# création des joueurs
joueur1 = Joueur("joueur 1")
joueur2 = Joueur("joueur 2")
joueur3 = Joueur("joueur 3")
joueur4 = Joueur("joueur 4")

modele_reseau = ReseauJoueurIA(input_size=430, output_size=8)
optimizer = optim.Adam(modele_reseau.parameters(), lr=0.1)
joueur_ia = JoueurIA("JoueurIA", modele_reseau, optimizer)
joueur_ia_cible = JoueurIA("JoueurIA_cible", modele_reseau, optimizer)

# Création de la liste des joueurs avec le réseau d'évaluation pour commencer
joueurs = [joueur_ia, joueur2, joueur3, joueur4]

# Création de l'objet jeu_des_coeurs
jeu_des_coeurs = JeuDesCoeurs()

pertes = []
nb_episodes = 100
update_frequency = 5  # Fréquence de changement entre joueur_ia et joueur_ia_cible

# Boucle d'entraînement
for episode in range(nb_episodes):
    game_state = BarbuGameState(jeu_des_coeurs, joueurs)

    entrainement = Entrainement(jeu_des_coeurs, joueur_ia, joueur_ia_cible)

    # Mettez à jour les poids du réseau d'évaluation (joueur_ia) avec les poids du réseau cible (joueur_ia_cible)
    if (episode + 1) % update_frequency == 0:
        joueur_ia.modele_reseau.load_state_dict(joueur_ia_cible.modele_reseau.state_dict())

    actions_etats = game_state.simuler_partie()

    entrainement.collecter_actions_etats(actions_etats)

    perte = entrainement.entrainer_modele(game_state.calculer_points())
    entrainement.mise_à_jour_réseau(joueur_ia_cible)
    pertes.append(perte.item())

print(pertes)

plt.plot(pertes)
plt.xlabel('Épisode')
plt.ylabel('Perte (%)')
plt.title('Évolution de la perte pendant l\'entraînement')
plt.show()

# Un problème changement de la taille du vecteur d'entrée, car les cartes_restantes_joueurs diminue
# au fur et à mesure des plis à résoudre avec du zero padding
# Deux réseaux de neurones le premier d'évaluation est mis à jour chaque X ép et c'est toujours
# le Rcible qui est mis à jour. Je continue d'utiliser le réseau d'évaluation pour prédire mes Qvaleurs.
# Utiliser le MonteCarlo pour les mises à jour des Qvaleurs prédites.
