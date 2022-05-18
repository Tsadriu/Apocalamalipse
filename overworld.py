import pygame
from gameData import levels
from support import import_folder
from decoration import BackGround


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, worldStatus, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if worldStatus == 'available':
            self.worldStatus = 'available'
        else:
            self.worldStatus = 'locked'
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2),
                                          icon_speed, icon_speed)

    def AnimateLevels(self):
        self.frame_index += 0.05
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.worldStatus == 'available':
            self.AnimateLevels()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('red', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('Assets/Art/character/skull.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, startLevel, maxUnlockableLevel, surface, createdLevel):

        # setup
        self.display_surface = surface
        self.max_level = maxUnlockableLevel
        self.current_level = startLevel
        self.create_level = createdLevel

        # movement
        self.IsMoving = False
        self.MovementDirection = pygame.math.Vector2(0, 0)
        self.speed = 7

        # sprites
        self.SetNodes()
        self.SetupIcon()
        self.sky = BackGround(8, 'overworld')

        # timer
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 200

    # Sono le posizioni dove appaiono i livelli
    def SetNodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def SetupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def GetPlayerInputToSelectLevel(self):
        keys = pygame.key.get_pressed()

        if not self.IsMoving and self.allow_input:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_UP]) and self.current_level < self.max_level:
                self.MovementDirection = self.GetMovData('next')
                self.current_level += 1
                self.IsMoving = True
            elif (keys[pygame.K_LEFT] or keys[pygame.K_DOWN]) and self.current_level > 0:
                self.MovementDirection = self.GetMovData('previous')
                self.current_level -= 1
                self.IsMoving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def GetMovData(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        elif target == 'previous':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def MovePlayerIcon(self):
        if self.IsMoving and self.MovementDirection:
            self.icon.sprite.pos += self.MovementDirection * self.speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.IsMoving = False
                self.MovementDirection = pygame.math.Vector2(0, 0)

    def InputCooldown(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

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
