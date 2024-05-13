from pygame import *

fenetre = display.set_mode((620,350))
display.set_caption('Tutoriel pygame')
init()
 
#les images
fond = image.load('prii.jpg')
fond = fond.convert()
 
#les spritesheets
perso = image.load('bobsp.svg')
#On associe les touches aux images
imageSprite = {K_DOWN:[perso.subsurface(x,0,96,96)for x in range(0,384,96)],
               K_LEFT:[perso.subsurface(x,96,96,96)for x in range(0,384,96)],
               K_RIGHT:[perso.subsurface(x,192,96,96)for x in range(0,384,96)],
               K_UP:[perso.subsurface(x,288,96,96)for x in range(0,384,96)]}
 
#paramètres de départ
jouer = True
etat = 0
xSprite,ySprite = 202,202
direction = K_DOWN
index_img = 0
 
 
#les fonctions du jeu
def deplacementPerso():
    global xSprite,ySprite,direction,index_img
    if k[K_LEFT]:
        direction = K_LEFT
        index_img = (index_img+1)%4
        xSprite = xSprite - k[K_LEFT]*8
    elif k[K_RIGHT]:
        direction = K_RIGHT
        index_img = (index_img+1)%4
        xSprite = xSprite + k[K_RIGHT]*8
    elif k[K_DOWN]:
        direction = K_DOWN
        index_img = (index_img+1)%4
        ySprite = ySprite + k[K_DOWN]*8
    elif k[K_UP]:
        direction = K_UP
        index_img = (index_img+1)%4
        ySprite = ySprite - k[K_UP]*8
    
while jouer:
    for events in event.get():
        if events.type == QUIT:
            quit()
 
    k = key.get_pressed()
 
    if etat==0:
        fonte = font.SysFont('comicsansms', 36)
        text = fonte.render('Appuyer sur ENTER', True, (0, 255, 0), (0, 5, 255))
        fenetre.fill((255,255,0))
        fenetre.blit(text, (20, 20))
        if k[K_RETURN]:
            etat=1
    
    if etat==1:
        #on execute les fonctions
        deplacementPerso()
        #On affiche les images
        fenetre.blit(fond, (0,0))
        fenetre.blit(imageSprite[direction][index_img],(xSprite,ySprite))
        if k[K_r]:
            etat=0
 
    display.flip()
    #définir les FPS on fait une pause 50ms entre chaque frame
    time.wait(50)