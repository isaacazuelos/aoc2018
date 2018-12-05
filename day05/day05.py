from collections import namedtuple, Counter, defaultdict
from itertools import repeat
from functools import reduce


def scan_once(units):

    if len(units) < 2:
        return units

    i = 0
    while i < len(units) - 1:
        l = units[i]
        r = units[i + 1]
        if (l.lower() == r.lower()) and (l.isupper() != r.isupper()):
            # must remove further one first, otherwise it moves.
            del units[i + 1]
            del units[i]
            continue
        else:
            i += 1

    return units


def scan(units):
    while True:
        len_before = len(units)
        scan_once(units)
        if len(units) == len_before:
            break

    return "".join(units)


def part_1(polymer):
    print("part 1 is pretty slow..")
    units = list(polymer)
    scan(units)
    print(f"part 1: {len(units)}")


def scan_filtering(units, char):
    char = char.lower()
    remaining = list(filter(lambda c: c.lower() != char, units))
    scan(remaining)
    return remaining


def part_2(polymer):
    print("part 2 is even more slow...")
    units = list(polymer)
    shortest = len(units)
    letters = "abcdefghijklmnopqrstuvwxyz"
    for letter in letters:
        remaining = scan_filtering(units, letter)
        rem_len = len(remaining)
        print(f"trying letter: {letter}, len: {rem_len}")
        if rem_len < shortest:
            shortest = rem_len
    print(f"part 2: {shortest}")


polymer = open("input.txt", "r").read().strip()

part_1(polymer)
part_2(polymer)
