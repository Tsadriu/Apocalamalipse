import pygame
import sys
import player
import settings
from settings import *
from level import Level

# Pygame setup
pygame.init()
screen_width = settings.screen_width
screen_height = settings.screen_height

# Sets the screen width and height
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

# Timer
font = pygame.font.SysFont("Consolas", 100)
counter = 60
text = font.render(str(counter), True, 'Yellow')

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)


def gravity_modifier(timer):
    default_gravity = 1.6
    amount = timer / 100
    print("gravity: " + str(default_gravity - amount))
    return default_gravity - amount


text_rect = text.get_rect(topleft=screen.get_rect().topleft)
while True:
    gravity = gravity_modifier(counter)
    for event in pygame.event.get():
        # If we got the event of quitting the game, close the application
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == timer_event:
            counter -= 1
            text = font.render(str(counter), True, 'Yellow')
            text_rect = text.get_rect(topleft=screen.get_rect().topleft)
            if counter == 0:
                pygame.time.set_timer(timer_event, 0)
                text = font.render('You suck', True, 'Red')
                text_rect = text.get_rect(center=screen.get_rect().center)

    screen.fill('black')

    # Esegui l'update del livello
    level.run(gravity_modifier(counter))

    screen.blit(text, text_rect)

    # Updates the window
    pygame.display.update()

    # Put the game's frames per second (FPS) to 60
    clock.tick(60)
