"""Exemple d'affichage d'une fenêtre simple."""
import pygame
from pygame.locals import *
import sys
import time


"""

Cette version du jeu culte "Space invaders" est un projet scolaire de l'année 2023-2024
Nous sommes une équipes de trois eleves de Terminal NSI
Si vous souhaiter travailler dessus, veillez ne pas effacer ce message et actualiser le temps de travaille

Temps de travail: 3H

"""



#Création des classes
class Ship:
    def __init__(self,x,y): #J'initialise mon 'ship'
        self.sprit=pygame.image.load("player.png") #Son sprite
        self.x = x #Ses coordonnées
        self.y = y
        self.bullet=0 #Je crée un missile vide pour pouvoir le remplire par la suite

    def draw(self):
        
        screen.blit(self.sprit,(self.x,self.y)) #Je place mon missile à sa position
               

    def move(self, dx, dy):
       
        self.x += dx #Je change la position de mon vaisseau
        self.y += dy #Le vaisseau ne change pas la valeurs des ordonné mais je crée quand meme la posibilité de le faire
        
        if self.x>infoObject.current_w-65: #Je crée deux mur invisble pour empecher le joueur de sortir de l'écran
            self.x= infoObject.current_w-65
            
        if self.x<0:
            self.x=0


#        if self.x>infoObject.current_w-65: #Je crée un mur traversable
#            self.x= 0
            
#       if self.x<0:
#           self.x=infoObject.current_w-65


    
    def shot(self):
        
        self.bullet=Bullet(self) #Je crée le missile 
        

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
    def __init__(self,speed=1): #J'innitialise l'application qui permet de faire tourner le jeu
        """
            Initialisation  des éléments
        """
        #Afficher le vaisseau
        screen.blit(background, (0, 0)) #Je crée le background de la fenetre
        self.ship=Ship((infoObject.current_w/2)-20,(infoObject.current_h-(infoObject.current_h/10))-20) #Je place le vaisseau au milieur de l'écran
        #Création du missile
        self.ship.shot() #Je shot, pour crée mon missile
        self.ship.bullet.y=-infoObject.current_h #Je place mon missile en haut de l'ecran pour ne pas le voir en lancant le jeu
        #Parametrage de la vitesse
        self.speed=speed

    def update(self):

        events = pygame.event.get()

        if event.type == pygame.KEYDOWN: #Cette boucle me permet de se déplacer quand j'appuie sur un bouton du clavier, ou de tirer
            if event.key == pygame.K_LEFT:
                self.ship.move(-1*self.speed,0)
            if event.key == pygame.K_RIGHT:
                self.ship.move(1*self.speed,0)
            if event.key == pygame.K_UP:
                self.ship.move(0,-1*self.speed)
            if event.key == pygame.K_DOWN:
                self.ship.move(0,1*self.speed)
            if event.key == pygame.K_TAB:
                self.ship.shot()
                

    def draw(self): 
        
        screen.fill((255,255,255))#J'efface l'écran précedant
        self.ship.draw() #Je draw le vaisseau à sa nouvelle position
        self.ship.bullet.draw() #De meme pour le missile
        self.ship.bullet.y-=3*self.speed #Je fais bouger mon missile de 5 vers le haut
        pygame.display.flip() #J'affiche tous les sprites

        


pygame.init() #Je crée l'interface pygame
infoObject = pygame.display.Info() #Je récupere les infos de l'ecran pour adapter la taille de la fenetre
screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h-20))#Je crée la fenetre en fonction de la taille de l'écran
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre


background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 
background = background.convert()
#background.fill((250, 250, 250)) #Je nettoie l'écran   
    
appli=App(2) #Je définie mon application, avec une valeur de vitesse


while True: #Boucle principas du jeu

    #time.sleep(5/10000)
    for event in pygame.event.get(): #Vérification qui me permet de fermer la fenetre
        if event.type == pygame.QUIT: sys.exit()
    
    #A chaque tour dans la boucle je verifie les modification et je les affiches
    appli.update()
    appli.draw()
