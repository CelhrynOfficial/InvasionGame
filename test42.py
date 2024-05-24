import pygame
from pygame.locals import *
import sys
import time
import random
import asyncio

class Ship:
    def __init__(self, x, y):
        self.perso = pygame.image.load('bob4.svg')
        self.rect = self.perso.get_rect(x=x, y=y)
        self.perso = pygame.image.load('spritebobi.png')

        self.sprite = {
            K_DOWN: [self.perso.subsurface((x, 0, 96, 96)) for x in range(0, 384, 96)],
            K_LEFT: [self.perso.subsurface((x, 96, 96, 96)) for x in range(0, 384, 96)],
            K_RIGHT: [self.perso.subsurface((x, 192, 96, 96)) for x in range(0, 384, 96)],
            K_UP: [self.perso.subsurface((x, 288, 96, 96)) for x in range(0, 384, 96)]
        }

        self.speed = 2
        self.velocity = [0, 0]
        self.bullets = []
        self.direction = K_DOWN
        self.index = 0
        self.bob = 0

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        screen.blit(self.sprite[self.direction][self.index], self.rect)

    def shot(self):
        x = self.rect.x
        y = self.rect.y
        speed = self.speed // 2
        bullet = Bullet(self, x, y, self.bob, speed * 3)
        self.bullets.append(bullet)

    def respirte(self, perso):
        self.perso = pygame.image.load(perso)
        self.sprite = {
            K_DOWN: [self.perso.subsurface((x, 0, 64, 64)) for x in range(0, 256, 64)],
            K_LEFT: [self.perso.subsurface((x, 64, 64, 64)) for x in range(0, 256, 64)],
            K_RIGHT: [self.perso.subsurface((x, 128, 64, 64)) for x in range(0, 256, 64)],
            K_UP: [self.perso.subsurface((x, 192, 64, 64)) for x in range(0, 256, 64)]
        }
        self.bob = 1

