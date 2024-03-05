class Carte:
    def __init__(self, couleur, rang):
        self.couleur = couleur
        self.rang = rang

    def __str__(self):
        return f"{self.rang.value}{self.couleur.value}"

    def get_couleur(self):
        return self.couleur

    def get_rang(self):
        return self.rang

    def get_order(self):
        from paquet import RANG_ORDER
        return RANG_ORDER.get(self.rang, 1000)
