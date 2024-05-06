import pygame
from pygame.locals import *
import sys
import time 
import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection



#choix serveur ou client
def choiceMode():
    try:
        choice = input("Serveur (1) ou client (0)? : ")
        if choice == "1":
            server_program()
            start_game(server=True)
        elif choice == "0":
            client_program()
            start_game(server=False)
        else:
            raise ValueError("Veuillez entrer 0 ou 1.")
    except Exception as e:
        print("Une erreur est survenue:", str(e))
        choiceMode()

def start_game(server=False):
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

choiceMode()

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
        screen.blit(background, (0, 0))

        self.ship = Ship(infoObject.current_w-(infoObject.current_w / 4) - 20, (infoObject.current_h - (infoObject.current_h / 10)) - 20)
        self.ship.speed = speed*2.2  # Création du vaisseau

        self.ship2 = Ship((infoObject.current_w / 4) - 20, (infoObject.current_h - (infoObject.current_h / 10)) - 20)
        self.ship2.speed = speed*2.2  # Création du vaisseau

        self.pressed_keys = []  # Liste pour stocker les touches enfoncées

        self.timel = 0  # Variables me permettant de gérer l'envoie des laser
        self.timerl = 0

        self.timel_ship2 = 0  # Variable pour gérer le délai entre les tirs de ship2
        self.timerl_ship2 = 0  # Variable pour gérer le délai entre les tirs de ship2

        self.groupe = band()  # Je crée les enemies

        self.tog = time.time()  # Variable me permettant de gérer le changement de vitesse des enemies
        self.anctog = time.time()

        self.score = score()  # Le score



    def update(self, key_events):
        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.pressed_keys:
                    self.pressed_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)

        # Déplacez le vaisseau
        if pygame.K_LEFT in self.pressed_keys:
            self.ship.velocity[0]=-1
        elif pygame.K_RIGHT in self.pressed_keys:
            self.ship.velocity[0]=1
        
        else:
            self.ship.velocity[0]=0

        if pygame.K_q in self.pressed_keys:
            self.ship2.velocity[0]=-1
        elif pygame.K_d in self.pressed_keys:
            self.ship2.velocity[0]=1
        else:
            self.ship2.velocity[0]=0
        

        infoObject = pygame.display.Info()
        w=infoObject.current_w #Cette variable me permet de faire un écran traversable par les bords

        if self.ship.rect.x== w:
            self.ship.rect.x=0
        elif self.ship.rect.x==0:
            self.ship.rect.x=w
        
        if self.ship2.rect.x== w:
            self.ship2.rect.x=0
        elif self.ship2.rect.x==0:
            self.ship2.rect.x=w

        self.ship.move()
        self.ship2.move()

        # Faire tirer ship1
        if pygame.K_SPACE in self.pressed_keys:
            self.timerl = time.time()
            if self.timerl - self.timel >= 0.5:
                self.ship.shot()
                self.timel = self.timerl
        
        # Faire tirer ship2
        if pygame.K_z in self.pressed_keys:
            self.timerl_ship2 = time.time()
            if self.timerl_ship2 - self.timel_ship2 >= 0.5:
                self.ship2.shot()  # Supprimer l'argument de la méthode shot()
                self.timel_ship2 = self.timerl_ship2
        
                
       # Mettez à jour la position de tous les lasers
        bullets_to_remove = []  # Liste temporaire pour stocker les balles à supprimer
        for bullet in self.ship.bullets:
            bullet.velocity[1] = -1 
            bullet.move()
            # Vérifier les collisions entre les lasers et les ennemis
            for enemy in self.groupe.band:
                if bullet.rect.colliderect(enemy.rect):
                    self.groupe.band.remove(enemy)
                    bullets_to_remove.append(bullet)  # Ajoutez la balle à la liste temporaire
                    self.score.score= self.score.score+100 #Si un ennemei est detruit je rajoue 100 points à mon score
                    self.groupe.add()
        # Mettez à jour la position de tous les lasers
        bullets_to_remove2 = []  # Liste temporaire pour stocker les balles à supprimer
        for bullet in self.ship2.bullets:
            bullet.velocity[1] = -1 
            bullet.move()

            # Vérifier les collisions entre les lasers et les ennemis
            for enemy in self.groupe.band:
                if bullet.rect.colliderect(enemy.rect):
                    self.groupe.band.remove(enemy)
                    bullets_to_remove2.append(bullet)  # Ajoutez la balle à la liste temporaire
                    self.score.score= self.score.score+100 #Si un ennemei est detruit je rajoue 100 points à mon score
                    self.groupe.add()

        # Supprimez les balles de la liste originale
        for bullet in bullets_to_remove:
            if bullet in self.ship.bullets:  # Vérifiez si la balle est toujours dans la liste
                self.ship.bullets.remove(bullet)
        # Supprimez les balles de la liste originale
        for bullet in bullets_to_remove2:
            if bullet in self.ship.bullets:  # Vérifiez si la balle est toujours dans la liste
                self.ship2.bullets.remove(bullet)



        # Mettre à jour la position des enemies
        for enemie in self.groupe.band:
            
            infoObject = pygame.display.Info()
            w = infoObject.current_w  # Cette variable me permet de faire faire des tours d'écrans aux enemis

            # Faire descendre les ennemis lorsqu'ils atteignent le bord de l'écran
            if enemie.rect.left < 0 or enemie.rect.right > w:
                enemie.velocity[0] = -enemie.velocity[0]  # Supprimer la multiplication par enemie.speed
                enemie.velocity[1] = 20  # Faire descendre les ennemis

            enemie.move()  # Je fais bouger le mob
            enemie.velocity[1] = 0  # Réinitialiser la vitesse verticale après le mouvement


                    
                
        # Supprimez les lasers qui ont quitté l'écran
        self.ship.bullets = [bullet for bullet in self.ship.bullets if bullet.rect.y > -bullet.sprite.get_height()]

        #Maintenir le vaisseau en bas de l'écran
        infoObject = pygame.display.Info()
        self.ship.rect.y= (infoObject.current_h - (infoObject.current_h)/20)-65

        #Changer la vitesse des ennemis, toute les 30 seconde

        self.tog=time.time() #J'enregiste le temps du jeu
        
        
        if self.tog - self.anctog >=15: #Si la difference entre le moment actuel et le dernier moment de modification est plus que 10 sec, je modifie la vitesse 
            x=2 #Ici x represente la limite de vitesse
            
            if self.groupe.speed>=x:#Si la limite est depasser, je remet ma vitesse à sa limite
                self.groupe.speed=x
            else:
                self.groupe.speed=self.groupe.speed*1.3 #Sinon je rajoute la moitié de la vitesse actuel
                if self.groupe.speed>=x: #Si la limite est depasser, je remet ma vitesse à sa limite
                    self.groupe.speed=x

            for enemie in self.groupe.band:  #Et je l'applique à ton mon groupe
                    enemie.speed=self.groupe.speed
            
            self.anctog=self.tog #Je change la valeur du dernier moment de modification


        
        
        

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

game=True


while game==True:  # Boucle principale du jeu

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