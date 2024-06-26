from pygame import *
import pygame
from pygame.locals import *
import sys
import time 
import random
import asyncio

#commande pour le son et bruitages
pygame.init()
pygame.mixer.init()
#bulles = pygame.mixer.Sound("bul.wav")
#pygame.mixer.Sound.get_volume(bulles)-3
splash = pygame.mixer.Sound("pop.wav")


class Ship:
    def __init__(self, x, y):

        self.perso= image.load('bob4.svg') #J'utilise cette image comme reference pour ma hit box
        self.rect= self.perso.get_rect(x=x, y=y)
        self.perso = image.load('spritebobi.png') #Puis j'utilise le sprite shite et le divise en sprite


        self.sprite = {K_DOWN:[self.perso.subsurface(x,0,96,96)for x in range(0,384,96)],
               K_LEFT:[self.perso.subsurface(x,96,96,96)for x in range(0,384,96)],
               K_RIGHT:[self.perso.subsurface(x,192,96,96)for x in range(0,384,96)],
               K_UP:[self.perso.subsurface(x,288,96,96)for x in range(0,384,96)]}
        
        
        self.speed=1
        self.velocity=[0,0]
        self.bullets=[]
        self.direction=K_DOWN
        self.index=0

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite[self.direction][self.index], self.rect)

    def shot(self):
        x=self.rect.x
        y=self.rect.y
        bullet = Bullet(self,x, y)  # Créez un nouveau laser
        self.bullets.append(bullet)  # Ajoutez le laser à la liste


       
