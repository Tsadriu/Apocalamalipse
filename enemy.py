import pygame

from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'Assets/Art/enemy/run', 18)
        self.rect.y += size - self.image.get_size()[1]
        self.movSpeed = randint(3, 7)
        self.damage = randint(5, 20)

    def MoveEnemy(self):
        self.rect.x += self.movSpeed

    def ReverseSprite(self):
        if self.movSpeed > 0:
            self.image = pygame.transform.flip(self.image, True, False) # Fai il flip della sprite

    def ReverseX(self): # Destra/Dinistra
        self.movSpeed = self.movSpeed * -1

    def Die(self):
        self.kill()

    def update(self, shift):
        self.rect.x += shift # Muove il nemico
        self.Animate()
        self.MoveEnemy()
        self.ReverseSprite()
