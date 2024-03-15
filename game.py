import pyxel

class Ship:
    """
        Vaisseau principal
    """
    def __init__(self, x, y):
        """
            Caractéristiques du vaisseau.
            C'est un carré dans un premier temps.
        """
        self.x = x
        self.y = y
        self.taille = 8

    def draw(self):
        """
            Affichage du vaisseau
        """
        decal = self.taille // 2
        pyxel.rectb(self.x - decal, self.y - decal, self.taille, self.taille, 7)

    def move(self, dx, dy):
        """
            Déplacement du vaisseau
        """
        self.x += dx
        self.y += dy


class App:
    def __init__(self):
        """
            Initialisation de la fenêtre et des éléments
        """
        # Fenêtre de 120 par 200 pyxels
        pyxel.init(120, 200)
        # Vaisseau en (60,180)
        self.ship = Ship(60,180)
        # On lance le moteur du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        """
            Mise à jour des positions et des états.
            Pas d'affichage ici !
        """
        # Déplacement à droite
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.move(1,0)

    def draw(self):
        """
            On affiche les éléments
        """
        # On rempli le fond avec une couleur
        pyxel.cls(0)
        # On affiche le vaisseau
        self.ship.draw()


App()

