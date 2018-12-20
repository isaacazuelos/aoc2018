import sys
from itertools import repeat
from collections import namedtuple

Instr = namedtuple("Instr", ["op", "a", "b", "c"])


class State:
    def __init__(self, ip=None, ipp=None, reg=None, code=None):
        self.ip = ip
        self.ipp = ipp
        self.reg = reg
        self.code = code


# State = namedtuple("State", ["ip", "ipp", "reg", "code"])


def addr(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] + state[instr.b]
    return new


def addi(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] + instr.b
    return new


def mulr(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] * state[instr.b]
    return new


def muli(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] * instr.b
    return new


def banr(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] & state[instr.b]
    return new


def bani(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] & instr.b
    return new


def borr(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] | state[instr.b]
    return new


def bori(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a] | instr.b
    return new


def setr(instr, state):
    new = state[:]
    new[instr.c] = state[instr.a]
    return new


def seti(instr, state):
    new = state[:]
    new[instr.c] = instr.a
    return new


def gtir(instr, state):
    new = state[:]
    new[instr.c] = int(instr.a > state[instr.b])
    return new


def gtri(instr, state):
    new = state[:]
    new[instr.c] = int(state[instr.a] > instr.b)
    return new


def gtrr(instr, state):
    new = state[:]
    new[instr.c] = int(state[instr.a] > state[instr.b])
    return new


def eqir(instr, state):
    new = state[:]
    new[instr.c] = int(instr.a == state[instr.b])
    return new


def eqri(instr, state):
    new = state[:]
    new[instr.c] = int(state[instr.a] == instr.b)
    return new


def eqrr(instr, state):
    new = state[:]
    new[instr.c] = int(state[instr.a] == state[instr.b])
    return new


ALL_OPS = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtri": gtri,
    "gtir": gtir,
    "gtrr": gtrr,
    "eqri": eqri,
    "eqir": eqir,
    "eqrr": eqrr,
}


def parse_ip(line):
    return int(line.split(" ")[-1])


def parse_instr(line):
    (op, a, b, c) = line.split(" ")
    return Instr(op=op, a=int(a), b=int(b), c=int(c))


def str_state(state):
    instr = state.code[state.ip]
    instr_str = f"{instr.op} {instr.a} {instr.b} {instr.c}"
    return f"ip={state.ip} {state.reg} {instr_str}"


def execute(reg, instr):
    # perform operation
    operation = ALL_OPS[instr.op]
    new_reg = operation(instr, reg)
    return new_reg


def tick(state, print_state=False):
    if print_state:
        print(str_state(state))

    state.reg[state.ipp] = state.ip

    instr = state.code[state.ip]
    state.reg = execute(state.reg, instr)

    state.ip = state.reg[state.ipp]
    state.ip += 1


def halted(state):
    return not (0 <= state.ip < len(state.code))


def run(state, print_state=False):
    while not halted(state):
        tick(state, print_state=print_state)


def part_1(state):
    run(state)
    print("part 1:", state.reg[0])


def part_2(state):
    run(state, print_state=True)
    print("part 2:", state.reg[0])


puzzle = open(sys.argv[1], "r").read().split("\n")

ipp = parse_ip(puzzle[0])

code = list(map(parse_instr, puzzle[1:]))

start_state = State(ip=0, ipp=ipp, code=code, reg=list(repeat(0, 6)))

part_1(start_state)

correct_start_state = State(ip=0, ipp=ipp, code=code, reg=[1, 0, 0, 0, 0, 0])

# part_2(correct_start_state)
