import pygame
from settings import *
from entity import Entity
from support import import_folder


class Monster(Entity):
    def __init__(self, monster_name, pos, groups, collision_sprites, attack_func):
        # initializing the monster class with the group of sprites it belongs to
        super().__init__(groups)
        self.sprite_type = "monster"
        self.z = LAYERS['player']
        self.status = 'up'

        # monster animations
        self.import_graphic(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy().inflate(0, -10)
        self.collision_sprites = collision_sprites

        # monster properties
        self.attack = attack_func
        self.monster_name = monster_name
        monster_info = MONSTER_DATA[self.monster_name]
        self.health = monster_info['health']
        self.gold = monster_info['gold']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.loot_table = monster_info['loot_table']
        self.attack_time = 0
        self.attack_cooldown = 1000

        # monster status
        self.move_flag = False
        self.can_attack = True

    def import_graphic(self, name):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [
        ], 'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
        for animation in self.animations.keys():
            full_path = f"./assets/graphics/monsters/{name}/" + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance(player)
        if (distance[0] < self.attack_radius) and self.can_attack:
            if "attack" not in self.status:
                self.frame_index = 0
            self.status = self.status.split('_')[0] + '_attack'

        elif distance[0] < self.notice_radius:
            if abs(distance[1][0]) > abs(distance[1][1]):
                if distance[1][0] > 0:
                    self.status = 'right'
                else:
                    self.status = 'left'
            elif abs(distance[1][0]) <= abs(distance[1][1]):
                if distance[1][1] >= 0:
                    self.status = 'down'
                else:
                    self.status = 'up'
            self.move_flag = True

        else:
            self.status = 'down'
            self.move_flag = False

    def actions(self, player):
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
        if self.move_flag:
            self.direction = self.get_player_distance(player)[1]
        if not self.move_flag:
            self.direction = pygame.math.Vector2(0, 0)

    def animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = False
                print("attacked")
                self.attack(self.damage)
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def attack_cooldown_timer(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time > self.attack_cooldown:
                self.can_attack = True

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.attack_cooldown_timer()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
