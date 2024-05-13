import pygame
import io

def load_and_scale_svg(filename, scale):
    svg_string = open(filename, "rt").read()
    start = svg_string.find('<svg')    
    if start > 0:
        svg_string = svg_string[:start+4] + f' transform="scale({scale})"' + svg_string[start+4:]
    return pygame.image.load(io.BytesIO(svg_string.encode()))

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

pygame_surface = load_and_scale_svg('bob4.svg', 2)
bob=pygame.transform.smoothscale(pygame.image.load('bob4.svg'), (128,128))

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((127, 127, 127))
    window.blit(pygame_surface, pygame_surface.get_rect(center = window.get_rect().center))
    #window.blit(bob, (50,130))
    #window.blit()
    pygame.display.flip()

pygame.quit()
exit()




    