import re
from collections import deque


def tokenize(line):
    tokens = []
    while True:
        if (num := re.match(r"\d+", line)):
            tokens.append(int(num.group()))
            line = line[num.end():]

        elif (oper := re.match(r"\+|\*", line)):
            tokens.append(oper.group())
            line = line[oper.end():]

        elif re.match(r"\(", line):
            # quick paranthetical parsing
            depth = 0
            inside_str = ""
            c = 1
            while not (depth == 0 and line[c] == ')'):
                if (line[c] == '('):
                    depth += 1
                elif (line[c] == ')'):
                    depth -= 1
                inside_str += line[c]
                c += 1
            tokens.append(tokenize(inside_str))
            line = line[len(inside_str)+2:]

        elif len(line) > 1:
            line = line[1:]

        else:
            break

    return tokens


with open("input.txt", "r") as f:
    program = [tokenize(ln) for ln in f.readlines()]

def eval_bad_math(prog):
    operands = deque() 
    operators = deque()
    for token in prog:
        if (type(token) == int):
            operands.append(token)
        elif (type(token) == str):
            operators.append(token)
        else:
            operands.append(eval_bad_math(token))
    for op in operators:
        a, b  = (operands.popleft(), operands.popleft())
        if op == '+':
            operands.appendleft(a + b)
        else:
            operands.appendleft(a * b)
    return operands[0]

# part 2:
# actually just shunting-yard algorithm
def eval_worse_math(prog):
    expr_stack = deque() 
    operators = deque()

    for token in prog:
        if (type(token) == int):
            expr_stack.append(token)
        elif (type(token) == str):
            if (token == '*'):
                if len(operators):
                    while len(operators) and (operators[len(operators)-1] == '+'):
                        expr_stack.append(operators.pop())
            operators.append(token)
        else:
            expr_stack.append(eval_worse_math(token))
    
    while len(operators):
        expr_stack.append(operators.pop())
    
    # Now we evaluate the stack
    value_stack = deque()
    for v in expr_stack:
        if type(v) == int:
            value_stack.append(v)
        else:
            a, b = (value_stack.pop(), value_stack.pop())
            if (v == '*'):
                value_stack.append(a*b)
            else:
                value_stack.append(a+b)
                
    return value_stack[0]

# part 1
print("Test Cases for Part 1:")
print("2 * 3 + (4 * 5) =", eval_bad_math(tokenize("2 * 3 + (4 * 5)")), "(should be 26)")
print("5 + (8 * 3 + 9 + 3 * 4 * 3) =", eval_bad_math(tokenize("5 + (8 * 3 + 9 + 3 * 4 * 3)")), "(should be 437)")
print("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) =", eval_bad_math(tokenize("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")), "(should be 12240)")
print("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 =", eval_bad_math(tokenize("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")), "(should be 13632)")

print("\nPart 1: ", sum([eval_bad_math(expr) for expr in program]))

# part 2
print("\nTest Cases for Part 2:")
print("1 + (2 * 3) + (4 * (5 + 6)) =", eval_worse_math(tokenize("1 + (2 * 3) + (4 * (5 + 6))")), "(should be 51)")
print("2 * 3 + (4 * 5) =", eval_worse_math(tokenize("2 * 3 + (4 * 5)")), "(should be 46)")
print("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) =", eval_worse_math(tokenize("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")),"(should be 669060)")

print("\nPart 2: ", sum([eval_worse_math(expr) for expr in program]))
