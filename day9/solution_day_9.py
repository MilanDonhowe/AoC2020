

with open("input.txt", "r") as f:
    code = list(map(int, f.readlines()))

def follows_rule(sequence, index):
    last_twenty_five = sequence[index-25:index]
    for i in range(24):
        for j in range(25):
            if (last_twenty_five[i] != last_twenty_five[j]):
                if (last_twenty_five[i] + last_twenty_five[j] == sequence[index]):
                    return True
    return False

needed_number = 0

# Part 1
for index in range(25, len(code)):
    if not follows_rule(code, index):
        print(f"The answer to part 1 is {code[index]}")
        needed_number = code[index]
        break
# Part 2
# find contigous set of numbers
starting_set = (0, 1)
for index in range(2, len(code)):
    set_sum = sum([x for x in code[starting_set[0]:starting_set[1]+1]]) 
    if set_sum == needed_number:
        numeric_set = set(x for x in code[starting_set[0]:starting_set[1]+1])
        print(f"The answer to part 2 is the range of [{starting_set[0]}, {starting_set[1]}] with sum of min and max as {min(numeric_set) + max(numeric_set)}")
        break
    elif set_sum > needed_number:
        starting_set = (starting_set[0]+1, starting_set[1])
    else:
        starting_set = (starting_set[0], starting_set[1]+1)