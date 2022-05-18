from csv import reader
from settings import tileSize
from os import walk
import pygame


def ImportFolderContent(path):
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
    with open(path) as currentMap:
        level = reader(currentMap, delimiter=',')
        for row in level:
            levelMap.append(list(row))
        return levelMap


# Taglia l'immagine del terreno_tiles così abbiamo gli indici
def ImportMapGraphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tileX = int(surface.get_size()[0] / tileSize)
    tileY = int(surface.get_size()[1] / tileSize)

    mapTiles = []
    for row in range(tileY):
        for column in range(tileX):
            x = column * tileSize
            y = row * tileSize
            newSurface = pygame.Surface((tileSize, tileSize), flags=pygame.SRCALPHA)
            newSurface.blit(surface, (0, 0), pygame.Rect(x, y, tileSize, tileSize))
            mapTiles.append(newSurface)

    return mapTiles
