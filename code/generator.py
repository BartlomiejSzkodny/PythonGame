import random
import re


def rekurencja(i, j, plane, reduced, pool, k):
    if plane[i][j] != 0:  # if the room is already filled, return
        return

    if k < 0:
        return
    k -= 1

    # seting up lists, that will determine what rooms can be placed in the current place
    reduced = []
    mussnt = []
    muss = []
    can = []
    if ((i-1 < 0) or (plane[i-1][j] != 0 and ('D' not in plane[i-1][j]))):
        mussnt.append('U')
    elif ((plane[i-1][j] != 0) and ('D' in plane[i-1][j])):
        muss.append('U')
    elif (plane[i-1][j] == 0):
        can.append('U')
    if ((j-1 < 0) or (plane[i][j-1] != 0 and ('R' not in plane[i][j-1]))):
        mussnt.append('L')
    elif ((plane[i][j-1] != 0) and ('R' in plane[i][j-1])):
        muss.append('L')
    elif (plane[i][j-1] == 0):
        can.append('L')
    if ((j+1 == 5) or (plane[i][j+1] != 0 and ('L' not in plane[i][j+1]))):
        mussnt.append('R')
    elif ((plane[i][j+1] != 0) and ('L' in plane[i][j+1])):
        muss.append('R')
    elif (plane[i][j+1] == 0):
        can.append('R')
    if ((i+1 == 5) or (plane[i+1][j] != 0 and ('U' not in plane[i+1][j]))):
        mussnt.append('D')
    elif ((plane[i+1][j] != 0) and ('U' in plane[i+1][j])):
        muss.append('D')
    elif (plane[i+1][j] == 0):
        can.append('D')

    # reducing the list of rooms that can be placed in the current place
    reduced = [s for s in pool if not any(m in s for m in mussnt)]
    reduced = [s for s in reduced if all(m in s for m in muss)]

    if len(reduced) == 0:
        reduced = can

    # placing the room in the current place
    plane[i][j] = random.choice(reduced)
    for c2 in plane[i][j]:
        if c2 == 'U':
            rekurencja(i-1, j, plane, reduced, pool, k)
        if c2 == 'L':
            rekurencja(i, j-1, plane, reduced, pool, k)
        if c2 == 'R':
            rekurencja(i, j+1, plane, reduced, pool, k)
        if c2 == 'D':
            rekurencja(i+1, j, plane, reduced, pool, k)

# function that generates the level


def LevelGenerationComplete():
    numberOfRooms = 0
    SpawnRommFind = False
    BossRoomFind = False
    ShopRoomFind = False
    # generating the level until all the conditions are met
    while ((ShopRoomFind == False) or (BossRoomFind == False) or (SpawnRommFind == False) or (10 < numberOfRooms > 15)):
        plane = [[0 for i in range(5)] for j in range(5)]
        levelGenerator(plane)
        numberOfRooms = cleaner(plane)
        SpawnRommFind, BossRoomFind, ShopRoomFind, spawn_i, spawn_j = FlagRooms(
            plane)

    return plane, spawn_i, spawn_j

# function that generates the level recursively


def levelGenerator(plane):
    rekurencja(2, 2, plane, [], ["U", "UL", "UR", "UD", "ULR", "ULD", "URD", "ULRD",
                                 "L", "LR", "LD", "LRD",
                                 "R", "RD",
                                 "D",
                                 "UL", "UR", "UD", "LR", "LD", "RD"], 5)

    return plane


# function that cleans the level from the romms that lead to nowhere
def cleaner(plane):
    numberOfRooms = 0
    for i in range(5):
        for j in range(5):
            if plane[i][j] != 0:
                numberOfRooms += 1
                if ("U" in plane[i][j]) and (plane[i-1][j] == 0):
                    plane[i][j] = re.sub("U", "", plane[i][j])
                if ("L" in plane[i][j]) and (plane[i][j-1] == 0):
                    plane[i][j] = re.sub("L", "", plane[i][j])
                if ("R" in plane[i][j]) and (plane[i][j+1] == 0):
                    plane[i][j] = re.sub("R", "", plane[i][j])
                if ("D" in plane[i][j]) and (plane[i+1][j] == 0):
                    plane[i][j] = re.sub("D", "", plane[i][j])
    return numberOfRooms


# function that flags the rooms(adds shop, spawn and boss rooms)
def FlagRooms(plane):
    SpawnRommFind = False
    BossRoomFind = False
    ShopRoomFind = False
    spawn_i = 0
    spawn_j = 0
    for i in range(5):
        for j in range(5):
            if plane[i][j] != 0:
                plane[i][j] += "-S"
                SpawnRommFind = True
                spawn_i = i
                spawn_j = j
                break
        if (SpawnRommFind == 1):
            break
    for i in range(4, -1, -1):
        for j in range(4, -1, -1):
            if plane[i][j] != 0:
                if (plane[i][j] == 'U') or (plane[i][j] == 'L') or (plane[i][j] == 'R') or (plane[i][j] == 'D'):
                    plane[i][j] += "-B"
                    BossRoomFind = True
                    break
        if (BossRoomFind == 1):
            break
    for i in range(5):
        for j in range(5):
            if (plane[i][j] == 'U') or (plane[i][j] == 'L') or (plane[i][j] == 'R') or (plane[i][j] == 'D'):
                plane[i][j] += "-I"
                ShopRoomFind = True
                break
        if (ShopRoomFind == 1):
            break

    return SpawnRommFind, BossRoomFind, ShopRoomFind, spawn_i, spawn_j
