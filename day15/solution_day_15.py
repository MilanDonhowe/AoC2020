#  Day 15: huh brute force worked this time 

from collections import deque 


# Tried implementing a circular buffer to decrease run time 
# but doesn't seem to yield a significantly faster result
class CircularBuffer(object):
    def __init__(self, size):
        self.size = size
        self.elems = [-1 for _ in range(size)]
        self.next_index = 0 

    def append(self, item):
        self.elems[self.next_index] = item
        self.next_index = (self.next_index + 1) % self.size

    def get(self, index):
        return self.elems[index%self.size]

    def __getitem__(self, key):
        return self.get(key)

    def get_last_item(self):
        return self.elems[self.next_index-1%2]


def get_turn(turn_limit, initial_sequence):
    # sequence of numbers we speak
    sequence = CircularBuffer(2)
    meta_history = dict()
    # meta will store {number, list of appearances}

    for turn in range(1, turn_limit+1):
        if (turn-1 < len(initial_sequence)):
            sequence.append(initial_sequence[turn-1])

            meta_history[initial_sequence[turn-1]] = deque([turn])
        else:
            #last_num_spoken = sequence[len(sequence)-1]
            last_num_spoken = sequence.get_last_item()

            if (len(meta_history[last_num_spoken]) > 1):
                
                age_ls = meta_history[last_num_spoken]
                age = age_ls[0] - age_ls[1]

                sequence.append(age)
                
                if age not in meta_history.keys():
                    meta_history[age] = deque([turn])
                else:
                    meta_history[age].appendleft(turn)
            else:
                sequence.append(0)
                
                if 0 not in meta_history.keys():
                    meta_history[0] = deque([turn])
                else:
                    meta_history[0].appendleft(turn)

    return sequence.get_last_item()
    #return sequence[len(sequence)-1]


# test cases
print(get_turn(2020, [0, 3, 6]), " should be 436")
print(get_turn(2020, [1, 3, 2]), " should be 1")

# applying solution to my input
starting_sequence = [0,14,6,20,1,4]
print("Part 1: ", get_turn(2020, starting_sequence))
print("Next part will take a few minutes but should ultimately work")
print("Part 2: ", get_turn(30000000, starting_sequence))
