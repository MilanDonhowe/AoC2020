from collections import Counter

with open("input.txt", "r") as f:
    program = list(map(lambda s: s.strip().split(" = "), f.readlines()))

    # test cases:
    #     
    #program = [
    #    ["mask", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"],
    #    ["mem[8]", "11"],
    #    ["mem[7]", "101"],
    #    ["mem[8]", "0"]
    #]

    #program = [
    #    ["mask", "000000000000000000000000000000X1001X"],
    #    ["mem[42]", "100"],
    #    ["mask", "00000000000000000000000000000000X0XX"],
    #    ["mem[26]", "1"]
    #]


class FerryByte(object):
    def __init__(self, bit_str=None):
        self.byte = [False for _ in range(36)]
        if (bit_str != None):
            self.write(bit_str)

    def write(self, bit_str):
        for index, bit in enumerate(bit_str):
            if bit == '1':
                self.byte[index] = True
            else:
                self.byte[index] = False
    
    def apply_mask(self, MASK_STR):
        #print("pre mask: ", self.__str__())
        for index, bit in enumerate(MASK_STR):
            if bit == '1':
                self.byte[index] = True
            elif bit == '0':
                self.byte[index] = False
        #print("post mask: ", self.__str__())


    def __str__(self):
        return "".join(map(str, self.__repr__()))

    def __repr__(self):
        return list(map(int, self.byte))

class FerryMachine(object):
    def __init__(self, code):
        # using a dictionary because I don't want to actually
        # use 10000000000000000000000 bytes
        self.Memory = dict()
        self.code = code
        self.ip = 0
        self.bitmask = None

    def _execute_next_instruction(self):
        instr = self.code[self.ip]
        if (instr[0].startswith('mem')):
            address = int(instr[0][4:-1])
            bit_string = bin(int(instr[1]))[2:]
            # Add left-padding
            bit_string = "0"*(36-len(bit_string)) + bit_string
            self.Memory[address] = FerryByte(bit_string)
            #print(f"Writing {bit_string} of length {len(bit_string)} to {address}")
            if (self.bitmask != None):
                self.Memory[address].apply_mask(self.bitmask)
            #print(f"After bitmask application... we get {self.Memory[address]}")
        elif (instr[0] == 'mask'):
            self.bitmask = instr[1]

    def run(self):
        while (self.ip < len(self.code)):
            self._execute_next_instruction()
            self.ip += 1

    def sum_memory(self):
        sum = 0
        for byte in self.Memory.values():
            sum += int(byte.__str__(), 2)
        return sum

class FerryMachineVersionTwo(FerryMachine):

    def _execute_next_instruction(self):
        instr = self.code[self.ip]

        if (instr[0].startswith('mem')):
            address = int(instr[0][4:-1])

            address_bitstring = bin(address)[2:]
            address_bitstring = '0'*(36-len(address_bitstring)) + address_bitstring
            address_bitstring = FerryByte(address_bitstring)

            masks = self.generate_masks()
            
            # setup our operand
            bit_string = bin(int(instr[1]))[2:]
            bit_string = "0"*(36-len(bit_string)) + bit_string

            # alright now let's write to each possible address
            for m in masks:
                new_addr = address_bitstring
                #print(f"------\n")
                #print (f"starting {new_addr}")
                #print (f"applying {m}")
                new_addr.apply_mask(m)
                #print (f"getting  {new_addr.__str__()}")
                #print(f"Writing {int(bit_string.__str__(), 2)} to address {int(new_addr.__str__(), 2)}")
                self.Memory[int(new_addr.__str__(), 2)] = bit_string

        elif (instr[0] == 'mask'):
            self.bitmask = instr[1].replace('0', 'A')


        # for a mask, generate each possible mask
        # then apply each mask
    def generate_masks(self):
        masks = list()
        # we have n wild cards

        slots = Counter(self.bitmask)
        n = slots['X']

        for combo_num in range(2**n):
            combo = bin(combo_num)[2:]
            combo = ('0'*(n-len(combo))) + combo
            combo_index = 0
            tmp_msk = list(self.bitmask)
            for i, c in enumerate(self.bitmask):
                if c == 'X':
                    tmp_msk[i] = combo[combo_index]
                    combo_index += 1
            masks.append("".join(tmp_msk))
        return masks

    def run(self):
        while (self.ip < len(self.code)):
            self._execute_next_instruction()
            self.ip += 1

# Part 1
ferry_computer = FerryMachine(program)
ferry_computer.run()
print(f"Part 1 results in {ferry_computer.sum_memory()}")

# part 2
ferry_computer_two = FerryMachineVersionTwo(program)
ferry_computer_two.run()
print(f"Part 2 results in {ferry_computer_two.sum_memory()}")