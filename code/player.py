import pygame
from settings import *
from support import *
from asyn import Asyn
from entity import Entity


class Player(Entity):  # player class
    def __init__(self, pos, group, collision_sprites, create_attack, destroy_attack):
        # initializing the player class with the group of sprites it belongs to
        super().__init__(group)

        # player animations
        self.import_assets()  # importing the assets of the player
        self.image = self.animations[self.status][self.frame_index]

        # player properties
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['player']
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.isattack = False

        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate(-130, -80)

        # timers
        self.timers = {
            'use weapon': Asyn(370, self.destroy_attack),
            'weapon change': Asyn(200),
            'potion_change': Asyn(200),
            'potion_use': Asyn(2000)
        }

        # weapons
        self.weapon_index = 0
        self.selected_weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.damage = WEAPON_DATA[self.selected_weapon]['damage']

        # health & status
        self.health = 100
        self.effects = None

        # inventory & money
        self.inventory_index = 0
        self.selected_potion = list(INVENTORY_DATA.keys())[
            self.inventory_index]
        self.money = 0

    def import_assets(self):  # importing the assets of the player
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}
        for animation in self.animations.keys():
            full_path = "./assets/graphics/Player/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):  # animating the player
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):  # all the inputs of the player
        keys = pygame.key.get_pressed()
        if (not self.timers['use weapon'].active):
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if not self.timers['weapon change'].active:
                # weapon use
                if keys[pygame.K_SPACE]:
                    self.timers['use weapon'].activate()
                    self.frame_index = 0
                    self.isattack = True

                    # change weapon
                if keys[pygame.K_LCTRL] and not self.timers['weapon change'].active:
                    self.timers['weapon change'].activate()
                    self.weapon_index += 1
                    if self.weapon_index >= len(list(WEAPON_DATA.keys())):
                        self.weapon_index = 0
                    self.selected_weapon = list(WEAPON_DATA.keys())[
                        self.weapon_index]
            # potion use and change
            if not self.timers['potion_change'].active:
                if keys[pygame.K_1]:
                    self.timers['potion_change'].activate()
                    self.inventory_index += 1
                    if self.inventory_index >= len(list(INVENTORY_DATA.keys())):
                        self.inventory_index = 0
                    self.selected_potion = list(INVENTORY_DATA.keys())[
                        self.inventory_index]
                # potion use
                if keys[pygame.K_2] and (not self.timers['potion_use'].active):
                    if INVENTORY_DATA[self.selected_potion]['amount'] > 0:
                        self.timers['potion_use'].activate()
                        if self.selected_potion == 'health_potion':
                            self.health += INVENTORY_DATA[self.selected_potion]['value']
                            INVENTORY_DATA[self.selected_potion]['amount'] -= 1
                            if self.health > 100:
                                self.health = 100
                        elif INVENTORY_DATA[self.selected_potion]['type'] == 'potion':
                            self.effects = INVENTORY_DATA[self.selected_potion]["effect"]
                            INVENTORY_DATA[self.selected_potion]['amount'] -= 1
        else:
            self.direction = pygame.math.Vector2()
    # moving the player

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # weapon Use
        if self.timers['use weapon'].active and self.isattack == True:
            # make attack anim here------------------------------------------------------
            self.create_attack()
            self.isattack = False

    # applying the effects of the potions, and clearing them
    def clear_effects(self):
        if not self.timers['potion_use'].active:
            self.effects = None
            self.damage = WEAPON_DATA[self.selected_weapon]['damage']
            self.speed = 300
        else:
            if self.effects == 'damage_up':
                self.damage = WEAPON_DATA[self.selected_weapon]['damage'] * \
                    INVENTORY_DATA[self.selected_potion]['value']
            if self.effects == 'speed_up':
                self.speed = 300 + \
                    INVENTORY_DATA[self.selected_potion]['value']
            if self.effects == 'speed_up':
                self.speed = 300 + \
                    INVENTORY_DATA[self.selected_potion]['value']

    # updating the timers
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    # Updating the player
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.clear_effects()
        self.move(dt)
        self.animate(dt)
