from networkx import DiGraph
import re

with open("input.txt", "r") as f:
    rules =["shiny gold bags contain 2 dark red bags.",
            "dark red bags contain 2 dark orange bags.",
            "dark orange bags contain 2 dark yellow bags.",
            "dark yellow bags contain 2 dark green bags.",
            "dark green bags contain 2 dark blue bags.",
            "dark blue bags contain 2 dark violet bags.",
            "dark violet bags contain no other bags."]
    #rules = map(lambda s: s.strip(), f.readlines())

# first I parse each rule into a dictionary 
def parse_rule(rule_str):
    containee_dict = dict()
    rules = re.findall(r"\d+ [A-Za-z ]+ bag", rule_str)
    for r in rules:
        number = int(re.search(r"\d+", r).group())
        bag_name = re.search(r"[A-Za-z ]+ (?=bag)", r).group().strip()
        containee_dict[bag_name] = number
    return containee_dict

table = dict()
for r in rules:
    container, containee = r.split(" contain ")
    table[re.search(r"[A-Za-z ]+ (?=bag)", container).group().strip()] = parse_rule(containee)


def build_weight_graph(tbl):
    gmatrix = DiGraph()
    for container, containee in tbl.items():
        for containee_name, containee_quantity in containee.items():
            gmatrix.add_edge(container, containee_name, weight=containee_quantity)
    return gmatrix

def graphx_part1(graph, name):
    unique_predecessors = set()
    for p in graph.predecessors(name):
        unique_predecessors.add(p)
        unique_predecessors = unique_predecessors.union(graphx_part1(graph, p))
    return unique_predecessors

def graphx_part2(graph, name):
    total = 0
    for p in graph.successors(name):
        total += (graph.get_edge_data(name, p)["weight"] * graphx_part2(graph, p))
    if total == 0:
        return 1
    return total

print("Part 1: ", len(graphx_part1(build_weight_graph(table), "shiny gold")))
print("Part 2: ", graphx_part2(build_weight_graph(table), "shiny gold"))