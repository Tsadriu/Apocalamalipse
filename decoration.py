from settings import verticalTileAmount, tileSize, screenWidth, screenHeight
import pygame
from tiles import AnimatedTile, StaticTile
from support import ImportFolderContent
from random import choice, randint


class BackGround:
    def __init__(self, horizon, style='level'):
        self.background = pygame.image.load('Assets/Art/decoration/background.png')
        self.horizon = horizon
        self.background = pygame.transform.scale(self.background, (screenWidth, screenHeight))

        self.style = style

    def draw(self, surface):
        for row in range(verticalTileAmount):
            if row == self.horizon:
                surface.blit(self.background, (0, 0))


class Lava:
    def __init__(self, top, levelWidth):
        lavaWidth = 192  # Lunghezza della sprite nella cartella
        lavaStart = -screenWidth  # dove parte la lava nell'asse x (sinistra)
        lavaTotalX = int((levelWidth + (screenWidth * 2)) / lavaWidth)
        self.lavaSprites = pygame.sprite.Group()

        for tile in range(lavaTotalX):
            x = tile * lavaWidth + lavaStart
            y = top - 50
            sprite = AnimatedTile(lavaWidth, x, y, 'Assets/Art/decoration/lava', 5)
            self.lavaSprites.add(sprite)

    def draw(self, surface, shift):
        self.lavaSprites.update(shift)
        self.lavaSprites.draw(surface)
