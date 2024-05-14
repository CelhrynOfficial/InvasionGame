import random
import pygame
from pygame.locals import *
import sys
import time 
import asyncio
import socket
import json


class GameClient:
    def __init__(self, player="Default", server=("127.0.0.1", 12000)):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(0.1)
        self.server = server
        self.player = player

    def send_message(self, msg):
        """ JSON-encode and send msg to server. """
        message = json.dumps(msg).encode("utf8")
        self.client_socket.sendto(message, self.server)

    def check_message(self):
        """ Check if there's a message from the server and return it, or None. """
        try:
            message, address = self.client_socket.recvfrom(1024)
            return json.loads(message.decode("utf8"))
        except socket.timeout:
            pass  # this passes as "non-blocking" for now
        return None
    
def game(player):
    me = GameClient()
    positions = {}
    my_x = my_y = 0
    me.send_message({player: [my_x, my_y]})
    while True:
        move = random.randrange(80)
        if move == 0:
            my_x -= 1
        elif move == 1:
            my_x += 1
        elif move == 2:
            my_y -= 1
        elif move == 3:
            my_y += 1
        if move < 4:
            me.send_message({player: [my_x, my_y]})
            print("me: {}".format([my_x, my_y]))
        updates = me.check_message()
        while updates:
            positions.update(updates)
            print("updates: {}".format(updates))
            print("positions: {}".format(positions))
            updates = me.check_message()
        time.sleep(0.1)

namePlayer = input("Nom : ")
game(namePlayer)

def start_game(server=False):
    BASE_WIDTH, BASE_HEIGHT = 800, 600
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)
    # Définition des couleurs
    WHITE = (255, 255, 255)

    # Taille initiale de la fenêtre
    BASE_WIDTH, BASE_HEIGHT = 800, 600

    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)

    infoObject = pygame.display.Info()  # Définir infoObject ici

    appli = App(server=server)  # Passer le paramètre server à la classe App

    key_events = []  # Liste pour stocker les événements clavier

    game = True

    while game:  # Boucle principale du jeu
        for event in pygame.event.get():  # Récupère tous les événements pygame
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Stockez les événements clavier
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                key_events.append(event)

        # Mettez à jour et dessinez le jeu
        appli.update(key_events)
        appli.draw()

        for enemis in appli.groupe.band: #Si un ennemi dépasse mon vaisseau, on arrête le jeu, le joueur a perdu
            if enemis.rect.y >= appli.ship.rect.y:
                game = False

        key_events.clear()  # Nettoyez la liste des événements clavier après les avoir traités

    pygame.quit()

main()

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
        x = self.rect.x
        y = self.rect.y
        bullet = Bullet(self, x, y)  # Créez un nouveau laser
        self.bullets.append(bullet)  # Ajoutez le laser à la liste



class Bullet:
    def __init__(self, ship, x, y):
        self.sprite = pygame.image.load("player.png")
        self.rect = self.sprite.get_rect(x=x, y=y)
        self.speed = 5
        self.velocity = [0, 0]


    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect)




class enemie:
    def __init__(self, x, y,speed=1):
        self.sprite=pygame.image.load("player.png")
        self.rect=self.sprite.get_rect(x=x, y=y)
        self.speed=speed
        self.velocity=[1,0]
        
    def shot(self):
        x=self.rect.x
        y=self.rect.y
        bullet_e = Bullet(self,x, y)  # Créez un nouveau laser
        self.bullets.append(bullet_e)  # Ajoutez le laser à la liste

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect) #Je place mon missile à sa position



class enemie_b:
    def __init__(self, x, y): #J'initialise mon 'Bullet'
        self.sprite=pygame.image.load("player.png") #Son sprite
        self.rect= self.sprite.get_rect(x=x, y=y)
        self.speed=1
        self.velocity=[0,0]

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        """
            Affichage du missile enemie
        """
        screen.blit(self.sprite, self.rect)



class band:
    def __init__(self):
        self.band=[]
        self.speed=1
        for i in range(8):
            for j in range(2):
                enemies=enemie((i+0.3)*64*1.5, (j*100)+20, self.speed)
                self.band.append(enemies)
    
    def add(self):
        enemies=enemie((0.3)*64*1.5, 20, self.speed)
        self.band.append(enemies)



class score:
    def __init__(self):
        self.score=0
        self.font=pygame.font.Font(None, 24)
        
    
    def draw(self):
        scr=str(self.score)
        txt="Score: "+ scr
        text = self.font.render(txt,1,(255,0,255))
        screen.blit(text, (0,0))


        
class App:
    def __init__(self, speed=1):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.ship1_client = GameClient("player1")
        self.ship2_client = GameClient("player2")

        self.ship1_position = [100, 300]
        self.ship2_position = [700, 300]

        self.speed = speed
        self.ship_speed = speed * 2.2

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ship1_position[0] -= self.ship_speed
        if keys[pygame.K_RIGHT]:
            self.ship1_position[0] += self.ship_speed
        if keys[pygame.K_UP]:
            self.ship1_position[1] -= self.ship_speed
        if keys[pygame.K_DOWN]:
            self.ship1_position[1] += self.ship_speed

        if keys[pygame.K_a]:
            self.ship2_position[0] -= self.ship_speed
        if keys[pygame.K_d]:
            self.ship2_position[0] += self.ship_speed
        if keys[pygame.K_w]:
            self.ship2_position[1] -= self.ship_speed
        if keys[pygame.K_s]:
            self.ship2_position[1] += self.ship_speed

        self.ship1_client.send_message({"position": self.ship1_position})
        self.ship2_client.send_message({"position": self.ship2_position})

        ship1_updates = self.ship1_client.check_message()
        if ship1_updates:
            self.ship1_position = ship1_updates.get("position", self.ship1_position)

        ship2_updates = self.ship2_client.check_message()
        if ship2_updates:
            self.ship2_position = ship2_updates.get("position", self.ship2_position)

        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.ship1_position, 50, 50))
        pygame.draw.rect(self.screen, (0, 0, 255), (*self.ship2_position, 50, 50))

        pygame.display.flip()
        self.clock.tick(60)
        
        
        

    def draw(self):
        screen.fill((255, 255, 255))  # J'efface l'écran précédent
        self.ship.draw()  # Je draw le vaisseau à sa nouvelle position
        self.ship2.draw()
        for enemie in self.groupe.band:
            enemie.draw()
            
        for bullet in self.ship.bullets:  # Dessinez tous les lasers
            bullet.draw()
        
        for bullet in self.ship2.bullets:
            bullet.draw()


        self.score.draw()

        pygame.display.flip()  # J'affiche tous les sprites


pygame.init() #Je crée l'interface pygame
infoObject = pygame.display.Info() #Je récupere les infos de l'ecran pour adapter la taille de la fenetre
#screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h-20))#Je crée la fenetre en fonction de la taille de l'écran
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre


background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 
background = background.convert()
  
    
appli=App() #Je définie mon application, avec une valeur de vitesse


key_events = []  # Liste pour stocker les événements clavier


if __name__ == "__main__":
    pygame.init()
    for event in pygame.event.get():  # Récupère tous les événements pygame
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Stockez les événements clavier
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            key_events.append(event)

    # Mettez à jour et dessinez le jeu
    appli.update(key_events)
    appli.draw()


    for enemis in appli.groupe.band: #Si un enemies dépasse mon vaisseau, on arrete le jeu, le joueur à perdu
        if enemis.rect.y>= appli.ship.rect.y:
            game=False
    
   
    
    
    key_events.clear()  # Nettoyez la liste des événements clavier après les avoir traités
    while True:
        appli.update()


