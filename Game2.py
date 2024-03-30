import pygame
from pygame.locals import *
import sys
import time

# Définition des couleurs
WHITE = (255, 255, 255)

# Taille initiale de la fenêtre
BASE_WIDTH, BASE_HEIGHT = 800, 600

screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)


infoObject = pygame.display.Info()  # Définir infoObject ici

class Ship:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("player.png")
        self.rect= self.sprite.get_rect(x=x, y=y)
        self.speed=1
        self.velocity=[0,0]
        self.bullets=[]

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect)

    def shot(self):
        x=self.rect.x
        y=self.rect.y
        bullet = Bullet(self,x, y)  # Créez un nouveau laser
        self.bullets.append(bullet)  # Ajoutez le laser à la liste

class Bullet:
    def __init__(self, ship, x, y): #J'initialise mon 'Bullet'
        self.sprite=pygame.image.load("player.png") #Son sprite
        self.rect= self.sprite.get_rect(x=x, y=y)
        self.speed=5
        self.velocity=[0,0]

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        """
            Affichage du missile
        """
        screen.blit(self.sprite, self.rect)
            

class enemie:
    def __init__(self, x, y):
        self.sprite=pygame.image.load("player.png")
        self.rect=self.sprite.get_rect(x=x, y=y)
        self.speed=1
        self.velocity=[1,0]
    
    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect) #Je place mon missile à sa position

class band:
    def __init__(self):
        self.band=[]
        for i in range(8):
            for j in range(3):
                enemies=enemie((i+0.3)*64*1.5, (j*100)+20)
                self.band.append(enemies)

class App:
    def __init__(self, speed=1):
            screen.blit(background, (0, 0))
            self.ship = Ship((infoObject.current_w / 2) - 20, (infoObject.current_h - (infoObject.current_h / 10)) - 20)
            self.speed = speed
            self.ship.speed=self.speed
            self.pressed_keys = []  # Liste pour stocker les touches enfoncées
            self.timel=0 #Variables me permettant de gere l'envoie des laser
            self.timerl=0
            self.timem=0
            self.timerm=0
            self.groupe=band()
            #self.ship.shot()

        
        

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
            self.ship.velocity[0]=-1
        elif pygame.K_RIGHT in self.pressed_keys:
            self.ship.velocity[0]=1
        else:
            self.ship.velocity[0]=0
        self.ship.move()

        #Faire tirer le vaisseau
        if pygame.K_SPACE in self.pressed_keys:
            self.timerl=time.time()
            if self.timerl-self.timel>=0.7: #Cette conditionelle empche de tirer le missile trop vite
                self.ship.shot()
                self.timel=self.timerl
        
                
        # Mettez à jour la position de tous les lasers
        for bullet in self.ship.bullets:
            bullet.velocity[1] = -1*self.speed
            bullet.move()

        
        #Mettre à jour la position des enemies
        for enemie in self.groupe.band:
            
            infoObject = pygame.display.Info()
            w=infoObject.current_w
            
        
            if enemie.rect.left < 0 or enemie.rect.right >w :
                enemie.velocity[0] = -enemie.velocity[0]*enemie.speed
             
            enemie.move()
        
        # Supprimez les lasers qui ont quitté l'écran
        self.ship.bullets = [bullet for bullet in self.ship.bullets if bullet.rect.y > -bullet.sprite.get_height()]

        #Maintenir le vaisseau en bas de l'écran
        infoObject = pygame.display.Info()
        self.ship.rect.y= (infoObject.current_h - (infoObject.current_h)/20)-65

        #Verifier les colision entre les lasers et les enemies
        
        

    def draw(self):
        screen.fill((255, 255, 255))  # J'efface l'écran précédent
        self.ship.draw()  # Je draw le vaisseau à sa nouvelle position
        for enemie in self.groupe.band:
            enemie.draw()
            
        for bullet in self.ship.bullets:  # Dessinez tous les lasers
            bullet.draw()


        pygame.display.flip()  # J'affiche tous les sprites


pygame.init() #Je crée l'interface pygame
infoObject = pygame.display.Info() #Je récupere les infos de l'ecran pour adapter la taille de la fenetre
#screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h-20))#Je crée la fenetre en fonction de la taille de l'écran
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre


background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 
background = background.convert()
#background.fill((250, 250, 250)) #Je nettoie l'écran   
    
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
    