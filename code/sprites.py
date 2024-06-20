
import pygame
from settings import *


class Generic(pygame.sprite.Sprite):  # generic class for all sprites
    def __init__(self, pos, surf, groups, z=LAYERS['background']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().move(0, -30).inflate(-16, -16)


class Weapon(pygame.sprite.Sprite):  # weapon class for displaying the weapon
    def __init__(self, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(center=player.rect.center)
        self.z = LAYERS['weapon']
        direction = player.status.split('_')[0]

        full_path = f"./assets/graphics/Player/weapons/{
            player.selected_weapon}/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        if direction == 'up':
            self.rect.midtop = player.rect.midtop
        if direction == 'down':
            self.rect.midbottom = player.rect.midbottom
        if direction == 'left':
            self.rect.midleft = player.rect.midleft
        if direction == 'right':
            self.rect.midright = player.rect.midright
