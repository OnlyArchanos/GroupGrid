import csv
import io
import os

from flask import Flask, Response, redirect, render_template, request, url_for

from groups import make_groups
from students import load_groups, load_students, read_history, save_groups, student_fields


app = Flask(__name__)
app.config["DATA_FOLDER"] = os.path.join(app.root_path, "data")
os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)


@app.route("/")
def home():
    students = load_students(app.config["DATA_FOLDER"])
    return render_template("index.html", students=students)


@app.route("/students", methods=["POST"])
def import_students():
    file = request.files["file"]
    path = os.path.join(app.config["DATA_FOLDER"], "students.csv")
    file.save(path)
    return redirect(url_for("home"))


@app.route("/groups", methods=["POST"])
def generate_groups():
    folder = app.config["DATA_FOLDER"]
    students = load_students(folder)
    history = read_history(folder)
    mode = request.form["mode"]
    value = request.form["value"]
    fields = request.form.getlist("fields")
    use_history = request.form.get("history") == "on"
    groups = make_groups(students, mode, value, fields, history, use_history)
    save_groups(folder, groups)
    return redirect(url_for("show_groups"))


@app.route("/groups")
def show_groups():
    groups = load_groups(app.config["DATA_FOLDER"])
    return render_template("groups.html", groups=groups)


@app.route("/groups.csv")
def export_groups():
    groups = load_groups(app.config["DATA_FOLDER"])
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["group"] + student_fields)
    writer.writeheader()
    for index in range(len(groups)):
        for student in groups[index]:
            row = {"group": str(index + 1)}
            for field in student_fields:
                row[field] = student[field]
            writer.writerow(row)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=groups.csv"}
    )


if __name__ == "__main__":
    app.run()
