import pygame
from pygame.locals import *
import sys


# Initialisation de pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)

# Taille initiale de la fenêtre
BASE_WIDTH, BASE_HEIGHT = 800, 600

screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)


infoObject = pygame.display.Info()  # Définir infoObject ici


# Classe Ship
class Ship:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("player.png")
        self.x = x
        self.y = y
        self.bullets = []  # Liste pour stocker les lasers

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        for bullet in self.bullets:  # Dessinez tous les lasers
            bullet.draw()

    def move(self, dx):
        infoObject = pygame.display.Info()
        self.x += dx
        self.y = (infoObject.current_h - (infoObject.current_h)/20)-65
        if self.x > infoObject.current_w - 65:
            self.x = infoObject.current_w - 65
        if self.x < 0:
            self.x = 0

    def shot(self):
        bullet = Bullet(self)  # Créez un nouveau laser
        self.bullets.append(bullet)  # Ajoutez le laser à la liste

class Bullet:
    def __init__(self, ship): #J'initialise mon 'Bullet'
        self.sprite=pygame.image.load("bob4.svg") #Son sprite
        self.x=ship.x #Ses coordonées
        self.y=ship.y
        

    def draw(self):
        """
            Affichage du vaisseau
        """
        screen.blit(self.sprite,(self.x,self.y)) #Je place mon missile à sa position
        

class App:
    def __init__(self, speed=1):
        screen.blit(background, (0, 0))
        self.ship = Ship((infoObject.current_w / 2) , (infoObject.current_h - (infoObject.current_h / 20)-65))
        self.speed = speed
        self.pressed_keys = []  # Liste pour stocker les touches enfoncées

    def update(self, key_events):
        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.pressed_keys:  # Ajoutez la touche à la liste si elle n'y est pas déjà
                    self.pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:  # Supprimez la touche de la liste si elle y est
                    self.pressed_keys.remove(event.key)

        # Déplacez le vaisseau
        if pygame.K_LEFT in self.pressed_keys:
            self.ship.move(-1 * self.speed)
        if pygame.K_RIGHT in self.pressed_keys:
            self.ship.move(1 * self.speed)
        if pygame.K_SPACE in self.pressed_keys:
            self.ship.shot()

        # Mettez à jour la position de tous les lasers
        for bullet in self.ship.bullets:
            bullet.y -= 3 * self.speed

        # Supprimez les lasers qui ont quitté l'écran
        self.ship.bullets = [bullet for bullet in self.ship.bullets if bullet.y > -bullet.sprite.get_height()]

    def draw(self):
        screen.fill((255, 255, 255))  # J'efface l'écran précédent
        self.ship.draw()  # Je draw le vaisseau à sa nouvelle position
        for bullet in self.ship.bullets:  # Dessinez tous les lasers
            bullet.draw()
        pygame.display.flip()  # J'affiche tous les sprites

pygame.init() #Je crée l'interface pygame
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre

background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 

appli=App(2) #Je définie mon application, avec une valeur de vitesse

key_events = []  # Liste pour stocker les événements clavier

while True:  # Boucle principale du jeu

    for event in pygame.event.get():  # Récupère tous les événements pygame
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Stockez les événements clavier
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            key_events.append(event)

    # Mettez à jour et dessinez le jeu
    appli.update(key_events)
    appli.draw()
    
    key_events.clear()  # Nettoyez la liste des événements clavier après les avoir traités
