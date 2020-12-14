from math import cos, sin, radians, sqrt, atan2


class Ferry(object):
    def __init__(self):
        # x, y
        self.pos = [0, 0]
        self.direction = 0

    def move(self, instruction):
        delta = int(instruction[1:])
        #pos_before = f"({self.pos[0]}, {self.pos[1]})"
        if (instruction[0] == 'N'):
            self.pos[1] += delta
        elif (instruction[0] == 'S'):
            self.pos[1] -= delta
        elif (instruction[0] == 'W'):
            self.pos[0] -= delta
        elif (instruction[0] == 'E'):
            self.pos[0] += delta
        elif (instruction[0] == 'F'):
            self.pos[0] = self.pos[0] + (delta * round(cos(radians(self.direction))))
            self.pos[1] = self.pos[1] + (delta * round(sin(radians(self.direction))))
        elif (instruction[0] == 'L'):
            self.direction += delta
        elif (instruction[0] == 'R'):
            self.direction -= delta

        #print(pos_before, f" -> ({self.pos[0]},{self.pos[1]})")


    def manhattan_distance(self):
        return abs(self.pos[0]) + abs(self.pos[1])

#
#nav = ["F10","N3","F7","R90","F11"]
#test_ferry = Ferry()
#for instr in test_input:
#    test_ferry.move(instr)
#print(test_ferry.manhattan_distance())

# Part 1
with open("input.txt", "r") as f:
    nav = f.readlines()

myFerry = Ferry()
for instr in nav:
    myFerry.move(instr)
print(myFerry.manhattan_distance())

# Part 2

class WayPoint(Ferry):
    def __init__(self):
        # boat position
        self.pos = [0,0]
        # waypoint
        self.waypoint = [10, 1]
        # waypoint direction
        self.direction = 0
    
    def move(self, instruction):
       delta = int(instruction[1:])
       #pos_before = f"({self.pos[0]}, {self.pos[1]})"
       if (instruction[0] == 'N'):
           self.waypoint[1] += delta
       elif (instruction[0] == 'S'):
           self.waypoint[1] -= delta
       elif (instruction[0] == 'W'):
           self.waypoint[0] -= delta
       elif (instruction[0] == 'E'):
           self.waypoint[0] += delta
       elif (instruction[0] == 'F'):
           self.pos[0] += self.waypoint[0] * delta 
           self.pos[1] += self.waypoint[1] * delta 
       elif (instruction[0] == 'L'):
           # trig time
            radius = sqrt(self.waypoint[0]**2 + self.waypoint[1]**2)
            theta = atan2(self.waypoint[1], self.waypoint[0])
            self.waypoint[0] = round(radius*cos(theta+radians(delta)))
            self.waypoint[1] = round(radius*sin(theta+radians(delta)))
       elif (instruction[0] == 'R'):
            radius = sqrt(self.waypoint[0]**2 + self.waypoint[1]**2)
            theta = atan2(self.waypoint[1], self.waypoint[0])
            self.waypoint[0] = round(radius*cos(theta-radians(delta)))
            self.waypoint[1] = round(radius*sin(theta-radians(delta)))

       #print(pos_before, f" -> ({self.pos[0]},{self.pos[1]})")

second_ferry = WayPoint()
for instr in nav:
    second_ferry.move(instr)
print(second_ferry.manhattan_distance())