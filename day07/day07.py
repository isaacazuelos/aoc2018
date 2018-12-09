from collections import defaultdict
from functools import cmp_to_key
from itertools import repeat

# If I were smarter I'd use a proper transitive closure algorithm and then sort.


def extract_pairs(line):
    l = line[5:6]
    r = line[36:37]
    return (l, r)


def remove_available(dependencies, available):
    for step in list(dependencies.keys()):  # for each step
        if not dependencies[step]:  # if that step has no dependencies
            available.append(step)  # it's available!
            del dependencies[step]


def remove_complete(dependencies, complete):
    for step in dependencies:
        if complete in dependencies[step]:
            dependencies[step].remove(complete)


def part_1(deps):
    complete = ""
    available = []

    while deps:
        remove_available(deps, available)
        available = sorted(available, reverse=True)
        a = available.pop()
        complete += a
        remove_complete(deps, a)

    print("part 1:", complete)


def time_for_step(step, base_seconds):
    return ord(step) - ord("A") + base_seconds


def complete_work(workers, second, deps):
    newly_complete = []
    for worker, (time_complete, step) in enumerate(workers):
        if time_complete < second and step is not None:
            newly_complete.append(step)
            workers[worker] = (0, None)
    return newly_complete


def take_work(workers, available, second, base_seconds):
    for worker, (_, current_step) in enumerate(workers):
        if available and (current_step is None):
            step = available.pop()
            workers[worker] = (second + time_for_step(step, base_seconds), step)
        # otherwise there's no work to take.


def part_2(deps, count, base_seconds):
    complete = []
    second = -1
    workers = list(repeat((0, None), count))  # all workers are ready to work.
    available = []
    while deps or any(worker[1] for worker in workers):
        second += 1
        complete_this_second = complete_work(workers, second, deps)
        for s in complete_this_second:
            remove_complete(deps, s)
            complete.append(s)

        remove_available(deps, available)
        available = sorted(available, reverse=True)
        take_work(workers, available, second, base_seconds)

        # print(
        #     f"""second: {second},
        # complete: {complete},
        # available:{available},
        # workers: {workers},
        # deps: {deps}"""
        # )

    print("part 2:", second)


lines = open("input.txt", "r").read().split("\n")
pairs = list(extract_pairs(line) for line in lines)

complete = ""
available = []


def mk_deps():
    # dict(char, set(char)) where the set is dependencies
    deps = defaultdict(set)
    for dep, step in pairs:
        deps[step].add(dep)
        # every step needs to be in there at the start
        if dep not in deps:
            deps[dep] = set()
    return deps


part_1(mk_deps())
part_2(mk_deps(), 5, 60)
