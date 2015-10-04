# 0 0000 | halt
# 1 0001 > move right one cell
# 2 0010 < move left one cell
# 3 0011 ! invert cell
# 4 0100 ] loop end
# 5 0101 ^ move up
# 6 0110 v move down
# 7 0111 + add 1 hex
# 8 1000 [ loop start
# 9 1001 TODO exec position from up to down
# A 1010 TODO exec position from down to up
# B 1011 - substract 1 hex
# C 1100 TODO break 
# D 1101 TODO copypaste
# E 1110 TODO exec position from right to left
# F 1111 * exec position from left to right
import time
class Data:
    def __init__(self):
        self.pos = [1,1]
        self.tape = []
        for y in range(3):
            self.tape.append([])
            for x in range(32):
                self.tape[y].append("0")
        self.prgp = 0
        self.program = "17881478241b14"
#                       >+[[>]+[<]>->]   
        self.loopcount = 0
        self.color_reset='\033[0m'
        self.color_red='\033[31m'
        self.color_green='\033[32m'
        self.color_yellow='\033[93m'
        self.color_cyan='\033[36m'
        self.color_bold='\033[01m'
        self.nested_prgp = []
        self.nested = 0
                                                
    def draw(self):
        print("\033[2J", "\033[0;0H")
        o = []
        y = 0
        x = 0
        for line in self.tape:
            for c in line:
                if c != "0":
                    o.append(self.color_cyan + c + self.color_reset)
                if c == "0":
                    o.append(self.color_green + "0" + self.color_reset)
                if x == self.pos[1] and y == self.pos[0] - 1:
                    try:
                        o[x] = self.color_yellow + c + self.color_reset 
                    except IndexError:
                        pass
                x += 1
            p = ""
            for c in o:
                p += c
            print(p)
            o = []
            y += 1
        print(self.program)
        print(" " * self.prgp + "^")
        time.sleep(0.5)
    def halt(self):
        pass
        return 1
    def mvr1(self):
        self.pos[1] += 1
        self.draw()
        return 1
    def mvl1(self):
        self.pos[1] -= 1
        self.draw()
        return 1
    def invb(self):
        l = list(self.tape)
        l[self.pos[1]] = ~ self.tape[self.pos[1]]
        self.tape = "".join(l)
        self.draw()
        return 1
    def add1(self):
        l = list(self.tape[self.pos[0]])
        l[self.pos[1]] = str(hex(int(self.tape[self.pos[0]][self.pos[1]], 16) + 1))[2:]
        self.tape[self.pos[0]] = ''.join(l)
        self.draw()
        return 1
    def lend(self):
        if self.tape[self.pos[0]][self.pos[1]] != "0" and self.tape[self.pos[0]][self.pos[1]] != " ":
            self.draw()
            return -1 - self.nested_prgp.pop()
        else:
            self.draw()
            return 1
    def loop(self):
        self.start = self.prgp
        subprg = []
        self.nested_prgp.append(self.start)
        if self.tape[self.pos[0]][self.pos[1]] != "0" and self.tape[self.pos[0]][self.pos[1]] != " " and self.program[self.prgp] != "4":
            for c in range(self.prgp, len(self.program)):
                if self.program[c] == "4":
                    subprg.append(self.program[self.prgp + 1:c - 1])
                if self.program[c] == "8":
                    self.nested += 1
                    for d in range(c, len(self.program)):
                        if self.program[d] == "8":
                            self.nested += 1
                        if self.program[d] == "4" and self.nested > 0:
                            self.nested -= 1
                        if self.program[d] == "4" and self.nested == 0:
                            subprg.append(self.program[self.prgp + 1:d - 1])
                        else:
                            self.draw()
                            return 1
                self.nested_prgp.append(self.run(subprg.pop()))
                self.draw()
                print("nested:", self.nested)
        self.nested = 0
        return 1


#        else:
#            for i in range(self.prgp, len(self.program)):
#                if self.program[i] == "4":
#                    self.draw()
#                    return self.start - self.prgp
#                else:
#                    pass
    def sub1(self):
        l = list(self.tape[self.pos[0]])
        l[self.pos[1]] = str(hex(int(self.tape[self.pos[0]][self.pos[1]], 16) - 1))[2:]
        self.tape[self.pos[0]] = ''.join(l)
        self.draw()
        return 1
    def brea(self):
        pass
        return 1
    def hex2prg(self):
        l = ""
        m = ""
        self.program = "".join(self.program.split())
        self.program = self.program.strip()
        self.tape = self.tape.strip()
    #    for hx in self.program:
    #        l.append(commands[int(hx, 16)])
#        for i in range(4, len(self.tape), 4):
#            l += hex(int(self.tape[i-4:i], 2))[2:]

        return l
    def exep(self):
        i = self.prgp
        prg = self.tape
        l = []
        self.program = prg
        self.tape = "00000000"
        self.prgp = 0
        self.run(prg)
    #    while i < len(prg) - 1:
    #        prg[i]()
    #        i += 1
    #        draw()
        return i
    def mvu1(self):
        self.pos[0] -= 1
        self.draw()
        return 1
    def mvd1(self):
        self.pos[0] += 1
        self.draw()
        return 1
    def exed(self):
        pass
    def exeu(self):
        pass
    def copa(self):
        pass
    def exel(self):
        pass

    commands = [halt, mvr1, mvl1, invb, lend, mvu1, mvd1, add1, loop, exed, exeu, sub1, brea, copa, exel, exep]
    def run(self, prg):
        i = 0
        while self.prgp <= len(prg) - 1:
            self.prgp += self.commands[int(prg[self.prgp], 16)](self)
            i += 1
        return self.prgp
    def tape2hex(self):
        newt = ""
        for i in range(len(self.tape), 4, 1):
            newt += hex(int(self.tape[i:i+4], 2))[2:]
        return newt

p = Data()
p.draw()
p.run(p.program)
p.draw()
