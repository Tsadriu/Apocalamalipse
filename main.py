import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        pygame.display.set_caption('Apocalamalypse')
        # Attributi livelli e 
        self.max_level = 0 # Imposta il numero di livello sbloccati.
        self.playerMaxHealth = 100
        self.playerCurrentHealth = 100

        # Audio
        self.levelMusic = pygame.mixer.Sound('Assets/Audio/level0.ogg')
        self.overworldMusic = pygame.mixer.Sound('Assets/Audio/overworld.ogg')
        self.overworldMusic.set_volume(0.1)

        # Creazione mappa mondo
        self.overworld = Overworld(0, self.max_level, screen, self.CreateLevel)
        self.status = 'overworld'
        self.overworldMusic.play(loops=-1)

        # Intefaccia utente
        self.ui = UI(screen)

    def CreateLevel(self, current_level):
        self.level = Level(current_level, screen, self.CreateOverworld, self.ChangePlayerHealth)
        self.status = 'level'
        self.overworldMusic.stop()
        self.levelMusic = pygame.mixer.Sound('Assets/Audio/level' + str(current_level) + '.ogg')
        self.levelMusic.set_volume(0.1)  # Abbassa il volume della musica
        self.levelMusic.play(loops=-1)

    def CreateOverworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(current_level, self.max_level, screen, self.CreateLevel)
        self.status = 'overworld'
        self.overworldMusic.play(loops=-1)
        self.levelMusic.stop()

    def ChangePlayerHealth(self, amount):
        self.playerCurrentHealth += amount
        if self.playerCurrentHealth > self.playerMaxHealth:
            self.playerCurrentHealth = self.playerMaxHealth

    def CheckGameOver(self):
        if self.playerCurrentHealth <= 0:
            self.playerCurrentHealth = self.playerMaxHealth
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.CreateLevel)
            self.status = 'overworld'
            self.levelMusic.stop()
            self.overworldMusic.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.RunGame()
            self.ui.ShowHealthBar(self.playerCurrentHealth, self.playerMaxHealth)
            self.CheckGameOver()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
