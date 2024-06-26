from os import walk
import pygame


def import_folder(path):  # importing the files of the game
    surface_list = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + "/" + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
