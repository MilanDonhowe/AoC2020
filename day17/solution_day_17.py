# huh, looks like a 3D conway's game of life.

# let's represent the grid as a 2D array of strings (3D array of characters)
with open("input.txt", "r") as initial_grid:
    universe = [[x.strip() for x in initial_grid.readlines()]]

# for part 2 
universe_part2 = [universe]

is_active = lambda c: c == '#'
inbounds = lambda num, len: len > num > -1

def check_neighbors(gx, gy, gz, grid):
    height = len(grid)
    width = len(grid[0])

    neighbors = set([(a, b, c) for a in range(gx-1, gx+2) for b in range(gy-1, gy+2) for c in range(gz-1, gz+2)])
    neighbors.remove((gx, gy, gz))
    active_neighbors = 0
    for x, y, z in neighbors:
        if (inbounds(z, height) and inbounds(x, width) and inbounds(y, width)):
            if (is_active(grid[z][y][x])):
                active_neighbors += 1
    return active_neighbors

def next_cycle_3D(previous_state):
    next_state = list()
    height = len(previous_state)
    width = len(previous_state[0])
    for z in range(-1, len(previous_state)+1):
        next_state.append(list())
        for y in range(-1, width+1):
            line = [] 
            for x in range(-1, width+1):
                # if in bounds
                if (inbounds(z, height) and inbounds(x, width) and inbounds(y, width)):
                    state = previous_state[z][y][x]
                # otherwise assumed inactive
                else:
                    state = '.'
                
                neighbors = check_neighbors(x, y, z, previous_state)
                if (is_active(state) and neighbors != 2 and neighbors != 3):
                    state = '.'
                elif ((not is_active(state)) and neighbors == 3):
                    state = '#'
                
                
                line.append(state)
            
            next_state[z+1].append("".join(line))
    return next_state


def count_active(grid):
    total = 0
    for plane in grid:
        for ln in plane:
            for char in ln:
                if is_active(char):
                    total += 1
    return total

test_input = [[".#.", "..#", "###"]]
print("Test Case:")
for _ in range(6):
    test_input = next_cycle_3D(test_input)
print(f"Test result: {count_active(test_input)} (should be 112)")


# Part 1:
for cycle in range(6):
    universe = next_cycle_3D(universe)
print("Part 1:", count_active(universe))

# Part II: Another Dimension Electric Boo-Ga-Loo

def check_neighbors_4D(gx, gy, gz, gw, grid):
    w_max = len(grid)
    z_max = len(grid[0])
    xy_max = len(grid[0][0])

    neighbors = set([(a, b, c, d) for a in range(gx-1, gx+2) for b in range(gy-1, gy+2) for c in range(gz-1, gz+2) for d in range(gw-1, gw+2)])
    neighbors.remove((gx, gy, gz, gw))
    active_neighbors = 0
    for x, y, z, w in neighbors:
        if (inbounds(z, z_max) and inbounds(x, xy_max) and inbounds(y, xy_max) and inbounds(w, w_max)):
            if (is_active(grid[w][z][y][x])):
                active_neighbors += 1
    return active_neighbors

def next_cycle_4D(previous_state):
    next_state = list()
    w_max = len(previous_state)
    z_max = len(previous_state[0])
    xy_max = len(previous_state[0][0])
    for w in range(-1, w_max+1):
        next_z = []
        for z in range(-1,z_max+1):
            next_xy = []
            for y in range(-1, xy_max+1):
                line = []
                for x in range(-1, xy_max+1):
                    # if in bounds
                    if (inbounds(z, z_max) and inbounds(x, xy_max) and inbounds(y, xy_max) and inbounds(w, w_max)):
                        state = previous_state[w][z][y][x]
                    # otherwise assumed inactive
                    else:
                        state = '.'

                    neighbors = check_neighbors_4D(x, y, z, w, previous_state)
                    if (is_active(state) and neighbors != 2 and neighbors != 3):
                        state = '.'
                    elif ((not is_active(state)) and neighbors == 3):
                        state = '#'
                    
                    line.append(state)
                next_xy.append("".join(line))
            next_z.append(next_xy)
        next_state.append(next_z)
    return next_state

# part 2 solution

test_input = [[[".#.", "..#", "###"]]]
print("Test Case:")
for _ in range(6):
    test_input = next_cycle_4D(test_input)

test_total = 0
for grid in test_input:
    test_total += count_active(grid)

print(f"Test result: {test_total} (should be 848)")

for _ in range(6):
    universe_part2 = next_cycle_4D(universe_part2)

part2_total = 0
for grid in universe_part2:
    part2_total += count_active(grid)

print("Part 2:", part2_total)