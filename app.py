from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "hospital_queue_secret_key"

DATABASE = "database/hospital.db"


# Create Database Tables
def create_database():

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Patients Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            token TEXT NOT NULL,
            status TEXT DEFAULT 'Waiting'
        )
    """)

    # Add Priority Column
    try:
        cursor.execute(
            "ALTER TABLE patients ADD COLUMN priority TEXT DEFAULT 'Normal'"
        )
    except sqlite3.OperationalError:
        pass

    # Doctors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            consultation_time INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()
@app.route("/")
def home():

    return render_template("index.html")


# Patient Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        phone = request.form["phone"]
        department = request.form["department"]
        priority = request.form["priority"]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        # Generate Token
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]

        token_number = patient_count + 1
        token = f"A{token_number:03d}"

        # Get consultation time for selected department
        cursor.execute(
            """
            SELECT consultation_time
            FROM doctors
            WHERE department = ?
            """,
            (department,)
        )

        doctor_data = cursor.fetchone()

        if doctor_data:
            consultation_time = doctor_data[0]
        else:
            consultation_time = 10

        # Count waiting patients in same department
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patients
            WHERE department = ?
            AND status = 'Waiting'
            """,
            (department,)
        )

        patients_ahead = cursor.fetchone()[0]

        # Calculate waiting time
        waiting_time = patients_ahead * consultation_time

        # Insert Patient
        cursor.execute("""
            INSERT INTO patients
            (name, age, phone, department, token,priority)
            VALUES (?, ?, ?, ?, ?,?)
        """, (
            name,
            age,
            phone,
            department,
            token,
            priority
        ))

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

    # Get departments from doctors table
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT DISTINCT department FROM doctors ORDER BY department"
    )

    departments = cursor.fetchall()

    connection.close()

    return render_template(
        "register.html",
        departments=departments
    )


# Queue Status
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

        # Find Patient
        cursor.execute(
            "SELECT * FROM patients WHERE token = ?",
            (token,)
        )

        patient = cursor.fetchone()

        if patient:

            department = patient[4]
            priority = patient[7]

            # Get consultation time
            cursor.execute(
                """
                SELECT consultation_time
                FROM doctors
                WHERE department = ?
                """,
                (department,)
            )

            doctor_data = cursor.fetchone()

            if doctor_data:
                consultation_time = doctor_data[0]
            else:
                consultation_time = 10


            # Emergency patient
            if priority == "Emergency":

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM patients
                    WHERE department = ?
                    AND status = 'Waiting'
                    AND priority = 'Emergency'
                    AND id < ?
                    """,
                    (department, patient[0])
                )

            # Normal patient
            else:

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM patients
                    WHERE department = ?
                    AND status = 'Waiting'
                    AND (
                        priority = 'Emergency'
                        OR id < ?
                    )
                    """,
                    (department, patient[0])
                )

            patients_ahead = cursor.fetchone()[0]

            waiting_time = patients_ahead * consultation_time

        else:

            message = "Token not found. Please check your token number."

        connection.close()

    return render_template(
        "queue.html",
        patient=patient,
        message=message,
        patients_ahead=patients_ahead,
        waiting_time=waiting_time
    )

# AI Queue Prediction
def predict_queue():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            department,
            COUNT(*)
        FROM patients
        WHERE status = 'Waiting'
        GROUP BY department
    """)

    department_patients = cursor.fetchall()

    total_waiting_time = 0
    total_waiting_patients = 0

    for department, patient_count in department_patients:

        cursor.execute(
            """
            SELECT consultation_time
            FROM doctors
            WHERE department = ?
            LIMIT 1
            """,
            (department,)
        )

        doctor_data = cursor.fetchone()

        if doctor_data:
            consultation_time = doctor_data[0]
        else:
            consultation_time = 10

        total_waiting_time += (
            patient_count * consultation_time
        )

        total_waiting_patients += patient_count

    connection.close()

    if total_waiting_patients <= 3:
        crowd_level = "Low"

    elif total_waiting_patients <= 7:
        crowd_level = "Medium"

    else:
        crowd_level = "High"

    return total_waiting_time, crowd_level


# Admin Login
@app.route("/login", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect("/admin")

        else:

            message = "Invalid username or password!"

    return render_template(
        "login.html",
        message=message
    )


# Doctor Management
@app.route("/doctor", methods=["GET", "POST"])
def doctor():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        consultation_time = request.form["consultation_time"]

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO doctors
            (name, department, consultation_time)
            VALUES (?, ?, ?)
        """, (
            name,
            department,
            consultation_time
        ))

        connection.commit()
        connection.close()

        return redirect("/doctor")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM doctors ORDER BY id ASC"
    )

    doctors = cursor.fetchall()

    connection.close()

    return render_template(
        "doctor.html",
        doctors=doctors
    )
    # Edit Doctor
