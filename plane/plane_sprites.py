import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 400, 600)
FRAME_PER_SEC = 60
CREAT_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprites(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprites):

    def __init__(self, is_alt=False):

        super().__init__("./image/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprites):

    def __init__(self):
        super().__init__("./image/enemy.png")
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.speed = random.randint(1, 4)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprites):

    def __init__(self):
        super().__init__("./image/me.png", 0)
        self.speed = 0
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x =0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in (0, 1, 2):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            self.bullets.add(bullet)

class Bullet(GameSprites):

    def __init__(self):
        super().__init__("./image/bullet.png", -3)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120


    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
