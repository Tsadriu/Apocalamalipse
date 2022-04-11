import pygame
import random
from support import import_folder


class Player(pygame.sprite.Sprite):
    # È l'equivalente del costruttore di Java
    def __init__(self, position):
        super().__init__()
        # Importare le sprite del giocatore
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # Dimensione sprite personaggio
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        # Input Giocatore
        self.xInput = 0
        self.yInput = 0

        # Movimento del giocatore
        self.defaultSpeed = 5
        self.speed = self.defaultSpeed
        self.gravity = 0.8
        self.jumpSpeed = -16
        self.canJump = True

        # Stato del giocatore (sta correndo, è fermo, sta saltando...)
        self.status = 'idle'

    def import_character_assets(self):
        selected_character = random.randint(1, 4)
        character_path = 'assets/art/characters/player/' + str(selected_character) + '/'

        # Dizionario
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            # Sarebbe /asset/art/characters/player/idle, ecc
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # Cicla nella quantità di sprite
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Facciamo un cast in int del frame_index, perché sopra facciamo la somma con l'animation_speed (0.13)
        # Così determiniamo la velocità del frame. Più basso è il numero, e più ci mette a passare da un'immagine all'altra
        self.image = animation[int(self.frame_index)]

    # Prendi l'input dell'utente
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.xInput = 1
        elif keys[pygame.K_LEFT]:
            self.xInput = -1
        else:
            self.xInput = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()

    def get_player_status(self):
        if self.yInput < 0:
            self.status = 'jump'
        elif self.yInput > 1:
            self.status = 'fall'
        else:
            if self.xInput != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.yInput += self.gravity
        self.rect.y += self.yInput

    def jump(self):
        if self.canJump:
            self.yInput = self.jumpSpeed
            self.canJump = False

    def update(self):
        self.input()
        self.get_player_status()
        self.animate()