from pygame import *
 
fenetre = display.set_mode((620,350))
display.set_caption('Tutoriel pygame')
init()
 
#les images
 
#les spritesheets
danse = image.load('bp.svg')
#On associe les touches aux images

danseSprite = [danse.subsurface((x%4)*96,(x//4)*96,96,96)for x in range(16)]

#paramètres de départ
jouer = True
index_danse = 0
 
#les fonctions du jeu

while jouer:
    for events in event.get():
         if events.type == QUIT:
             quit()
    #les 4 lignes pour afficher le sprite animé
    index_danse = (index_danse +1)%(len(danseSprite))
    fenetre.fill((255,255,0))
    fenetre.blit(danseSprite[index_danse],(100,100))
    display.flip()
    #définir les FPS on fait une pause 50ms entre chaque frame
    time.wait(50)