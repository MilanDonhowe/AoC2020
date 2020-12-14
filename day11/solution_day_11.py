from copy import deepcopy
from enum import Enum, auto
from pprint import pprint
# . floor
# # filled seat
# L empty seat

#    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
#    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
#    Otherwise, the seat's state does not change.

class TileType(Enum):
    EMPTY = auto()
    OCCUPIED = auto()
    FLOOR = auto()

class Tile(object):
    def __init__(self, state_char):
        if (state_char == 'L'):
            self.state = TileType.EMPTY
        elif (state_char == '#'):
            self.state = TileType.OCCUPIED
        else:
            self.state = TileType.FLOOR

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if (self.state == TileType.OCCUPIED):
            return '#'
        elif (self.state == TileType.EMPTY):
            return 'L'
        else:
            return '.'
        

def modify_p1(row, col, new_room, old_room):
    change = 0
    if (str(old_room[row][col]) == 'L'):
        if (adjacent_seats(row, col, old_room) == 0):
            change = 1
            new_room[row][col].state = TileType.OCCUPIED 
    elif (str(old_room[row][col]) == '#'):
        if (adjacent_seats(row, col, old_room) >= 4):
            change = 1
            new_room[row][col].state = TileType.EMPTY
    return change

def inbounds(x, max, min=-1):
    return x < max and x > min

def adjacent_seats(row, col, room):
    total = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 or y != 0):
                if (inbounds(col+x, len(room)) and inbounds(row+y, len(room))):
                    if str(room[row+y][col+x]) == '#':
                        total += 1
    return total

with open("input.txt", "r") as f:
    room_txt = list(map(lambda s: s.strip(), f.readlines()))


def build_tile_map(txt):
    map = list()
    for index, line in enumerate(txt):
        map.append(list())
        for char in line:
            map[index].append(Tile(char))
    return map

#room_txt = ["#.##.##.##",
#"#######.##",
#"#.#.#..#..",
#"####.##.##",
#"#.##.##.##",
#"#.#####.##",
#"..#.#.....",
#"##########",
#"#.######.#",
#"#.#####.##"]

#TileMap = build_tile_map(room_txt)

#for ln in TileMap:
#    print("".join(list(map(str, ln))))



def run_simulation(room, modifier_fn):
    changes = 1
    new_room = room
    while (changes != 0):
        changes = 0
        old_room = new_room
        new_room = deepcopy(old_room)
        for y in range(len(room)):
            for x in range(len(room[y])):
                changes += modifier_fn(y,x,new_room,old_room)
        print(f" {changes} seats changed", end='\r')
    return new_room

def COUNT_OCCUPIED_SEATS(TILE_MAP):
    seats = 0
    for tile_ls in TILE_MAP:
        for tile in tile_ls:
            if (str(tile) == '#'):
                seats += 1
    return seats

#final_map = run_simulation(TileMap)
#for ln in final_map:
#    print("".join(list(map(str, ln))))

#part 1
complete_map = run_simulation(build_tile_map(room_txt), modify_p1)
print(f"The total number of seats for part 1 is : {COUNT_OCCUPIED_SEATS(complete_map)}")

def modify_p2(row, col, new_room, old_room):
    change = 0
    if (str(old_room[row][col]) == '#'):
        if (sees_adjacent_seats(row, col, old_room) >= 5):
            change = 1
            new_room[row][col].state = TileType.EMPTY
    elif (str(old_room[row][col]) == 'L'):
        if (sees_adjacent_seats(row, col, old_room) == 0):
            change = 1
            new_room[row][col].state = TileType.OCCUPIED
            
    return change

def sees_adjacent_seats(row, col, room):
    total = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x != 0 or y != 0):
                if (sees_occupied_seat(row, col, (y, x), room)):
                    total += 1
    return total


# vector is dy, dx
def sees_occupied_seat(row, col, vector, room):
    y = row
    x = col
    while (inbounds(x+vector[1], len(room[0])) and inbounds(y+vector[0], len(room))):
        x += vector[1]
        y += vector[0]
        if (room[y][x].state == TileType.EMPTY): return False
        elif (room[y][x].state == TileType.OCCUPIED): return True
    return False 
#part 2
complete_map = run_simulation(build_tile_map(room_txt), modify_p2)
print(f"The total number of seats for part 2 is : {COUNT_OCCUPIED_SEATS(complete_map)}")
