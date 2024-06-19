

TILE_SIZE = 64
ROOM_WIDTH = 13
ROOM_HEIGHT = 9
WIDTH_screen = TILE_SIZE*ROOM_WIDTH
HEIGHT_screen = TILE_SIZE*ROOM_HEIGHT

LAYERS = {
    "background": 0,
    "walls": 1,
    "player": 2,
    "weapon": 3
}

WEAPON_DATA = {
    "sword": {'cooldown': 50, 'damage': 0.4},
    "axe": {'cooldown': 50, 'damage': 0.4},
    "lance": {'cooldown': 50, 'damage': 0.4},
    "rapier": {'cooldown': 50, 'damage': 0.4},
    "sai": {'cooldown': 50, 'damage': 0.4}
}

MONSTER_DATA = {
    "Imp": {'health': 100, 'gold': 10, 'speed': 100, 'damage': 10, 'attack_radius': 30, 'notice_radius': 300, 'loot_table': {'damage_potion': 1, 'speed_potion': 1, 'health_potion': 1, 'money': 10}
            },
    "Minotaur": {'health': 500, 'gold': 20, 'speed': 160, 'damage': 0.2, 'attack_radius': 40, 'notice_radius': 400, 'loot_table': {'damage_potion': 2, 'health_potion': 2, 'money': 20}}
}


INVENTORY_DATA = {
    'damage_potion': {'type': 'potion', 'value': 2, "amount": 0, "effect": "damage_up"},
    'health_potion': {'type': 'potion', 'value': 50, "amount": 0},
    'speed_potion': {'type': 'potion', 'value': 100, "amount": 0, "effect": "speed_up"},
    'dragons_blood': {'type': 'potion', 'value': 100, "amount": 1, "effect": "area_dmg"}
}
