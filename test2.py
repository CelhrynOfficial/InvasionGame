import pygame
from pygame.locals import *

# Initialisation de pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)

# Taille initiale de la fenêtre
BASE_WIDTH, BASE_HEIGHT = 800, 600

# Création de la fenêtre en mode fenêtré avec la possibilité de redimensionnement
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)
pygame.display.set_caption('Space Invaders')

class Ship:
    def __init__(self, x, y, width, height):
        # Chargement du sprite du vaisseau
        self.original_sprite = pygame.image.load("player.png")
        # Redimensionnement du sprite du vaisseau
        self.sprite = pygame.transform.scale(self.original_sprite, (width, height))
        # Récupération du rectangle englobant le sprite pour la détection de collisions
        self.rect = self.sprite.get_rect()
        # Positionnement initial du vaisseau
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Affichage du vaisseau à sa position actuelle
        screen.blit(self.sprite, self.rect)

class Bullet:
    def __init__(self, x, y, width, height):
        # Chargement du sprite du missile
        self.original_sprite = pygame.image.load("bob4.svg")
        # Redimensionnement du sprite du missile
        self.sprite = pygame.transform.scale(self.original_sprite, (width, height))
        # Récupération du rectangle englobant le sprite pour la détection de collisions
        self.rect = self.sprite.get_rect()
        # Positionnement initial du missile
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Affichage du missile à sa position actuelle
        screen.blit(self.sprite, self.rect)

class App:
    def __init__(self, speed=1):
        # Dimensions initiales du vaisseau et du missile
        self.ship_width = BASE_WIDTH // 10
        self.ship_height = BASE_HEIGHT // 10
        self.bullet_width = BASE_WIDTH // 50
        self.bullet_height = BASE_HEIGHT // 50
        # Création du vaisseau
        self.ship = Ship((BASE_WIDTH / 2) - (self.ship_width / 2), 
                         (BASE_HEIGHT - (BASE_HEIGHT / 10)) - (self.ship_height / 2),
                         self.ship_width, self.ship_height)
        # Vitesse de déplacement
        self.speed = speed
        # Liste des missiles tirés
        self.bullets = []

    def update(self, key_events):
        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Déplacement du vaisseau vers la gauche
                    self.ship.rect.x -= self.speed
                if event.key == pygame.K_RIGHT:
                    # Déplacement du vaisseau vers la droite
                    self.ship.rect.x += self.speed
                if event.key == pygame.K_SPACE:
                    # Création et ajout d'un nouveau missile à la liste
                    bullet = Bullet(self.ship.rect.x + self.ship.rect.width / 2 - (self.bullet_width / 2), 
                                    self.ship.rect.y,
                                    self.bullet_width, self.bullet_height)
                    self.bullets.append(bullet)

        # Mise à jour de la position des missiles
        for bullet in self.bullets:
            bullet.rect.y -= 3 * self.speed

        # Suppression des missiles qui ont quitté l'écran
        self.bullets = [bullet for bullet in self.bullets if bullet.rect.y > -bullet.rect.height]

    def draw(self, screen):
        # Effacement de l'écran précédent
        screen.fill(WHITE)
        # Affichage du vaisseau
        self.ship.draw(screen)
        # Affichage des missiles
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # Rafraîchissement de l'écran
        pygame.display.flip()

# Initialisation de l'application
app = App(2)

# Boucle principale du jeu
running = True
while running:
    key_events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            # Fermeture de la fenêtre
            running = False
        elif event.type == KEYDOWN or event.type == KEYUP:
            # Gestion des événements clavier
            key_events.append(event)
        elif event.type == VIDEORESIZE:
            # Redimensionnement de la fenêtre
            BASE_WIDTH, BASE_HEIGHT = event.size
            screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), RESIZABLE)
            # Ajustement de la taille et de la position du vaisseau et des missiles
            app.ship_width = BASE_WIDTH // 10
            app.ship_height = BASE_HEIGHT // 10
            app.bullet_width = BASE_WIDTH // 50
            app.bullet_height = BASE_HEIGHT // 50
            app.ship.sprite = pygame.transform.scale(app.ship.original_sprite, (app.ship_width, app.ship_height))
            app.ship.rect = app.ship.sprite.get_rect()
            app.ship.rect.topleft = ((BASE_WIDTH / 2) - (app.ship_width / 2), 
                                     (BASE_HEIGHT - (BASE_HEIGHT / 10)) - (app.ship_height / 2))
            for bullet in app.bullets:
                bullet.sprite = pygame.transform.scale(bullet.original_sprite, (app.bullet_width, app.bullet_height))
                bullet.rect = bullet.sprite.get_rect()
                bullet.rect.topleft = (bullet.rect.x, bullet.rect.y)

    app.update(key_events)
    app.draw(screen)

# Fermeture de pygame
pygame.quit()
