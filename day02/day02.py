import itertools


def has_letter_twice(s):
    counts = {}
    for letter in s:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return 2 in counts.values()


def has_letter_thrice(s):
    counts = {}
    for letter in s:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return 3 in counts.values()


def checksum(lines):
    twos = 0
    threes = 0

    for line in lines:
        if has_letter_twice(line):
            twos += 1
        if has_letter_thrice(line):
            threes += 1

    return twos * threes


def correct_ids(l, r):
    same = ""
    differ_count = 0
    for cl, cr in zip(l, r):
        if cl == cr:
            same += cl
        else:
            differ_count += 1
    if differ_count == 1:
        return same
    else:
        return None


lines = open("input.txt").readlines()

print("part 1:", checksum(lines))

for a in lines:
    for b in lines:
        if a == b:
            continue
        match = correct_ids(a, b)
        if match:
            print("part 2:", match)
