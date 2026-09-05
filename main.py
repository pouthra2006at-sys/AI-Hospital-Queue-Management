from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = "database/hospital.db"


def create_database():

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS patients ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "age INTEGER NOT NULL, "
        "phone TEXT NOT NULL, "
        "department TEXT NOT NULL, "
        "token TEXT NOT NULL, "
        "status TEXT DEFAULT 'Waiting'"
        ")"
    )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        phone = request.form["phone"]
        department = request.form["department"]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]

        token_number = patient_count + 1
        token = f"A{token_number:03d}"

        patients_ahead = patient_count
        waiting_time = patients_ahead * 5

        cursor.execute(
            "INSERT INTO patients (name, age, phone, department, token) VALUES (?, ?, ?, ?, ?)",
            (name, age, phone, department, token)
        )

        connection.commit()
        connection.close()

        return render_template(
            "token.html",
            name=name,
            department=department,
            token=token,
            patients_ahead=patients_ahead,
            waiting_time=waiting_time
        )

    return render_template("register.html")


@app.route("/queue", methods=["GET", "POST"])
def queue():

    patient = None
    message = None
    patients_ahead = 0
    waiting_time = 0

    if request.method == "POST":

        token = request.form["token"].upper()

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE token = ?",
            (token,)
        )

        patient = cursor.fetchone()

        if patient:

            cursor.execute(
                "SELECT COUNT(*) FROM patients WHERE id < ? AND status = 'Waiting'",
                (patient[0],)
            )

            patients_ahead = cursor.fetchone()[0]
            waiting_time = patients_ahead * 5

        else:
            message = "Token not found"

        connection.close()

    return render_template(
        "queue.html",
        patient=patient,
        message=message,
        patients_ahead=patients_ahead,
        waiting_time=waiting_time
    )


@app.route("/admin")
def admin():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id ASC")
    patients = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE status = 'Waiting'"
    )
    waiting_patients = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE status = 'Completed'"
    )
    completed_patients = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        patients=patients,
        total_patients=total_patients,
        waiting_patients=waiting_patients,
        completed_patients=completed_patients
    )


@app.route("/complete/<int:patient_id>")
def complete_patient(patient_id):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE patients SET status = 'Completed' WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


create_database()


if __name__ == "__main__":
    app.run(debug=True)