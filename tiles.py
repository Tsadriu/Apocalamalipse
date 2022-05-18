import pygame

import player
from support import ImportFolderContent


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path, speed):
        super().__init__(size, x, y)
        self.frames = ImportFolderContent(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        self.speed = speed

    def Animate(self):
        # Imposta la velocità. Un numero più alto, e più veloce sarà l'animazione. Passare sempre un numero intero
        self.frameIndex += (self.speed / 100)
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self, shift):
        self.Animate()
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Spike(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('Assets/Art/terrain/spike.png').convert_alpha())
        offsetY = y + size
        offsetX = x #- size
        self.rect = self.image.get_rect(bottomleft=(offsetX, offsetY))
        self.damage = 200

class Cherry(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path, 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.value = value
