import pygame
from support import import_folder


class PlayerOne(pygame.sprite.Sprite):
    # È l'equivalente del costruttore di Java
    def __init__(self, position):
        super().__init__()
        # Importare le sprite del giocatore
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.13
        # Dimensione sprite personaggio
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)

        # Movimento del giocatore
        self.xPosition = 0
        self.yPosition = 0
        self.defaultSpeed = 5
        self.speed = self.defaultSpeed
        self.gravity = 0.8
        self.jumpSpeed = -16
        self.canJump = True

    def import_character_assets(self):
        character_path = 'assets/art/characters/player/'
        # Dizionario
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            # Sarebbe /asset/art/characters/player/idle, ecc
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # Prendi l'input dell'utente
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.xPosition = 1
        elif keys[pygame.K_LEFT]:
            self.xPosition = -1
        else:
            self.xPosition = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.yPosition += self.gravity
        self.rect.y += self.yPosition

    def jump(self):
        if self.canJump:
            self.yPosition = self.jumpSpeed
            self.canJump = False

    def update(self):
        self.input()
