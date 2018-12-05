from collections import namedtuple, Counter, defaultdict
from itertools import repeat
from functools import reduce
import re


Night = namedtuple("Night", ["date", "guard", "events"])

Event = namedtuple("Event", ["is_awake", "minute"])


def chunk(ls, predicate):
    acc = []
    for l in ls:
        if predicate(l) and acc:
            yield acc
            acc = [l]
        else:
            acc.append(l)
    # the last chunk doesn't end with start of another
    yield acc


def extract_date(line):
    hour = int(line[12:14])
    date = int(line[9:11])
    if hour == "23":
        date += 1
    return date


def extract_minute(line):
    return int(line[15:17])


def extract_guard(line):
    regex = re.compile(r"#(\d+)")
    match = regex.search(line)
    if match:
        guard = int(match.group(1))
        return guard


def parse_event(line):
    return Event(minute=extract_minute(line), is_awake="wake" in line)


def parse_night(lines):
    date = extract_date(lines[0])
    guard = extract_guard(lines[0])
    events = list(parse_event(e) for e in lines[1:])
    return Night(date=date, guard=guard, events=events)


def minutes_asleep(night):
    slept = 0
    nap_start = None
    for e in night.events:
        if e.is_awake:
            slept += e.minute - nap_start
        else:
            nap_start = e.minute

    return slept


def sleep_map(events):
    result = Counter()

    if not events:
        return result

    e = 0
    awake = True
    event = events[e]
    for m in range(0, 60):
        if event.minute == m:
            awake = event.is_awake
            e += 1
            event = events[min(e, len(events) - 1)]
        if not awake:
            result[m] += 1
    return result


def sum_sleep_map(sleep_maps):
    acc = Counter()
    for m in sleep_maps:
        acc.update(m)
    return acc


# Part 1


def part_1(nights):
    # sleep_per_night_by_guard: [(guard, slept)]
    sleep_per_night = ((night.guard, minutes_asleep(night)) for night in nights)

    slept_by_guard = Counter()
    for (guard, slept) in sleep_per_night:
        slept_by_guard[guard] += slept

    # sg = sleepiest_guard

    # sg = sleepiest_guard
    (sg, _) = slept_by_guard.most_common(1)[0]

    sg_nights = filter(lambda n: n.guard == sg, nights)
    sg_map_sum = sum_sleep_map(map(lambda n: sleep_map(n.events), sg_nights))

    (minute, _freq) = sg_map_sum.most_common(1)[0]

    print(f"part 1: {sg * minute}")


def part_2(nights):
    # group nights by guard
    grouped = defaultdict(Counter)
    for night in nights:
        grouped[night.guard].update(sleep_map(night.events))

    # now we want to find the guard with the highest minute.
    guard = None
    freq = 0
    minute = None
    for (g, smap) in grouped.items():
        if smap:
            (m, f) = smap.most_common(1)[0]
            if f > freq:
                freq = f
                guard = g
                minute = m

    print(f"part 2: {guard * minute}")


log = open("input.txt").read().split("\n")
log.sort()  # pus the dates in order.

nights = list(parse_night(n) for n in chunk(log, lambda line: "begin" in line))

part_1(nights)
part_2(nights)
