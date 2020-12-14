
with open("input.txt", "r") as f:
    program = list(map(lambda instr: list(map(lambda p: p.strip(), instr.split(" "))), f.readlines()))


class VM(object):
    def __init__(self, prog):
       self.code = prog
       self.ip = 0
       self.acc = 0
       self.ip_history = set()

    # returns 100 on graceful exit
    # returns 99 if still running    
    def _exec_operation(self, addr):
        if (self.ip == len(self.code)):
            print("Terminating Virtual Machine Gracefully")
            return 100

        #print(f"executing {self.code[addr]}")
        self.ip_history.add(self.ip)
        delta = int(self.code[addr][1])
        if (self.code[addr][0] == 'jmp'):
            self.ip += delta
        else:
            if (self.code[addr][0] == 'acc'):
                self.acc += delta
            self.ip += 1

        return 99

    def next_instruction(self):
        self._exec_operation(self.ip)

    def check_loop(self):
        return self.ip in self.ip_history

    def program_terminates(self):
        self.reset()
        while (self._exec_operation(self.ip) == 99):
            if (self.check_loop()): return False
            if(self.ip < 0): return False
        return True


    def repair(self):
        # iteratively change instructions until our program doesn't repeat itself
        for i in range(len(self.code)):
            if (self.code[i][0] == 'nop' and int(self.code[i][1]) != 0):
                self.code[i][0] = 'jmp'
                if (self.program_terminates()):
                    break
                self.code[i][0] = 'nop'
            elif (self.code[i][0] == 'jmp'):
                self.code[i][0] = 'nop'
                if (self.program_terminates()):
                    break
                self.code[i][0] = 'jmp'
        
        return self.acc
    
    def reset(self):
        self.ip = 0
        self.acc = 0
        self.ip_history.clear()


console = VM(program)
while (console.check_loop() == False):
    console.next_instruction()
print(f"Part 1: {console.acc}")
print(f"Part 2: {console.repair()}")