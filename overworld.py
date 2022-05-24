import pygame
from gameData import levels
from support import ImportFolderContent
from decoration import BackGround


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, worldStatus, icon_speed, path):
        super().__init__()
        self.frames = ImportFolderContent(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        if worldStatus == 'available':
            self.worldStatus = 'available'
        else:
            self.worldStatus = 'locked'
        self.rect = self.image.get_rect(center=pos)
        self.xDetection = self.rect.centerx - (icon_speed / 2);
        self.yDetection = self.rect.centery - (icon_speed / 2);
        self.detection_zone = pygame.Rect(self.xDetection, self.yDetection, icon_speed, icon_speed)

    def AnimateLevels(self):
        self.frameIndex += 0.05
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    # Fa l'update delle animazioni dei livelli
    def update(self):
        if self.worldStatus == 'available':
            self.AnimateLevels()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('red', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.image.load('Assets/Art/character/skull.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position


class Overworld:
    def __init__(self, startLevel, maxUnlockableLevel, surface, createdLevel):

        self.display_surface = surface
        self.maxLevel = maxUnlockableLevel
        self.currentLevel = startLevel
        self.createdLevel = createdLevel

        self.IsMoving = False
        self.MovementDirection = pygame.math.Vector2(0, 0)
        self.speed = 7.5

        self.SetNodes()
        self.SetupIcon()
        self.sky = BackGround(8, 'overworld')

        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 200

    # Sono le posizioni dove appaiono i livelli
    def SetNodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.maxLevel:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def SetupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(icon_sprite)

    def GetPlayerInputToSelectLevel(self):
        keys = pygame.key.get_pressed()

        if not self.IsMoving and self.allow_input:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_UP]) and self.currentLevel < self.maxLevel:
                self.MovementDirection = self.GetMovement('next')
                self.currentLevel += 1
                self.IsMoving = True
            elif (keys[pygame.K_LEFT] or keys[pygame.K_DOWN]) and self.currentLevel > 0:
                self.MovementDirection = self.GetMovement('previous')
                self.currentLevel -= 1
                self.IsMoving = True
            elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.createdLevel(self.currentLevel)

    def InputCooldown(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def GetMovement(self, target):
        posStart = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        posEnd = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1 if target == 'next' else self.currentLevel - 1].rect.center)
        return (posEnd - posStart).normalize()

    def MovePlayerIcon(self):
        if self.IsMoving and self.MovementDirection:
            self.icon.sprite.position += self.MovementDirection * self.speed
            position = self.nodes.sprites()[self.currentLevel]

            if position.detection_zone.collidepoint(self.icon.sprite.position):
                self.IsMoving = False
                self.MovementDirection = pygame.math.Vector2(0, 0)

    def RunOverworld(self):
        # Non fa ricevere input dal giocatore dopo essersi mosso da un livello all'altro
        self.InputCooldown()
        # Ricevere input per selezionare il livello
        self.GetPlayerInputToSelectLevel()

        self.MovePlayerIcon()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
