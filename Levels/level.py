import pygame

from playerOne import PlayerOne
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
                    player_sprite = PlayerOne((x, y))
                    self.player.add(player_sprite)

    def scroll_map_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.xPosition

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.defaultSpeed

    def run(self):
        # Fa l'update dello schermo
        self.tiles.update(self.world_shift)

        # Disegna il livello
        self.tiles.draw(self.display_surface)

        # Disegna il giocatore
        self.player.draw(self.display_surface)

        # Update input giocatore
        self.player.update()

        # Fa l'update della camera che segue il giocatore
        self.scroll_map_x()