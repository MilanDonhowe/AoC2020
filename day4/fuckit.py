# after failing hard with trying to use regex in c
# i fell back to python

import re


def valid(passport):
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for f in fields:
        if (f not in passport): 
            return False
    return True

with open("input.txt", "r") as f:
    passports = f.read().split("\n\n")

# part 1
passports = list(filter(valid, passports))
print(len(passports))
# part 2
# I have severe brain damage after doing this much regex
def validate_fields(passport):
    try:
        birth_year = int(re.search(r"byr:\d+", passport).group().split(':')[1])
        if (birth_year not in range(1920, 2003)): 
            return False
        issue_year = int(re.search(r"iyr:\d+", passport).group().split(':')[1])
        if (issue_year not in range(2010, 2021)): 
            return False
        expire_year = int(re.search(r"eyr:\d+", passport).group().split(":")[1])
        if (expire_year not in range(2020, 2031)):
            return False
        # height test
        height = re.search(r"hgt:\d+(in|cm)", passport).group().split(":")
        height_int = int(height[1][:-2])
        if (height[1].endswith("in")):
            if height_int not in range(59, 77):
                return False
        else:
            if height_int not in range(150, 194):
                return False

        if not re.search(r"hcl:#[0-9a-f]{6}", passport):
            return False
        
        if not re.search(r"ecl:(amb|blu|brn|gry|grn|hzl|oth)", passport):
            return False

        # had to use negative lookahead as it would accept PIDs with 10 digits :C
        if not re.search(r"pid:\d{9}(?!\d)", passport):
            return False

        return True
    except:
        return False

passports = list(filter(validate_fields, passports))
print(len(passports))