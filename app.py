import csv
from flask import Flask, redirect, render_template, request, send_file, url_for

from groups import make_groups
from students import load_groups, load_students, read_history, save_groups, student_fields


app = Flask(__name__)


@app.route("/")
def home():
    students = load_students()
    return render_template("index.html", students=students)


@app.route("/students", methods=["POST"])
def import_students():
    file = request.files["file"]
    file.save("students.csv")
    return redirect(url_for("home"))


@app.route("/groups", methods=["POST"])
def generate_groups():
    students = load_students()
    history = read_history()
    mode = request.form["mode"]
    value = request.form["value"]
    fields = request.form.getlist("fields")
    use_history = request.form.get("history") == "on"
    groups = make_groups(students, mode, value, fields, history, use_history)
    save_groups(groups)
    return redirect(url_for("show_groups"))


@app.route("/groups")
def show_groups():
    groups = load_groups()
    return render_template("groups.html", groups=groups)


@app.route("/groups.csv")
def export_groups():
    groups = load_groups()
    with open("groups.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["group"] + student_fields)
        writer.writeheader()
        for index in range(len(groups)):
            for student in groups[index]:
                row = {"group": str(index + 1)}
                for field in student_fields:
                    row[field] = student[field]
                writer.writerow(row)
    return send_file("groups.csv", as_attachment=True)


if __name__ == "__main__":
    app.run()
