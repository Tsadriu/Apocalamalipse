import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    movSpeed = 6.5
    def __init__(self, pos, currentHealth, currentLevel):
        super().__init__()
        self.ImportCharacterSprites(currentLevel)
        self.currentFrameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.currentFrameIndex]
        self.rect = self.image.get_rect(topleft=pos)

        # Movimento del giocatore
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.685 # Più è basso il numero e più alto salta il giocatore
        self.jumpSpeed = -14.25 # Più è basso il numero e più è veloce sarà il giocatore a saltare in verticale
        self.collisionRectangle = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        # Lo stato del giocatore (se è ferma, che direzione sta guardando, con cosa è in contatto, ecc.)
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeftWall = False
        self.onRightWall = False

        # Vita/tempo di invulnerabilità e CD dell'invulnerabilità.
        self.currentHealth = currentHealth
        self.invulnerability = False # Viene usato quando il giocatore viene colpito, altrimenti in un frame viene insta-one shottato
        self.invulnerabilityLength = 650 # 0.65 secondi dovrebbe essere abbastanza tempo per l'invulnerabilità (rende il gioco difficile )
        self.hurtTime = 0 # Viene usata per sapere quando il giocatore è stato danneggiato

        # Audio del giocatore
        self.playerJumpSound = pygame.mixer.Sound('Assets/Audio/effects/jump.wav')
        self.playerJumpSound.set_volume(0.2)
        self.playerHitSound = pygame.mixer.Sound('Assets/Audio/effects/hit.wav')
        self.playerHitSound.set_volume(0.2)

    def ImportCharacterSprites(self, currentLevel):
        #selectedCharacter = random.randint(1, 5) # Prendi un dinosauro a caso
        selectedCharacter = (currentLevel + 1)
        resourcePath = 'Assets/Art/character/' + str(selectedCharacter) + '/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            fullPath = resourcePath + animation
            self.animations[animation] = import_folder(fullPath)

    def UpdateAnimation(self):
        animation = self.animations[self.status]

        # Cicla nella quantità di sprite
        self.currentFrameIndex += self.animationSpeed
        if self.currentFrameIndex >= len(animation):
            self.currentFrameIndex = 0

        # Facciamo un cast in int del frame_index, perché sopra facciamo la somma con l'animation_speed (0.13)
        # Così determiniamo la velocità del frame. Più basso è il numero, e più ci mette a passare da un'immagine all'altra
        image = animation[int(self.currentFrameIndex)]

        if self.facingRight:
            self.image = image
            self.rect.bottomleft = self.collisionRectangle.bottomleft
        else:
            #                                            X     Y
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collisionRectangle.bottomright

        if self.invulnerability:
            self.image.set_alpha(50)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def GetUserInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facingRight = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facingRight = False
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.onGround:
            self.Jump()

    def GetCharacterStatus(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def ApplyGravity(self):
        self.direction.y += self.gravity
        self.collisionRectangle.y += self.direction.y

    def Jump(self):
        self.direction.y = self.jumpSpeed
        self.playerJumpSound.play()

    def GetDamage(self, amount):
        if not self.invulnerability:
            self.playerHitSound.play()
            self.currentHealth(-amount)
            self.invulnerability = True
            self.hurtTime = pygame.time.get_ticks()

    def GetHeal(self, amount):
        self.currentHealth(amount)

    def InvulnerabilityTimer(self):
        if self.invulnerability: # Se il giocatore è sotto l'effetto di invibilità
            currentTime = pygame.time.get_ticks() # Prendi il tempo corrente
            if currentTime - self.hurtTime >= self.invulnerabilityLength: # Se il tempo corrente - il tempo quando il giocatore è entrato in contatto col nemico >= della lunghezza
                self.invulnerability = False                              # dell'invincibilità, togli.

    def update(self):
        #Prende l'input del giocatore
        self.GetUserInput()
        # Prende lo stato del giocatore (sta saltando, cadendo, ecc)
        self.GetCharacterStatus()
        # Fa l'update delle animazioni (loop infinito)
        self.UpdateAnimation()
        # Fa il countdown del tempo dell'invulnerabilità
        self.InvulnerabilityTimer()
