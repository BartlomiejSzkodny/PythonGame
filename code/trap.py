from entity import Entity
import pygame
from support import import_folder
from settings import LAYERS, TILE_SIZE
# trap


class Trap(Entity):
    def __init__(self, trap_name, pos, groups):
        super().__init__(groups)
        self.import_graphic(trap_name)
        self.status = 'idle'
        self.image = self.animations["idle"][self.frame_index]
        self.z = LAYERS['walls']
        self.rect = self.image.get_rect(topleft=pos).inflate(0, 5)

    def import_graphic(self, name):
        self.animations = {'idle': []}
        for animation in self.animations.keys():
            full_path = f"./assets/graphics/traps/{name}/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
