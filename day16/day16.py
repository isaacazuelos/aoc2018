import sys
from collections import namedtuple, defaultdict

Instr = namedtuple("Instr", ["op", "a", "b", "c"])
Sample = namedtuple("Sample", ["instr", "before", "after"])
# type State: [int; 4]
# type Operation: (Instr, State) -> State


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


ALL_OPS = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtri,
    gtir,
    gtrr,
    eqri,
    eqir,
    eqrr,
]


def parse_instr(line):
    (op, a, b, c) = map(int, line.split(" "))
    return Instr(op=op, a=a, b=b, c=c)


def parse_part_1(string):
    samples = []
    lines = string.split("\n")
    for i in range(0, len(lines), 4):
        # lol eval
        before = eval(lines[i + 0][7:])
        instr = parse_instr(lines[i + 1])
        after = eval(lines[i + 2][7:])

        samples.append(Sample(instr=instr, before=before, after=after))
    return samples


def parse_part_2(string):
    prog = []
    for line in string.strip().split("\n"):
        prog.append(parse_instr(line))

    return prog


def part_1(samples):
    possibilities = []
    for s in samples:
        ops_with_expected_result = []
        for op in ALL_OPS:
            if s.after == op(s.instr, s.before):
                ops_with_expected_result.append((s.instr.op, op))
        possibilities.append(ops_with_expected_result)

    i = 0
    for ops in possibilities:
        if len(ops) >= 3:
            i += 1

    print("part 1:", i)


def decode_ops(samples):
    known = {}
    unsure = defaultdict(set)

    for s in samples:
        for op in ALL_OPS:
            if s.after == op(s.instr, s.before):
                unsure[s.instr.op].add(op)

    while unsure:
        for opcode, options in list(unsure.items()):
            if len(options) == 1:
                operation = options.pop()
                # it's know!
                known[opcode] = operation
                del unsure[opcode]

                # remove from other unsure
                for options in unsure.values():
                    if operation in options:
                        options.remove(operation)

            elif len(unsure[opcode]) == 0:
                del unsure[opcode]

    return known


def part_2(samples, program):
    state = [0, 0, 0, 0]
    machine = decode_ops(samples)

    for instr in program:
        state = machine[instr.op](instr, state)

    print("part 2:", state[0])


puzzle = open(sys.argv[1], "r").read()

[part1_input, part2_input] = puzzle.split("\n\n\n")

samples = parse_part_1(part1_input)
part_1(samples)

program = parse_part_2(part2_input)
part_2(samples, program)


# space: {opcode: Set Operation }
# for (opcode, input, output) in example:
#   for operation in space[opcode]:
#     if opreation(input) != output:
#        space.remove(operation)
