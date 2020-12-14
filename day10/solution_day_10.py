# sorting fun
from networkx import Graph, all_simple_paths

with open("input.txt", "r") as f:
    adapters = sorted(map(int, f.readlines()))
    adapters = [0] + adapters + [adapters[len(adapters)-1]+3]

def count_differences(sequence: list, diff: int):
    occurences = 0
    for x in range(len(sequence)-1):
        if (sequence[x+1]-sequence[x] == diff):
            occurences += 1
    return occurences
print(len(adapters)/4)
print(f"The answer to part 1 is {count_differences(adapters, 1) * count_differences(adapters, 3)}")


# part 2
# well brute force doesn't work so time to try and recall discrete mathematics
#
def build_graph(sequence):
    graph = Graph()
    for x in sequence:
        graph.add_node(x)
    for x in range(0, len(sequence)-1):
        for y in range(x, len(sequence)):
            if (abs(sequence[y] - sequence[x]) < 4):
                graph.add_edge(sequence[x], sequence[y])
    return graph

def get_pathways(a, g):
    total = 1
    for i in range(1,4):
        if (g.has_edge(a, a+i)):
            total += 1
    return total

#def remove_redundant_pathways(a, g):
#    if ()

def count_paths(adapters, graph):
    total = 1
    for a in adapters:
        # multiply total by possible edges to traverse
        # remove redundant edges from graph
        total *= get_pathways(a, graph)
    return total

print(f"total pathways is {count_paths(adapters, build_graph(adapters))}")


#print("this will take about an hour, get a cup of coffee or tea and let the CPU crunch some numbers")
#g = build_graph(adapters)
#num_paths = 0
#for path in all_simple_paths(g, 0, adapters[len(adapters)-1]):
#    num_paths += 1
#    print(num_paths, end="\r")
#print(f"The answer to part 2 is {num_paths}")

#def possible_sequels(adapter, adapter_set):
#    # test first case
#    sequels = 1
#   for i in range(1, 4):
#        if (adapter+i in adapter_set):
#            sequels += 1
#    if (sequels == 2):
#        return 4
#    elif (sequels == 3):
#        return 15
#    return 1

#def count_total_combinations(adapters):
#    total = 1
#    adapter_set = set(adapters)
#    for adapter in adapters[1:-1]:
#        total *= possible_sequels(adapter, adapter_set)
#    return total

#print(f"Solution to part 2 {count_total_combinations(adapters)}")