class Bullet:
    def __init__(self, ship, x, y, bob, speed=3):
        if bob == 0:
            self.perso = pygame.image.load("bull.svg")
            self.rect = self.perso.get_rect(x=x, y=y)
            self.perso = pygame.image.load("spbl.png")
        elif bob == 1:
            self.perso = pygame.image.load("bull.svg")
            self.rect = self.perso.get_rect(x=x, y=y)
            self.perso = pygame.image.load("spritebobi.png")

        self.sprite = [self.perso.subsurface((x % 4) * 64, (x // 4) * 64, 64, 64) for x in range(16)]
        self.ref = pygame.image.load("bull.svg")
        self.speed = speed
        self.velocity = [0, 0]
        self.index = 0

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        screen.blit(self.sprite[self.index], self.rect)

class Enemie:
    def __init__(self, x, y, bob, speed=1):
        if bob == 0:
            self.sprite = pygame.image.load("jellyy.png")
        elif bob == 1:
            self.sprite = pygame.image.load("bob4.svg")
        self.rect = self.sprite.get_rect(x=x, y=y)
        self.speed = speed
        self.velocity = [1, 0]

    def resprite(self, sprite):
        self.sprite = pygame.image.load(sprite)

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        screen.blit(self.sprite, self.rect)

class EnemieBullet:
    def __init__(self, x, y, bob, speed=1):
        if bob == 0:
            self.perso = pygame.image.load("bull.svg")
            self.rect = self.perso.get_rect(x=x, y=y)
            self.perso = pygame.image.load("ebsp.png")
        elif bob == 1:
            self.perso = pygame.image.load("bull.svg")
            self.rect = self.perso.get_rect(x=x, y=y)
            self.perso = pygame.image.load("spritebobi.png")

        self.sprite = [self.perso.subsurface((x % 4) * 64, (x // 4) * 64, 64, 64) for x in range(16)]
        self.ref = pygame.image.load("bull.svg")
        self.speed = speed
        self.velocity = [0, 0]
        self.index = 0

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        screen.blit(self.sprite[self.index], self.rect)

class Band:
    def __init__(self, speed):
        self.band = []
        self.bullets = []
        self.speed = speed
        self.bob = 0
        for i in range(8):
            for j in range(3):
                enemies = Enemie((i + 0.3) * 64 * 1.5, (j * 100) + 20, self.bob, self.speed)
                self.band.append(enemies)

    def add(self, bob):
        enemies = Enemie((0.3) * 64 * 1.5, 20, bob, self.speed)
        self.band.append(enemies)

    def shot(self, bob):
        i = random.randint(0, len(self.band) - 1)
        x = self.band[i].rect.x
        y = self.band[i].rect.y
        bullet_e = EnemieBullet(x, y, bob, self.speed)
        self.bullets.append(bullet_e)

    def resprite(self, sprite):
        for enemie in self.band:
            enemie.resprite(sprite)

class Boss:
    def __init__(self, x, y, speed=1):
        self.sprite = pygame.image.load("Boss.jpg")
        self.rect = self.sprite.get_rect(x=x, y=y)
        self.life = Life(10)
        self.speed = speed
        self.velocity = [3, 0]
        self.bullet_b = []

    def shot(self, bob):
        x = self.rect.x
        y = self.rect.y
        bullet = EnemieBullet(x, y, bob, self.speed)
        self.bullet_b.append(bullet)

    def respirte(self, perso):
        self.sprite = pygame.image.load(perso)

    def move(self):
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def draw(self):
        screen.blit(self.sprite, self.rect)

class Life:
    def __init__(self, lp):
        self.life = lp
        self.font = pygame.font.Font(None, 34)

    def draw(self):
        scr = str(self.life)
        txt = "Life: " + scr
        text = self.font.render(txt, 1, (0, 0, 0))
        screen.blit(text, (700, 0))

class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 34)

    def draw(self):
        scr = str(self.score)
        txt = "Score: " + scr
        text = self.font.render(txt, 1, (0, 0, 0))
        screen.blit(text, (0, 0))

class App:
    def __init__(self, speed=1):
        screen.blit(background, (0, 0))
        self.speed = speed
        self.game = True
        self.ship = Ship((infoObject.current_w / 2) - 64, infoObject.current_h - 64)
        self.enemies = Band(self.speed)
        self.score = Score()
        self.life = Life(3)
        self.boss = None

    def draw(self):
        screen.blit(background, (0, 0))
        self.ship.draw()
        for bullet in self.ship.bullets:
            bullet.draw()
        for enemie in self.enemies.band:
            enemie.draw()
        for bullet in self.enemies.bullets:
            bullet.draw()
        if self.boss:
            self.boss.draw()
            for bullet in self.boss.bullet_b:
                bullet.draw()
        self.score.draw()
        self.life.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]:
                    self.ship.velocity = [0, 0]
                    if event.key == K_LEFT:
                        self.ship.velocity[0] = -1
                    elif event.key == K_RIGHT:
                        self.ship.velocity[0] = 1
                    elif event.key == K_UP:
                        self.ship.velocity[1] = -1
                    elif event.key == K_DOWN:
                        self.ship.velocity[1] = 1
                    self.ship.direction = event.key
                elif event.key == K_SPACE:
                    self.ship.shot()
            elif event.type == KEYUP:
                if event.key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]:
                    self.ship.velocity = [0, 0]

    async def main_loop(self):
        while self.game:
            self.handle_events()
            self.ship.move()
            for bullet in self.ship.bullets:
                bullet.move()
            for enemie in self.enemies.band:
                enemie.move()
            for bullet in self.enemies.bullets:
                bullet.move()
            if self.boss:
                self.boss.move()
                for bullet in self.boss.bullet_b:
                    bullet.move()
            self.draw()
            await asyncio.sleep(0)  # Limite à ~60 FPS

async def main():
    global screen, background, infoObject
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    background = pygame.image.load("prairioa.jpg")
    app = App()
    await app.main_loop()

if __name__ == "__main__":
    asyncio.run(main())




    