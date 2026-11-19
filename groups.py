import random


def group_sizes(total, mode, value):
    number = int(value)
    if mode == "size":
        count = total // number
        if total % number != 0:
            count = count + 1
    else:
        count = number
    sizes = []
    for index in range(count):
        size = total // count
        if index < total % count:
            size = size + 1
        sizes.append(size)
    return sizes


def pair_key(first, second):
    if first < second:
        return (first, second)
    return (second, first)


def count_pairs(history):
    old_groups = {}
    for row in history:
        key = (row["run"], row["group"])
        if key not in old_groups:
            old_groups[key] = []
        old_groups[key].append(row["roll"])
    pairs = {}
    for rolls in old_groups.values():
        for first in range(len(rolls)):
            for second in range(first + 1, len(rolls)):
                key = pair_key(rolls[first], rolls[second])
                if key not in pairs:
                    pairs[key] = 0
                pairs[key] = pairs[key] + 1
    return pairs


def score_student(student, group, fields, pairs, use_history):
    role_matches = 0
    branch_matches = 0
    year_matches = 0
    other_penalty = 0
    for member in group:
        if "role" in fields and student["role"] == member["role"]:
            role_matches = role_matches + 1
        if "branch" in fields and student["branch"] == member["branch"]:
            branch_matches = branch_matches + 1
        if "year" in fields and student["year"] == member["year"]:
            year_matches = year_matches + 1
        if "gender" in fields and student["gender"] == member["gender"]:
            other_penalty = other_penalty + 1
        if use_history:
            key = pair_key(student["roll"], member["roll"])
            if key in pairs:
                other_penalty = other_penalty + 2 * pairs[key]
    return (role_matches, branch_matches, year_matches, other_penalty)


def allocate_students(students, sizes, fields, pairs, use_history):
    order = students.copy()
    random.shuffle(order)
    groups = []
    for size in sizes:
        groups.append([])
    total_score = [0, 0, 0, 0]
    for student in order:
        best_index = -1
        best_score = (0, 0, 0, 0)
        for index in range(len(groups)):
            if len(groups[index]) >= sizes[index]:
                continue
            score = score_student(student, groups[index], fields, pairs, use_history)
            if best_index == -1 or score < best_score:
                best_index = index
                best_score = score
            elif score == best_score and len(groups[index]) < len(groups[best_index]):
                best_index = index
        groups[best_index].append(student)
        for index in range(4):
            total_score[index] = total_score[index] + best_score[index]
    return groups, tuple(total_score)


def make_groups(students, mode, value, fields, history, use_history):
    sizes = group_sizes(len(students), mode, value)
    pairs = {}
    if use_history:
        pairs = count_pairs(history)
    best_groups = []
    best_score = None
    for attempt in range(10):
        groups, score = allocate_students(students, sizes, fields, pairs, use_history)
        if best_score is None or score < best_score:
            best_groups = groups
            best_score = score
    return best_groups
