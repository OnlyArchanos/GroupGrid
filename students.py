import csv


student_fields = ["roll", "name", "year", "branch", "gender", "role"]
history_fields = ["run", "group"] + student_fields


def load_students():
    students = []
    try:
        with open("students.csv", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        return []
    return students


def read_history():
    rows = []
    try:
        with open("history.csv", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        return []
    return rows


def save_groups(groups):
    rows = read_history()
    run = 1
    if rows:
        run = int(rows[-1]["run"]) + 1
    with open("history.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=history_fields)
        if not rows:
            writer.writeheader()
        for index in range(len(groups)):
            for student in groups[index]:
                row = {"run": str(run), "group": str(index + 1)}
                for field in student_fields:
                    row[field] = student[field]
                writer.writerow(row)


def load_groups():
    rows = read_history()
    groups = []
    if rows:
        latest = rows[-1]["run"]
        for row in rows:
            if row["run"] == latest:
                number = int(row["group"])
                while len(groups) < number:
                    groups.append([])
                student = {}
                for field in student_fields:
                    student[field] = row[field]
                groups[number - 1].append(student)
    return groups
