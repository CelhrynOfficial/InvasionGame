import pygame
import sys

# Initialise screen
pygame.init()
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w-20, infoObject.current_h-20))
pygame.display.set_caption('Invaders')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()    

while True:

    #time.sleep(5/10000)
    for event in pygame.event.get():
        print(event.type)
        print(pygame.key.key_code)
        print(pygame.key.name)
        if event.type == pygame.QUIT: sys.exit()
