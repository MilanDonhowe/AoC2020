import re
from copy import deepcopy

with open("input", "r") as f:
    text_blocks = f.read().split('\n\n')


def parse_ranges(range_txt):
    valid_numbers = set()
    for ln in range_txt.split('\n'):
        numbers = re.findall(r"\d+", ln)
        for index in range(1, len(numbers), 2):
            high = numbers[index]
            low = numbers[index-1]
            for num in range(int(low), int(high)+1):
                valid_numbers.add(num)
    return valid_numbers


valid_ranges = parse_ranges(text_blocks[0])
my_ticket = [int(x) for x in text_blocks[1].split('\n')[1].split(',')]
nearby_tickets = [[int(x) for x in line.split(',')] for line in text_blocks[2].split('\n')[1:][:-1]] 

# part 1 : eliminating bad tickets
def ticket_error_rate(valid_set, tickets):
    error_rate = 0
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for num in ticket:
            if num not in valid_set:
                error_rate += num
                valid = False
        if valid:
            valid_tickets.append(ticket)

    return error_rate, valid_tickets

error_rate, valid_tickets = ticket_error_rate(valid_ranges, nearby_tickets)
print(f"The error rate for part 1 is {error_rate}")

valid_tickets.append(my_ticket)


# part 2 : determining the fields

# have a hash table with a set of valid numbers for each field
def generate_field_table(spec_txt):
    field_table = dict()
    for ln in spec_txt.split('\n'):
        components = ln.split(':')
        field_name = components[0]
        field_set = set()
        numbers = [int(num) for num in re.findall(r"\d+", components[1])]
        for index in range(1, len(numbers), 2):
            for valid_num in range(numbers[index-1], numbers[index]+1):
                field_set.add(valid_num)
        field_table[field_name] = field_set 
    return field_table

# Recursively determine the ordering by process of elimination :)
def determine_field_ordering(field_tbl, ticket_ls, cached_dict=None, cached_set=None):
    if (cached_dict != None):
        ordering_table = cached_dict
    else:
        ordering_table = dict(zip(field_tbl.keys(), [-1 for _ in range(999999)]))

    if (cached_set != None):
        possible_fields = cached_set
    else:
        possible_fields = set(field_tbl.keys())

    for order in range(0, len(ticket_ls[0])):
        if order in ordering_table.values():
            continue
        field_candidates = deepcopy(possible_fields)
        for ticket in ticket_ls:
            if (len(field_candidates) == 1):
                break
            for candidate in deepcopy(field_candidates):
                if ticket[order] not in field_tbl[candidate]:
                    field_candidates.remove(candidate)
        if (len(field_candidates) == 1):
            for c in field_candidates:
                possible_fields.remove(c)
                ordering_table[c] = order
    
    if -1 in ordering_table.values():
        return determine_field_ordering(field_tbl, ticket_ls, ordering_table, possible_fields)
    else:
        return ordering_table

tbl = generate_field_table(text_blocks[0])
tbl_order = determine_field_ordering(tbl, valid_tickets)

part_two_answer = 1
for key in tbl_order.keys():
    if "departure" in key:
        part_two_answer *= my_ticket[tbl_order[key]]

print("The product for part 2 is", part_two_answer)