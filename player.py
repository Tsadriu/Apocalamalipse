import pygame
import random

from support import import_folder


class Player(pygame.sprite.Sprite):
    # È l'equivalente del costruttore di Java
    def __init__(self, position):
        super().__init__()
        # Dizionario
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
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
        self.defaultSpeed = 6
        self.speed = self.defaultSpeed
        self.gravity = 0.8
        self.jumpSpeed = -18
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onWallLeft = False
        self.onWallRight = False

        # Stato del giocatore (sta correndo, è fermo, sta saltando...)
        self.status = 'idle'

    def import_character_assets(self):
        selected_character = random.randint(1, 5)
        character_path = 'assets/art/characters/player/' + str(selected_character) + '/'

        for animation in self.animations.keys():
            # Sarebbe /asset/art/characters/1/player/idle, ecc
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
        image = animation[int(self.frame_index)]

        if self.facingRight:
            self.image = image
        else:
            #                                            X     Y
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # Imposta il rect del giocatore (l'hitbox)
        if self.onGround and self.onWallRight:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.onGround and self.onWallLeft:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.onCeiling and self.onWallRight:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.onCeiling and self.onWallLeft:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    # Prendi l'input dell'utente
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.xInput = 1
            self.facingRight = True
        elif keys[pygame.K_LEFT]:
            self.xInput = -1
            self.facingRight = False
        else:
            self.xInput = 0

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.onGround:
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

    def set_gravity(self, amount):
        if amount is not None:
            self.gravity = amount

    def jump(self):
        self.yInput = self.jumpSpeed

    def update(self, timer):
        self.input()
        self.get_player_status()
        self.animate()
        self.set_gravity(timer)
