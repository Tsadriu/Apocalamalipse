import pygame

class PlayerOne(pygame.sprite.Sprite):
    # È l'equivalente del costruttore di Java
    def __init__(self, position):
        super().__init__()
        # Dimensione sprite personaggio
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=position)

        # Movimento del giocatore
        self.xPosition = 0
        self.yPosition = 0
        self.defaultSpeed = 5
        self.speed = self.defaultSpeed
        self.gravity = 0.8
        self.jumpSpeed = -16
        self.canJump = True;

    # Prendi l'input dell'utente
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.xPosition = 1
        elif keys[pygame.K_LEFT]:
            self.xPosition = -1
        else:
            self.xPosition = 0

        if keys[pygame.K_UP]:
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

