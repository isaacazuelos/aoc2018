from collections import namedtuple

Tree = namedtuple("Tree", ["children", "metadata"])


def treeify(numbers):
    child_count = numbers.pop()
    meta_count = numbers.pop()
    children = []
    metadata = []

    for _ in range(child_count):
        children.append(treeify(numbers))

    for _ in range(meta_count):
        metadata.append(numbers.pop())

    return Tree(children=children, metadata=metadata)


def part_1(tree):
    print(f"part 1:", sum_meta(tree))


def sum_meta(tree):
    acc = sum(tree.metadata)
    for child in tree.children:
        acc += sum_meta(child)

    return acc


def part_2_value(tree):
    if tree.children:
        value = 0
        for one_based_index in tree.metadata:
            if one_based_index == 0:
                continue
            elif one_based_index <= len(tree.children):
                value += part_2_value(tree.children[one_based_index - 1])
        return value
    else:
        return sum(tree.metadata)


def part_2(tree):
    print("part 2:", part_2_value(tree))


numbers = list(int(digits) for digits in open("input.txt", "r").read().split(" "))
numbers.reverse()
tree = treeify(numbers)

part_1(tree)
part_2(tree)
