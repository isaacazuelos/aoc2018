def update(state, rules):
    tng = set()
    min_pot = min(state)
    max_pot = max(state)
    for pot in range(min_pot - 2, max_pot + 3):
        key = ""

        for p in range(-2, 3):
            if (pot + p) in state:
                key += "#"
            else:
                key += "."

        if key in rules and rules[key] == "#":
            tng.add(pot)

    return frozenset(tng)


def downshift_state(state):
    down_shift = min(state)
    new = frozenset(pot - down_shift for pot in state)
    return (new, down_shift)


def upshift_state(state, shift):
    return frozenset(pot + shift for pot in state)


def part_1(state, rules, gen_count):
    for _ in range(gen_count):
        state = update(state, rules)

    count = sum(state)

    print(f"part 1: {count}")


def part_2(state, rules, gen_count):
    FUTURE = 50_000_000_000

    seen_states = {}

    start = None
    end = None
    drift_per_cycle = None

    for gen in range(gen_count):

        (ds, shift) = downshift_state(state)

        if ds in seen_states:
            (start, start_shift) = seen_states[ds]
            drift_per_cycle = shift - start_shift
            end = gen
            break
        else:
            seen_states[ds] = (gen, shift)
            state = update(state, rules)

    # it's just shifting by 1 every cycle from here, but if it were a nice
    # kite, we'd still have what we need here!
    #
    # if this wasn't true we could modulo and use the cycle in seen_states by
    # reverse lookup of the gens
    assert drift_per_cycle == 1

    print("part 2:", sum(upshift_state(state, FUTURE - end)))


lines = open("input.txt", "r").read().split("\n")

# for pots -1, -2
state = set()
for pot, plant in enumerate(lines[0][15:]):
    if plant == "#":
        state.add(pot)

# a state is just a set of (filled) pots
state = frozenset(state)

rules = {}
for line in lines[2:]:
    [l, r] = line.split(" => ")
    rules[l] = r

generations = 20

part_1(state, rules, generations)
part_2(state, rules, 50_000_000_000)
