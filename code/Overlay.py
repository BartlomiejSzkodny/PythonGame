import pygame
from settings import *
from sprites import Generic


class overlay:
    def __init__(self, player, visited_rooms, level):
        # setup

        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.visited_rooms = visited_rooms
        self.level = level
        # weapon selected
        overlay_path = "./assets/graphics/Overlay/"
        self.weapons_surf = {weapon: pygame.image.load(
            f'{overlay_path}{weapon}.png').convert_alpha() for weapon in list(WEAPON_DATA.keys())}

        # minimap
        overlay_path = "./assets/graphics/minimap/"
        self.map_part = {part: pygame.image.load(
            f'{overlay_path}{part}.png').convert_alpha() for part in ["U", "UL", "UR", "UD", "ULR", "ULD", "URD", "ULRD",
                                                                      "L", "LR", "LD", "LRD",
                                                                      "R", "RD",
                                                                      "D",
                                                                      "U-S", "UL-S", "UR-S", "UD-S", "ULR-S", "ULD-S", "URD-S", "ULRD-S",
                                                                      "L-S", "LR-S", "LD-S", "LRD-S",
                                                                      "R-S", "RD-S",
                                                                      "D-S", "U-I", "U-B", "L-I", "L-B", "R-I", "R-B", "D-I", "D-B"]}

        self.playerIndicator = pygame.image.load(
            overlay_path + "playerIndicator.png").convert_alpha()

    def display(self, player):
        # health
        self.display_surface.blit(pygame.font.Font('freesansbold.ttf', 32).render(
            "Hp: "+str(round(player.health)), True, (255, 255, 255)), (10, 124))

        # money
        self.display_surface.blit(pygame.font.Font('freesansbold.ttf', 32).render(
            "$ "+str(player.money), True, (255, 255, 255)), (10, 92))

        # weapon
        weapon_surf = self.weapons_surf[self.player.selected_weapon]
        self.display_surface.blit(weapon_surf, (16, 16))

        # inventory
        self.display_surface.blit(pygame.font.Font('freesansbold.ttf', 32).render(
            str(player.selected_potion)+" "+str(INVENTORY_DATA[player.selected_potion]['amount']), True, (255, 255, 255)), (10, 160))

        # minimap
        for room in self.visited_rooms:
            room_to_display = self.map_part[room[2]]
            self.display_surface.blit(
                room_to_display, (WIDTH_screen - 26*5 + room[1]*26, room[0]*18))
        self.display_surface.blit(
            self.playerIndicator, (WIDTH_screen - 26*5 + self.level.current_room[1]*26, self.level.current_room[0]*18))
