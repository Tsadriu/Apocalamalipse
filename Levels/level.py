import pygame

from player import Player
from tiles import Tile
from settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):

        # Level setup
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                # Calcola posizione X e Y
                x = column_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_map_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.xInput

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.defaultSpeed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.xInput * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.xInput < 0:
                    player.rect.left = sprite.rect.right
                elif player.xInput > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.yInput < 0:
                    player.rect.top = sprite.rect.bottom
                    player.yInput = 0  # Quando picchio la testa, torna subito giù
                elif player.yInput > 0:
                    player.rect.bottom = sprite.rect.top
                    player.yInput = 0
                    player.canJump = True

    def run(self):
        # Fa l'update dello schermo
        self.tiles.update(self.world_shift)

        # Disegna il livello
        self.tiles.draw(self.display_surface)

        # Fa l'update della camera che segue il giocatore
        self.scroll_map_x()

        # Update input giocatore
        self.player.update()

        # Muove il giocatore in orizzontale e controlla le collisioni avvenute
        self.horizontal_movement_collision()

        # Muove il giocatore in verticale e controlla le collisioni avvenute
        self.vertical_movement_collision()

        # Disegna il giocatore
        self.player.draw(self.display_surface)
