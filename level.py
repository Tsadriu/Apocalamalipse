import pygame
import random

from support import ImportCsvFile, import_cut_graphics
from settings import tileSize, screenHeight, screenWidth
from tiles import Tile, StaticTile, Spike, Cherry
from enemy import Enemy
from decoration import Sky, Lava
from player import Player
from gameData import levels


class Level:
    def __init__(self, current_level, surface, createOverworld, changeHealth):
        # general setup
        self.display_surface = surface
        self.worldShift = 0
        self.current_x = None

        # Audio
        self.cherrySounds = pygame.mixer.Sound('Assets/Audio/effects/cherry.wav')
        self.victorySound = pygame.mixer.Sound('Assets/Audio/effects/win.wav')
        self.enemyDeath = pygame.mixer.Sound('Assets/Audio/effects/enemy_death.wav')
        self.enemyDeath.set_volume(0.2)

        # overworld connection
        self.currentOverworld = createOverworld
        self.currentLevel = current_level
        levelData = levels[self.currentLevel]
        self.unlockedMaxLevel = levelData['unlock']

        # player
        player_layout = ImportCsvFile(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.SetupPlayer(player_layout, changeHealth)
        self.playerOnGround = False

        # terrain setup
        terrain_layout = ImportCsvFile(levelData['terrain'])
        self.terrain_sprites = self.CreateTileGroup(terrain_layout, 'terrain')

        # Spikes
        spikesLayout = ImportCsvFile(levelData['spikes'])
        self.spikeSprites = self.CreateTileGroup(spikesLayout, 'spikes')

        # cherry
        cherryLayout = ImportCsvFile(levelData['cherry'])
        self.cherrySprites = self.CreateTileGroup(cherryLayout, 'cherry')

        # enemy
        enemyLayout = ImportCsvFile(levelData['enemies'])
        self.enemySprites = self.CreateTileGroup(enemyLayout, 'enemies')

        # enemylimit
        enemyLimitLayout = ImportCsvFile(levelData['enemyLimit'])
        self.constraint_sprites = self.CreateTileGroup(enemyLimitLayout, 'enemyLimit')

        # decoration
        self.sky = Sky(8)
        levelWidth = len(terrain_layout[0]) * tileSize
        self.lava = Lava(screenHeight - 20, levelWidth)

    def CreateTileGroup(self, layout, typeOfTile):
        spriteGroup = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tileSize
                    y = row_index * tileSize

                    if typeOfTile == 'enemies':
                        sprite = Enemy(tileSize, x, y)

                    if typeOfTile == 'terrain':
                        terrain_tile_list = import_cut_graphics('Assets/Art/terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tile_surface)

                    if typeOfTile == 'spikes':
                        sprite = Spike(tileSize, x, y)

                    if typeOfTile == 'cherry':
                        sprite = Cherry(tileSize, x, y, 'Assets/Art/cherry/sprites', 5)

                    if typeOfTile == 'enemyLimit':
                        sprite = Tile(tileSize, x, y)

                    spriteGroup.add(sprite)

        return spriteGroup

    def SetupPlayer(self, layout, changeHealth):
        for rowIndex, row in enumerate(layout):
            for columnIndex, value in enumerate(row):
                x = columnIndex * tileSize
                y = rowIndex * tileSize
                if value == '0':
                    sprite = Player((x, y), changeHealth)
                    self.player.add(sprite)
                if value == '1':
                    skullEndLevel = pygame.image.load('Assets/Art/character/skull.png').convert_alpha()
                    sprite = StaticTile(tileSize, x, y, skullEndLevel)
                    self.goal.add(sprite)

    def FlipEnemyEdgeSprite(self):
        for enemy in self.enemySprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.ReverseX()

    def CheckHorizontalCollision(self):
        player = self.player.sprite
        player.collisionRectangle.x += player.direction.x * player.movSpeed
        # Cosa può 'toccare' il giocatore. Cosa non viene specificato farà 'teletrasportare' il giocatore
        # per evitare che entri dentro la sprite
        spritesThatCanCollide = self.terrain_sprites.sprites() # + self.spike_sprites.sprites()
        for sprite in spritesThatCanCollide:
            if sprite.rect.colliderect(player.collisionRectangle):
                if player.direction.x < 0:
                    player.collisionRectangle.left = sprite.rect.right
                    player.onLeftWall = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collisionRectangle.right = sprite.rect.left
                    player.onRightWall = True
                    self.current_x = player.rect.right

    def CheckVertivalCollision(self):
        player = self.player.sprite
        player.ApplyGravity()
        collidable_sprites = self.terrain_sprites.sprites() # + self.spike_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collisionRectangle):
                if player.direction.y > 0:
                    player.collisionRectangle.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.collisionRectangle.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False

    def ScrollMapX(self):
        player = self.player.sprite
        playerPositionX = player.rect.centerx
        playerDirectionX = player.direction.x

        if playerPositionX < screenWidth / 4 and playerDirectionX < 0:
            self.worldShift = Player.movSpeed
            player.movSpeed = 0
        elif playerPositionX > screenWidth - (screenWidth / 4) and playerDirectionX > 0:
            self.worldShift = -Player.movSpeed
            player.movSpeed = 0
        else:
            self.worldShift = 0
            player.movSpeed = Player.movSpeed

    def IsPlayerOnGround(self):
        if self.player.sprite.onGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

    def CheckPlayerWin(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.victorySound.set_volume(0.2)
            self.victorySound.play()
            self.currentOverworld(self.currentLevel, self.unlockedMaxLevel)

    def CheckPlayerDeath(self):
        if self.player.sprite.rect.top > screenHeight:
            self.currentOverworld(self.currentLevel, 0)

    def CheckCherryCollisions(self):
        collidedCherries = pygame.sprite.spritecollide(self.player.sprite, self.cherrySprites, True)
        if collidedCherries:
            for cherry in collidedCherries:
                cherry.kill()
                self.cherrySounds.play()
                self.player.sprite.GetHeal()

    def CheckEnemyCollisions(self):
        collidedEnemies = pygame.sprite.spritecollide(self.player.sprite, self.enemySprites, False)
        if collidedEnemies:
            for enemy in collidedEnemies:
                enemyCenter = enemy.rect.centery
                enemyTop = enemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    self.enemyDeath.play()
                    self.player.sprite.direction.y = -8.25 # Fai saltare il giocatore
                    enemy.Die()
                else:
                    self.player.sprite.GetDamage(enemy.damage)

    def CheckSpikeCollisions(self):
        spikeCollisions = pygame.sprite.spritecollide(self.player.sprite, self.spikeSprites, False)

        if spikeCollisions:
            for spike in spikeCollisions:
                self.player.sprite.GetDamage(spike.damage)

    def RunGame(self):
        # Questo esegue un update di praticamente tutto il gioco
        # sky
        self.sky.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.worldShift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemySprites.update(self.worldShift)
        self.constraint_sprites.update(self.worldShift)
        # Gira il nemico quando arriva nell'angolo della sprite
        self.FlipEnemyEdgeSprite()
        self.enemySprites.draw(self.display_surface)

        # Spikes
        self.spikeSprites.update(self.worldShift)
        self.spikeSprites.draw(self.display_surface)

        # coins
        self.cherrySprites.update(self.worldShift)
        self.cherrySprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.CheckHorizontalCollision()

        self.IsPlayerOnGround()
        self.CheckVertivalCollision()

        self.ScrollMapX()
        self.player.draw(self.display_surface)
        self.goal.update(self.worldShift)
        self.goal.draw(self.display_surface)

        self.CheckPlayerDeath()
        self.CheckPlayerWin()

        self.CheckCherryCollisions()
        self.CheckEnemyCollisions()
        self.CheckSpikeCollisions()

        # water
        self.lava.draw(self.display_surface, self.worldShift)
