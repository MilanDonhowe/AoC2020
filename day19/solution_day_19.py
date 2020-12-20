import re
import subprocess

with open("input", "r") as f:
    text_blocks = f.read().split('\n\n')

# basically I want to build a regular expression from a self-referencing table

def build_table(textblock):
    table = dict()
    for ln in textblock:
        key, value = ln.split(':')
        table[key] = value
    return table

reference_table = build_table(text_blocks[0].strip().split('\n'))

def gen_regex(tbl, start_key):
    regex = ""
    line = tbl[start_key]
    while True:
        if (key := re.match(r"\d+", line)):
            line = line[key.end():]
            if ('|' in tbl[key.group()]):
                regex = regex + '(' + gen_regex(tbl, key.group()) + ')'
            else:
                regex += gen_regex(tbl, key.group())
        elif (len(line) > 0):
            # individual character check
            # for some reason it was adding double quotes
            # to the pattern so I check for that too
            if (not line[0].isspace()) and line[0] != '"':
                regex += line[0]
            line = line[1:]
        else:
            break
    return regex


def find_matches(pattern, candidates):
    pattern = pattern + "$"
    total_matches = 0
    for c in candidates:
        if (re.match(pattern, c)):
            total_matches += 1
    return total_matches


def test_expr(regex, text):
    result = re.match(regex, text)
    if result == None:
        result = "no match"
    print(f"the regular expression {regex} against {text} results in", result)


# Test Case

Test_input = ["0: 4 1 5", "1: 2 3 | 3 2", "2: 4 4 | 5 5", "3: 4 5 | 5 4", '4: "a"', '5: "b"']
Test_text = ["ababbb", "bababa", "abbbab", "aaabbb", 'aaabbb']
Test_tbl = build_table(Test_input)
Test_pattern = gen_regex(Test_tbl, "0")
print("Test case for part 1: ", find_matches(Test_pattern, Test_text), "(should be 2)")

# Part 1 Calculation

print("Part 1:", find_matches(gen_regex(reference_table, '0'), text_blocks[1].strip().split('\n')))


# I have a .NET C# script
def test_expr_dotnet(pattern, text):
    proc = subprocess.Popen(["./RegexMatcher/bin/Debug/net5.0/RegexMatcher", pattern, text], stdout=subprocess.PIPE)
    proc.wait()
    response = proc.poll()
    return int(response)


def find_matches_dotnet(pattern, tests):
    pattern = "^" + pattern + "$"
    total = 0
    for test in tests:
        total += test_expr_dotnet(pattern, test)
    return total
    
print("Test cases (using dotnet):", find_matches_dotnet(Test_pattern, Test_text), "(should be 2)")

# Part 2 Calculation
# seems this is intended to throw off regex approaches given its recursive nature
# which is incredibly unforunate, luckily .NET has a handy feature in its built-in regex engine
# so I'll just write up a quick C# script and use it as a seperate binary.

reference_table['8'] =  '(42)+'

# I have to use balancing groups for this part
# www.rexegg.com/regex-quantifier-capture.html
reference_table['11'] = '(?:(42)(?<M>))+(?<-M>(31))+(?(M)(?!))' 


print("Part 2 (using dotnet):", find_matches_dotnet(gen_regex(reference_table, '0'), text_blocks[1].strip().split('\n')))
