import sys


def new_recipes(a, b, recipes):
    s = recipes[a] + recipes[b]

    if s >= 10:
        recipes.append(s // 10)
        recipes.append(s % 10)
    else:
        recipes.append(s)


def move_elf(elf, recipes):
    return (elf + recipes[elf] + 1) % len(recipes)


def part_1(a, b, recipes, max_recipes):
    recipes = recipes[:]
    while len(recipes) < max_recipes + 10:
        new_recipes(a, b, recipes)
        a = move_elf(a, recipes)
        b = move_elf(b, recipes)

    print("part 1:", "".join(str(r) for r in recipes[-10:]))


def part_2(a, b, recipes, pattern):
    i = 0
    # what if we add two a turn?
    while (recipes[-len(pattern) :] != pattern) and (
        recipes[-len(pattern) - 1 : -1] != pattern
    ):
        new_recipes(a, b, recipes)
        a = move_elf(a, recipes)
        b = move_elf(b, recipes)
        i += 1
        if i % 1_000_000 == 0:
            print("at {:,} recipes".format(i))

    if recipes[-len(pattern) :] == pattern:
        print("part 2:", len(recipes) - len(pattern))
    elif recipes[-len(pattern) - 1 : -1] == pattern:
        print("part 2:", len(recipes) - len(pattern) - 1)
    else:
        print("oh no!")


puzzle_input = sys.argv[1]

part_1(0, 1, [3, 7], int(puzzle_input))
part_2(0, 1, [3, 7], list(int(digit) for digit in puzzle_input))
