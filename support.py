from os import walk  # Aggiunge molte funzionalità del sistema
# Walk ritorna il percorso, il nome del percorso e i nomi dei file all'interno del percorso passato
import pygame


def import_folder(path):
    surface_list = []

    for _, _, sheets in walk(path):
        for sheet in sheets:
            full_path = path + '/' + sheet
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