class Bullet:
    def __init__(self, ship, x, y): #J'initialise mon 'Bullet'
        self.perso=pygame.image.load("bull.svg") #Son sprite
        self.rect= self.perso.get_rect(x=x, y=y)
        self.perso=pygame.image.load("spbl.png")

        self.sprite=[self.perso.subsurface((x%4)*64,(x//4)*64,64,64)for x in range(16)]
        self.ref=pygame.image.load("bull.svg")
        self.speed=3
        self.velocity=[0,0]
        self.index = 0

         

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        """
            Affichage du missile
        """
        screen.blit(self.sprite[self.index], self.rect)

    
class enemie:
    def __init__(self, x, y,speed=1):
        self.sprite=pygame.image.load("jellyy.png")
        self.rect=self.sprite.get_rect(x=x, y=y)
        self.speed=speed
        self.velocity=[1,0]
       

    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect) #Je place mon missile à sa position

    


class enemie_b:
    def __init__(self, x, y, speed): #J'initialise mon 'Bullet' enemie
        self.perso=pygame.image.load("bull.svg") #Son sprite
        self.rect= self.perso.get_rect(x=x, y=y)
        self.perso=pygame.image.load("ebsp.png")

        self.sprite=[self.perso.subsurface((x%4)*64,(x//4)*64,64,64)for x in range(16)]
        self.ref=pygame.image.load("bull.svg")
        self.speed=speed
        self.velocity=[0,0]
        self.index = 0


    def move(self):
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        """
            Affichage du missile enemie
        """
        screen.blit(self.sprite[self.index], self.rect)

class band:
    def __init__(self, speed):
        self.band=[]
        self.bullets=[]
        self.speed=speed
        self.speed_b=speed
        for i in range(8):
            for j in range(3) :
                enemies=enemie((i+0.3)*64*1.5, (j*100)+20, self.speed)
                self.band.append(enemies)
    
    def add(self):
        enemies=enemie((0.3)*64*1.5, 20, self.speed)
        self.band.append(enemies)

    def shot(self):
         
        i=random.randint(0, len(self.band)-1)
        x=self.band[i].rect.x
        y=self.band[i].rect.y
        bullet_e = enemie_b(x, y,  self.speed_b)  # Créez un nouveau laser
        self.bullets.append(bullet_e)  # Ajoutez le laser à la liste

class Boss:
    def __init__(self, x, y, speed=1):
        self.sprite=pygame.image.load("Boss.png")
        self.rect=self.sprite.get_rect(x=x, y=y)
        self.life=life(10)
        self.speed=speed
        self.velocity=[3,0]
        self.bullet_b=[]
       

    def shot(self):
        x=self.rect.x
        y=self.rect.y
        bullet = enemie_b (x, y, self.speed)  # Créez un nouveau laser
        self.bullet_b.append(bullet)  # Ajoutez le laser à la liste

    def move(self):
        print(self.speed)
        self.rect.move_ip(self.velocity[0]*self.speed, self.velocity[1]*self.speed )

    def draw(self):
        screen.blit(self.sprite, self.rect) #Je place mon missile à sa position  

class life:
    def __init__(self, lp):
        self.life=lp
        self.font=pygame.font.Font(None, 34)
        
    
    def draw(self):
        scr=str(self.life)
        txt="Life: "+ scr
        text = self.font.render(txt,1,(0,0,0))
        screen.blit(text, (700,0))

class score:
    def __init__(self):
        self.score=14900
        self.font=pygame.font.Font(None, 34)
        
    
    def draw(self):
        scr=str(self.score)
        txt="Score: "+ scr
        text = self.font.render(txt,1,(0,0,0))
        screen.blit(text, (0,0))

        
class App:
    def __init__(self, speed=1):
            screen.blit(background, (0, 0))
            
            self.game=0
                
            self.speed=speed
            
            self.ship = Ship((infoObject.current_w / 2) - 20, (infoObject.current_h - (infoObject.current_h / 10)) - 20)
            self.ship.speed=self.speed*2 #Création du vaisseau

            self.pressed_keys = []  # Liste pour stocker les touches enfoncées

            self.timel=0 #Variables me permettant de gere l'envoie des laser du joueur
            self.timerl=0

            self.groupe=band(self.speed) #Je crée les enemies

            self.boss=Boss(0,0, self.speed)

            self.tog=time.time() #Variable me permettant de gerer le changement de vitesse des enemies 
            self.anctog=time.time()

            self.cycle=0 #Variable qui mémorise le nombre de cycle du jeu

            self.score=score() #Le score

            self.background= pygame.image.load('prairioa.jpg')

            

            

            

        
        

    def update(self, key_events):

        self.cycle+=1 #A chaque fois que je fais un cycle je le mémorise
        #print(self.cycle)

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
            self.ship.direction = K_LEFT
            if self.cycle%50==0:
                self.ship.index = (self.ship.index+1)%4
            
        elif pygame.K_RIGHT in self.pressed_keys:
            self.ship.velocity[0]=1
            self.ship.direction = K_RIGHT
            if self.cycle%50==0:
                self.ship.index = (self.ship.index+1)%4
        else:
            self.ship.velocity[0]=0
            self.ship.direction = K_DOWN
            self.ship.index = 0

        infoObject = pygame.display.Info()
        w=infoObject.current_w #Cette variable me permet de faire un écran traversable par les bords

        if self.ship.rect.x== w:
            self.ship.rect.x=0
        elif self.ship.rect.x==0:
            self.ship.rect.x=w

        self.ship.move()

        #Faire tirer le vaisseau
        if pygame.K_SPACE in self.pressed_keys:
            self.timerl=time.time()
            #bulles.play()

            if self.timerl-self.timel>=0.5: #Cette conditionelle empeche de tirer le missile trop vite
                self.ship.shot()
                self.timel=self.timerl
        
                
       # Mettez à jour la position de tous les lasers
        bullets_to_remove = []  # Liste temporaire pour stocker les balles à supprimer
        for bullet in self.ship.bullets:
            bullet.velocity[1] = -1 
            bullet.move()
            bullet.index= (bullet.index +1)%(len(bullet.sprite))


            if self.score.score<15000:
                # Vérifier les collisions entre les lasers et les ennemis
                for enemy in self.groupe.band:
                    if bullet.rect.colliderect(enemy.rect):
                        self.groupe.band.remove(enemy)
                        bullets_to_remove.append(bullet)  # Ajoutez la balle à la liste temporaire
                        self.score.score= self.score.score+100 #Si un ennemei est detruit je rajoue 100 points à mon score
                        splash.play()
                        self.groupe.add()

            #Vérifier les collisions entres les missiles et le boss          
            elif self.score.score>=15000:
                if bullet.rect.colliderect(self.boss.rect):
                        bullets_to_remove.append(bullet)  # Ajoutez la balle à la liste temporaire
                        self.score.score= self.score.score+500 #Si le boss est touché je rajoue 100 points à mon score
                        self.boss.life.life=self.boss.life.life-1
                        print(self.boss.life.life)
                        if self.boss.life.life==0:
                            self.victory()
                        

      
                    
                  

        # Supprimez les balles de la liste originale
        for bullet in bullets_to_remove:
            if bullet in self.ship.bullets:  # Vérifiez si la balle est toujours dans la liste
                self.ship.bullets.remove(bullet)

        if self.score.score<15000:
            #Faire tirer les ennemis
            if self.cycle%200==0:
                self.groupe.shot()
            
                
            # Mettez à jour la position de tous les lasers ennemis
            bullets_e_to_remove = []  # Liste temporaire pour stocker les balles à supprimer
            for bullet in self.groupe.bullets:
                bullet.velocity[1] = 1 
                bullet.move()
                
                if self.cycle%10==0:
                    bullet.index= (bullet.index +1)%(len(bullet.sprite))
                    

                # Vérifier les collisions entre les lasers et le joueur
                for bullet in self.groupe.bullets:
                    if bullet.rect.colliderect(self.ship.rect):
                        self.groupe.bullets.remove(bullet)
                        bullets_e_to_remove.append(bullet)  # Ajoutez la balle à la liste temporaire
                        self.gameover()

            # Supprimez les balles de la liste originale
            for bullet in bullets_e_to_remove:
                if bullet in self.groupe.bullets:  # Vérifiez si la balle est toujours dans la liste
                    self.groupe.bullets.remove(bullet)
                    


            # Mettre à jour la position des enemies
            if self.cycle%3==0:
                for enemie in self.groupe.band:
                    
                    infoObject = pygame.display.Info()
                    w = infoObject.current_w  # Cette variable me permet de faire faire des tours d'écrans aux enemis

                    # Faire descendre les ennemis lorsqu'ils atteignent le bord de l'écran
                    if enemie.rect.left < 0 or enemie.rect.right > w:
                        enemie.velocity[0] = -enemie.velocity[0]  # Supprimer la multiplication par enemie.speed
                        enemie.velocity[1] = 20  # Faire descendre les ennemis

                    enemie.move()  # Je fais bouger le mob
                    enemie.velocity[1] = 0  # Réinitialiser la vitesse verticale après le mouvement

        #Je gere les lasers du boss
        elif self.score.score>=15000:

            #Faire tirer les ennemis
            if self.cycle%150==0:
                self.boss.shot()
            
                
            # Mettez à jour la position de tous les lasers du boss
            bullets_b_to_remove = []  # Liste temporaire pour stocker les balles à supprimer
            for bullet in self.boss.bullet_b:
                bullet.velocity[1] = 1 
                bullet.move()
                
                if self.cycle%10==0:
                    bullet.index= (bullet.index +1)%(len(bullet.sprite))
                    

                # Vérifier les collisions entre les lasers et le joueur
                for bullet in self.boss.bullet_b:
                    if bullet.rect.colliderect(self.ship.rect):
                        self.boss.bullet_b.remove(bullet)
                        bullets_b_to_remove.append(bullet)  # Ajoutez la balle à la liste temporaire
                        self.gameover()
                        self.game=2

            # Supprimez les balles de la liste originale
            for bullet in bullets_b_to_remove:
                if bullet in self.groupe.bullets:  # Vérifiez si la balle est toujours dans la liste
                    self.groupe.bullets.remove(bullet)

            if self.cycle%3==0:
                infoObject = pygame.display.Info()
                w = infoObject.current_w  # Cette variable me permet de faire faire des tours d'écrans au Boss

                # Faire descendre le Boss lorsqu'ils atteignent le bord de l'écran
                if self.boss.rect.left < 0 or self.boss.rect.right > w:
                    self.boss.velocity[0] = -self.boss.velocity[0]  # Supprimer la multiplication par enemie.speed
                    self.boss.velocity[1] = 30  # Faire descendre les ennemis

                self.boss.move()  # Je fais bouger le mob
                self.boss.velocity[1] = 0  # Réinitialiser la vitesse verticale après le mouvement

                    
                
        # Supprimez les lasers qui ont quitté l'écran
        self.ship.bullets = [bullet for bullet in self.ship.bullets if bullet.rect.y > -bullet.ref.get_height()]

        #Maintenir le vaisseau en bas de l'écran
        infoObject = pygame.display.Info()
        self.ship.rect.y= (infoObject.current_h - (infoObject.current_h)/20)-65

        #Changer la vitesse des ennemis, toute les 30 seconde

        self.tog=time.time() #J'enregiste le temps du jeu
        
        x=2*self.speed #Ici x represente la limite de vitesse

        if self.score.score>10000: #Si le joueur depasse le score de 10.000 point
            x=3*self.speed #Je change la limite de vitesse
            self.groupe.speed =x
            for enemie in self.groupe.band:  #Et je l'applique à ton mon groupe
                    enemie.speed=self.groupe.speed

        if self.tog - self.anctog >=15 : #Si la difference entre le moment actuel et le dernier moment de modification est plus que 10 sec, je modifie la vitesse 
            
            if self.groupe.speed>=x:#Si la limite est depasser, je remet ma vitesse à sa limite
                self.groupe.speed=x
            else:
                self.groupe.speed=self.groupe.speed+1 #Sinon je rajoute 1 à la vitesse actuel
                if self.groupe.speed>=x: #Si la limite est depasser, je remet ma vitesse à sa limite
                    self.groupe.speed=x

            for enemie in self.groupe.band:  #Et je l'applique à ton mon groupe
                    enemie.speed=self.groupe.speed
            
            self.anctog=self.tog #Je change la valeur du dernier moment de modification
        
        


        
        
        

    def draw(self):
        if self.game==0:
            screen.fill((0, 0, 0))  # J'efface l'écran précédent
            screen.blit(self.background,(0,0))
            self.ship.draw()  # Je draw le vaisseau à sa nouvelle position
                
            for bullet in self.ship.bullets:  # Dessinez tous les lasers
                bullet.draw()

            if self.score.score<15000:
                for enemie in self.groupe.band:
                    enemie.draw()

                for bullet in self.groupe.bullets:
                    bullet.draw()

            elif self.score.score>=15000:
                self.boss.draw()
                self.boss.life.draw()
                for bullet in self.boss.bullet_b:
                    bullet.draw()

            

            self.score.draw()
        elif self.game==1:
            self.victory
        elif self.game==2:
            self.gameover
        pygame.display.flip()  # J'affiche tous les sprites

    def gameover(self):
        
        screen.fill((0, 0, 0))
        
        self.game=2

        self.background= pygame.image.load('gameover.png')
            
        screen.blit(self.background,(0,0))
            
        pygame.display.flip()

    def victory(self):
        
        screen.fill((0, 0, 0))
        
        self.game=1

        self.background= pygame.image.load('winner.png')
            
        screen.blit(self.background,(0,0))
            
        pygame.display.flip()


# Taille initiale de la fenêtre
BASE_WIDTH, BASE_HEIGHT = 800, 600

pygame.init() #Je crée l'interface pygame

screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)

infoObject = pygame.display.Info() #Je récupere les infos de l'ecran pour adapter la taille de la fenetre
#screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h-20))#Je crée la fenetre en fonction de la taille de l'écran
pygame.display.set_caption('Invaders') #Je choisi le nom de ma fenetre


background = pygame.Surface(screen.get_size()) #Je crée mon fond d'écran 
background = background.convert()

#background sound
mixer.music.load('Under.wav')
mixer.music.play(-1) 


async def main():    
    appli=App(1) #Je définie mon application, avec une valeur de vitesse

    key_events = []  # Liste pour stocker les événements clavier

    etat = 0

    while True:  # Boucle principale du jeu
        
        for event in pygame.event.get():  # Récupère tous les événements pygame
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Stockez les événements clavier
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                
                key_events.append(event)

        if appli.game==0:
            if etat==0:
                enter=pygame.image.load('entrer.png')
                screen.blit(enter,(0,0))
                pygame.display.flip()
                k = key.get_pressed()
                if k[K_RETURN]:
                    etat=1
                
                
            if etat==1:
                # Mettez à jour et dessinez le jeu
                appli.update(key_events)
                appli.draw()


                for enemis in appli.groupe.band: #Si un enemies dépasse mon vaisseau, on arrete le jeu, le joueur à perdu
                    if enemis.rect.y>= appli.ship.rect.y:
                        appli.gameover()

        

        time.sleep(0.001)
        
    
        
        
        key_events.clear()  # Nettoyez la liste des événements clavier après les avoir traités
        await asyncio.sleep(0)

asyncio.run(main())