# LET'S ABUSE MY CPU WOOHOO
from multiprocessing import Pool, cpu_count

with open("input.txt", "r") as f:
    passes = f.readlines()
    arrival_time = int(passes[0])
    IDs_p2 = list(map(lambda s: s.strip(), passes[1].split(',')))
    IDs = list(map(int, filter(lambda s: s.isnumeric(), map(lambda s: s.strip(), passes[1].split(',')))))

#arrival_time = 939
#IDs = [7, 13, 59, 31, 19]

def find_nearest_bus(time, IDs):
    # id, wait_time
    best_bus = (0, 9999999999999999999999)
    for id in IDs:
        # when does the bus arrive before we get there?
        next_arrival = time - (time % id)
        while (next_arrival < time):
            next_arrival += id
        # calc wait time
        wait_time = next_arrival - time
        if (wait_time < best_bus[1]):
            best_bus = (id, wait_time)
    return best_bus

best_pair = find_nearest_bus(arrival_time, IDs)
print(f"The answer to part 1 is {best_pair[0]*best_pair[1]}")

pair_ls = list()
for index, value in enumerate(IDs_p2):
    if (value != 'x'):
        pair_ls.append((int(value), index))


def validate_t(t, pair_reqs):
    for ID, t_offset in pair_reqs:
        if ((t+t_offset) % ID != 0):
            return False
    return True


def generate_t_candidate(biggest_id, t_offset, start, step):
    multiple = start
    while True:
        multiple += step
        yield (biggest_id*multiple)-t_offset

def find_t(pair_reqs, start, delta):
    sorted_pairs = sorted(pair_reqs, key=lambda pair: pair[0], reverse=True)
    t_gen = generate_t_candidate(sorted_pairs[0][0], sorted_pairs[0][1], start, delta)
    t = next(t_gen)
    while not validate_t(t, pair_reqs):
        #print(f"\ttesting {t}", end='\r')
        t = next(t_gen)
    return t

test_ls = [(67, 0), (7, 1), (59, 3), (61, 4)]

# how could I leverage parallelization to solve this problem?
# Well, I'm looking for some multiple of the biggest item within the range of
# [1 trillion, infinity)
# counting each multiple linearly with a step of 1 sucks

# bad serial process approach
#print(f"Answer occurs @ {find_t(pair_ls)}")

# number is higher than 100000000000000....
# 100000000000000

#def report_t(result):
#    print(f"one possible answer is {result}")
#    exit(0)

#pool = Pool(cpu_count())
# parallelize calls
#for delta in [2, 3, 5, 7, 11, 13]:
#    pool.apply_async(find_t, args=(pair_ls, 0, delta), callback=report_t)

#pool.close()