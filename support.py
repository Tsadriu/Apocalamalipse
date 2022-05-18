from csv import reader
from settings import tileSize
from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


# Legge il file csv
def ImportCsvFile(path):
    levelMap = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            levelMap.append(list(row))
        return levelMap


# Taglia l'immagine del terreno_tiles così abbiamo gli indici
def ImportMapGraphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tileSize)
    tile_num_y = int(surface.get_size()[1] / tileSize)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tileSize
            y = row * tileSize
            new_surf = pygame.Surface((tileSize, tileSize), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tileSize, tileSize))
            cut_tiles.append(new_surf)

    return cut_tiles
