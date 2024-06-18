from settings import *
from player import Player
from Overlay import overlay
from sprites import Generic, Weapon
from enemy import Monster
from trap import Trap
from boss import Boss
from generator import LevelGenerationComplete

import pygame
from pytmx.util_pygame import load_pygame
import re
import concurrent.futures
import random

# setting up the level - this is where the player will be spawned, the enemies will be spawned, etc


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()  # seting up the screen
        # setting up the allsprites, this is where all the sprites will be stored
        self.allsprites = cameraGroup()
        self.collision_sprites = pygame.sprite.Group()  # setting up the collision sprites
        self.doors = pygame.sprite.Group()  # setting up the doors
        self.enemy_positio = {}
        self.trap_positio = {}

        self.setup()  # setting up the level - this is where the player will be spawned, the enemies will be spawned, etc

        self.previous = [0, 0]
        self.visited_rooms = []
        self.current_room = [-2, -2]

        self.list_of_enemies = []

        # setting up the overlay, this is where the player's health will be displayed and camera will be displayed
        self.overlay = overlay(
            self.player, self.visited_rooms, self)

        # setting up the variables, these variables will be used to control the game
        self.CloseDoors = False
        self.OpenDoors = False
        self.encounter = False
        self.EnterBossRoom = False
        self.newFloor = False
        self.current_attack = None

        # setting up the groups, these groups will be used to store the sprites
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.trap_sprites = pygame.sprite.Group()

    def setup(self):  # setting up the level

        # loading the map from the assets folder in tmx format, i used concurrent.futures to load the map and the level generation at the same time
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_tmx = executor.submit(
                load_pygame, '../PythonGame/assets/tileset/map.tmx')
            future_level_gen = executor.submit(LevelGenerationComplete)

            # Retrieve the results once both functions have completed
            self.tmx_data = future_tmx.result()
            self.plain = [[0 for i in range(5)] for j in range(5)]
            self.plain, spawn_i, spawn_j = future_level_gen.result()

        # print(self.plain) how the rooms are connected
        for i in self.plain:
            print("\t".join(map(str, i)))
        for i, _ in enumerate(self.plain):
            for j, Name in enumerate(_):
                if Name == 0:
                    Name = '0'  # 0 is the name of the empty space
                if Name != '0':
                    for x, y, surf in self.tmx_data.get_layer_by_name(Name).tiles():
                        Generic(  # import all walls
                            ((x % ROOM_WIDTH)*TILE_SIZE+(j-1)*ROOM_WIDTH*TILE_SIZE,
                             (y % ROOM_HEIGHT)*TILE_SIZE+(i-1)*ROOM_HEIGHT*TILE_SIZE),
                            surf,
                            [self.allsprites, self.collision_sprites],
                            LAYERS['walls'])
                    # import all enemies and traps
                    if (not re.search("-S", Name) and not re.search("-I", Name)):
                        self.enemy_positio[(i, j)] = {}
                        self.trap_positio[(i, j)] = {}
                        for obj in self.tmx_data.get_layer_by_name(Name+"_Enemy"):

                            # import traps
                            if obj.name == "trap":
                                self.trap_positio[(i, j)][(
                                    obj.x % WIDTH_screen+(j-1)*ROOM_WIDTH*TILE_SIZE, obj.y % HEIGHT_screen+(i-1)*ROOM_HEIGHT*TILE_SIZE)] = obj.name
                            else:
                                # import enemies
                                self.enemy_positio[(i, j)][(
                                    # j to jest nasz y, a i to jest nasz x
                                    obj.x % WIDTH_screen+(j-1)*ROOM_WIDTH*TILE_SIZE, obj.y % HEIGHT_screen+(i-1)*ROOM_HEIGHT*TILE_SIZE)] = obj.name

        self.player = Player(
            # spawn the player
                            ((spawn_j)*13*64-(64*7), (spawn_i)*9*64-(64*5)), self.allsprites, self.collision_sprites, self.create_attack, self.destroy_attack)

    # check if the player is in a new room, this is used to spawn the enemies, traps and move camera
    def check_if_in_new_room(self, player):
        new_x_y = (player.rect.centery//(9*64)+1,
                   player.rect.centerx//(13*64)+1)
        self.current_room = new_x_y

        if (16 < player.rect.centery % (9*64) < 64*6.8 and 48 < player.rect.centerx % (13*64) < 64*11):
            # print("Now in room: ", self.plain[new_x_y[0]][new_x_y[1]])
            if (([new_x_y[0], new_x_y[1], self.plain[new_x_y[0]][new_x_y[1]]]) in self.visited_rooms):
                # print("Already visited")
                pass
            else:

                self.visited_rooms.append([  # list of visited rooms for minimap
                    new_x_y[0], new_x_y[1], self.plain[new_x_y[0]][new_x_y[1]]])
                # print("Visited rooms: ", self.visited_rooms)
                if ((not re.search("-S", self.plain[new_x_y[0]][new_x_y[1]])) and (not re.search("-I", self.plain[new_x_y[0]][new_x_y[1]])) and (not re.search("-B", self.plain[new_x_y[0]][new_x_y[1]]))):
                    self.encounter = True  # this will spawn the enemies
                elif (re.search("-B", self.plain[new_x_y[0]][new_x_y[1]])):
                    self.EnterBossRoom = True  # this will spawn the boss

                self.previous = new_x_y

    def create_attack(self):  # this is the function for spawning the attack
        self.current_attack = Weapon(
            self.player, [self.allsprites, self.attack_sprites])

    def destroy_attack(self):  # this is the function for destroying the attack
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # this is the function for the player attack logic, like specyfic attack for specyfic enemy
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                colided_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if colided_sprites:
                    for sprite in colided_sprites:
                        if sprite.monster_name == 'Imp' and self.player.selected_weapon == 'axe':
                            sprite.health -= self.player.damage*100
                        if sprite.monster_name == 'Minotaur' and self.player.selected_weapon == 'sai':
                            sprite.health -= self.player.damage*10
                        else:
                            sprite.health -= self.player.damage

                        if sprite.health <= 0:
                            sprite.kill()
                            self.list_of_enemies.remove(sprite)
                            loot = random.choice(
                                # reward for killing enemy
                                list(sprite.loot_table.keys()))
                            if loot == "money":
                                self.player.money += sprite.loot_table[loot]
                            else:
                                if loot in list(INVENTORY_DATA.keys()):
                                    INVENTORY_DATA[loot]["amount"] += sprite.loot_table[loot]
                                else:
                                    INVENTORY_DATA[loot] = sprite.loot_table[loot]
                            if sprite.__class__.__name__ == "Boss":
                                self.newFloor = True  # if boss is killed, new floor is generated

    # this is function that damages player if its sprite colide with trap sprite
    def traps_logic(self):
        for sprite in self.trap_sprites:
            if self.player.hitbox.colliderect(sprite.rect):
                self.player.health -= 0.1

    # this is the function for spawning the enemies in normal rooms, and spawns traps
    def encounter_spawner(self):
        if self.encounter:
            self.encounter = False
            self.CloseDoors = True
            # monster spawn
            for position in self.enemy_positio[self.current_room]:

                monster_to_defeat = Monster(
                    self.enemy_positio[self.current_room][position],  # name
                    position,  # position
                    [self.allsprites, self.attackable_sprites],
                    self.collision_sprites,
                    self.player_damaged
                )
                self.list_of_enemies.append(monster_to_defeat)
            # trap spawn
            for position in self.trap_positio[self.current_room]:

                monster_to_defeat = Trap(
                    trap_name="spikes",
                    pos=position,
                    groups=[self.allsprites, self.trap_sprites]
                )

    def BossSpawner(self):  # this is the function for spawning the boss
        if self.EnterBossRoom:
            self.EnterBossRoom = False
            self.CloseDoors = True
            for position in self.enemy_positio[self.current_room]:

                monster_to_defeat = Boss(
                    self.enemy_positio[self.current_room][position],  # name
                    position,  # position
                    [self.allsprites, self.attackable_sprites],
                    self.collision_sprites,
                    self.player_damaged
                )
                self.list_of_enemies.append(monster_to_defeat)

    # this is the function for damaging the player
    def player_damaged(self, damage):
        self.player.health -= damage

    def DoorCloser(self):  # this is the function for closing the doors

        if self.CloseDoors:
            if (re.search("U", self.plain[self.current_room[0]][self.current_room[1]])):
                for x, y, surf in self.tmx_data.get_layer_by_name("doors").tiles():
                    Generic(
                        ((45 % ROOM_WIDTH)*TILE_SIZE+(self.player.rect.centerx//(13*64))*ROOM_WIDTH*TILE_SIZE,
                         (45 % ROOM_HEIGHT)*TILE_SIZE+(self.player.rect.centery//(9*64))*ROOM_HEIGHT*TILE_SIZE),
                        surf,
                        [self.allsprites, self.doors, self.collision_sprites],
                        LAYERS['walls'])

            if (re.search("D", self.plain[self.current_room[0]][self.current_room[1]])):
                for x, y, surf in self.tmx_data.get_layer_by_name("doors").tiles():
                    Generic(
                        ((45 % ROOM_WIDTH)*TILE_SIZE+(self.player.rect.centerx//(13*64))*ROOM_WIDTH*TILE_SIZE,
                         (53 % ROOM_HEIGHT)*TILE_SIZE+(self.player.rect.centery//(9*64))*ROOM_HEIGHT*TILE_SIZE),
                        surf,
                        [self.allsprites, self.doors, self.collision_sprites],
                        LAYERS['walls'])

            if (re.search("L", self.plain[self.current_room[0]][self.current_room[1]])):
                for x, y, surf in self.tmx_data.get_layer_by_name("doors").tiles():
                    Generic(
                        ((39 % ROOM_WIDTH)*TILE_SIZE+(self.player.rect.centerx//(13*64))*ROOM_WIDTH*TILE_SIZE,
                         (49 % ROOM_HEIGHT)*TILE_SIZE+(self.player.rect.centery//(9*64))*ROOM_HEIGHT*TILE_SIZE),
                        surf,
                        [self.allsprites, self.doors, self.collision_sprites],
                        LAYERS['walls'])

            if (re.search("R", self.plain[self.current_room[0]][self.current_room[1]])):
                for x, y, surf in self.tmx_data.get_layer_by_name("doors").tiles():
                    Generic(
                        ((51 % ROOM_WIDTH)*TILE_SIZE+(self.player.rect.centerx//(13*64))*ROOM_WIDTH*TILE_SIZE,
                         (49 % ROOM_HEIGHT)*TILE_SIZE+(self.player.rect.centery//(9*64))*ROOM_HEIGHT*TILE_SIZE),
                        surf,
                        [self.allsprites, self.doors, self.collision_sprites],
                        LAYERS['walls'])

            self.CloseDoors = False

    def DoorOpener(self):  # this is the function for opening the doors
        print(self.list_of_enemies)
        if self.list_of_enemies == [] and self.CloseDoors == False:
            for sprite in self.doors:
                sprite.kill()
            self.OpenDoors = False

    def IfPlayerDied(self):  # this is the function for checking if the player died
        if self.player.health <= 0:
            return True

    def run(self, dt):  # run the level
        self.display_surface.fill((24, 20, 37))  # fill the screen with black
        self.allsprites.custom_draw(
            self.player)  # draw the sprites
        self.check_if_in_new_room(self.player)

        self.allsprites.update(dt)  # update the sprites
        self.allsprites.enemy_updatei(self.player)  # update the enemies
        self.player_attack_logic()  # player attack logic
        self.traps_logic()  # traps logic
        self.overlay.display(self.player)  # display the overlay
        self.encounter_spawner()  # spawn the enemies
        self.BossSpawner()  # spawn the boss
        self.DoorCloser()  # close the doors
        self.DoorOpener()  # open the doors


class cameraGroup(pygame.sprite.Group):  # seting up the camera group
    def __init__(self):
        super().__init__()  # initialize the camera group
        self.display_surface = pygame.display.get_surface()  # seting up the screen
        self.offset = pygame.math.Vector2()  # seting up the offset

    def custom_draw(self, player):  # how the camera will be displayed

        self.offset.x = player.rect.centerx//(13*64) * \
            13*64 - WIDTH_screen+64*12.5

        self.offset.y = player.rect.centery//(9*64) * \
            9*64 - HEIGHT_screen+64*8.5

        for layer in LAYERS.values():
            # sort the sprites, so that the player will be in the front
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:  # if the sprite is in the layer, then display the sprite
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # if sprite == player:  # if the sprite is the player, then display the hitbox this will help in debugging
                    #     pygame.draw.rect(self.display_surface,
                    #                      'red', offset_rect, 5)
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface,
                    #                      'green', hitbox_rect, 5)
                    # if sprite.__class__.__name__ == "Monster" or sprite.__class__.__name__ == "Boss":
                    #     hitbox_rect = sprite.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface,
                    #                      'green', hitbox_rect, 5)
                    # if sprite.__class__.__name__ == "Trap":
                    #     hitbox_rect = sprite.rect.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface,
                    #                      'green', hitbox_rect, 5)

    def enemy_updatei(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()]
        for i in enemy_sprites:
            # if the sprite is a monster, then update the sprite
            if i.__class__.__name__ == "Monster":
                i.enemy_update(player)
            if i.__class__.__name__ == "Boss":
                i.enemy_update(player)
