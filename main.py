import pygame
import sys

# Pygame setup
pygame.init()
screen_width = 1200
screen_height = 700

# Sets the screen width and height
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        # If we got the event of quitting the game, close the application
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill('black')

        # Updates the window
        pygame.display.update()

        # Put the game's frames per second (FPS) to 60
        clock.tick(60)