@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
def edit_doctor(doctor_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        consultation_time = request.form["consultation_time"]

        cursor.execute(
            """
            UPDATE doctors
            SET name = ?,
                department = ?,
                consultation_time = ?
            WHERE id = ?
            """,
            (
                name,
                department,
                consultation_time,
                doctor_id
            )
        )

        connection.commit()
        connection.close()

        return redirect("/doctor")

    cursor.execute(
        "SELECT * FROM doctors WHERE id = ?",
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_doctor.html",
        doctor=doctor
    )
    # Doctor-wise Patient Queue
@app.route("/doctor_queue/<int:doctor_id>")
def doctor_queue(doctor_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Get selected doctor
    cursor.execute(
        "SELECT * FROM doctors WHERE id = ?",
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    # Get waiting patients for doctor's department
    cursor.execute(
        """
        SELECT * FROM patients
        WHERE department = ?
        AND status = 'Waiting'
        ORDER BY id ASC
        """,
        (doctor[2],)
    )

    patients = cursor.fetchall()
def predict_queue():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT department, COUNT(*)
        FROM patients
        WHERE status = 'Waiting'
        GROUP BY department
    """)

    department_patients = cursor.fetchall()

    total_waiting_time = 0
    total_waiting_patients = 0

    for department, patient_count in department_patients:

        cursor.execute(
            """
            SELECT consultation_time
            FROM doctors
            WHERE department = ?
            LIMIT 1
            """,
            (department,)
        )

        doctor_data = cursor.fetchone()

        if doctor_data:
            consultation_time = doctor_data[0]
        else:
            consultation_time = 10

        total_waiting_time += patient_count * consultation_time
        total_waiting_patients += patient_count

    connection.close()

    if total_waiting_patients <= 3:
        crowd_level = "Low"

    elif total_waiting_patients <= 7:
        crowd_level = "Medium"

    else:
        crowd_level = "High"

    return total_waiting_time, crowd_level
# Delete Doctor
@app.route("/delete_doctor/<int:doctor_id>")
def delete_doctor(doctor_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM doctors WHERE id = ?",
        (doctor_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/doctor")


# Admin Dashboard
@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients ORDER BY id ASC"
    )

    patients = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )

    total_patients = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE status = 'Waiting'"
    )

    waiting_patients = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE status = 'Completed'"
    )

    completed_patients = cursor.fetchone()[0]

    estimated_time, crowd_level = predict_queue()

    # Department-wise Patient Count
    cursor.execute("""
        SELECT department, COUNT(*)
        FROM patients
        GROUP BY department
    """)

    department_data = cursor.fetchall()

    connection.close()

    return render_template(
        "admin.html",
        patients=patients,
        total_patients=total_patients,
        waiting_patients=waiting_patients,
        completed_patients=completed_patients,
        estimated_time=estimated_time,
        crowd_level=crowd_level,
        department_data=department_data
    )


# Mark Patient Completed
@app.route("/complete/<int:patient_id>")
def complete_patient(patient_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE patients SET status = 'Completed' WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


# Delete Patient
@app.route("/delete/<int:patient_id>")
def delete_patient(patient_id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")
@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect("/login")


# Create Database
create_database()


# Run Application
if __name__ == "__main__":

    app.run(debug=True)