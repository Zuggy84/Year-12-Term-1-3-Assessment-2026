from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from datetime import datetime
app = Flask(__name__)
engine = create_engine("sqlite:///Assessment_Tracker.db", echo = True)
connection = engine.connect()
user_log_in_status = False
user_id_fetch = None
@app.route("/")
def home():
    return render_template("home.html", user_log_in_status = user_log_in_status)
@app.route("/log_in", methods = ["GET", "POST"])
def log_in():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        query = text("SELECT * FROM users WHERE user_name = :user_name AND user_password = :user_password;")
        results = connection.execute(query, {"user_name": user_name, "user_password": user_password}).fetchone()
        if results:
            query = text("SELECT user_id FROM users WHERE user_name = :user_name AND user_password = :user_password;")
            results = connection.execute(query, {"user_name": user_name, "user_password": user_password}).fetchone()
            if results:
                global user_id_fetch
                user_id_fetch = int(results[0])
            global user_log_in_status
            user_log_in_status = True
            return render_template("home.html", user_log_in_status = user_log_in_status)
        else:
            user_log_in_unsuccessful = True
            return render_template("log_in.html", user_log_in_unsuccessful = user_log_in_unsuccessful, user_log_in_status = user_log_in_status)
    return render_template("log_in.html", user_log_in_status = user_log_in_status)
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        query = text("INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password);")
        connection.execute(query, {"user_name": user_name, "user_password": user_password})
        connection.commit()
        query = text("SELECT user_id FROM users WHERE user_name = :user_name AND user_password = :user_password;")
        results = connection.execute(query, {"user_name": user_name, "user_password": user_password}).fetchone()
        if results:
            global user_id_fetch
            user_id_fetch = int(results[0])
        global user_log_in_status
        user_log_in_status = True
        return render_template("home.html", user_log_in_status = user_log_in_status)
    return render_template("register.html", user_log_in_status = user_log_in_status)
@app.route("/assessments")
def assessments():
    query = text("SELECT * FROM assessments WHERE user_id = :user_id_fetch;")
    results = connection.execute(query, {"user_id_fetch": user_id_fetch}).fetchall()
    return render_template("assessments.html", assessments = results, user_log_in_status = user_log_in_status)
@app.route("/subjects")
def subjects():
    query = text("SELECT assessment_subject FROM assessments WHERE user_id = :user_id_fetch;")
    results = connection.execute(query, {"user_id_fetch": user_id_fetch}).fetchall()
    return render_template("subjects.html", subjects = results, user_log_in_status = user_log_in_status)
@app.route("/add_assessments", methods = ["GET", "POST"])
def add_assessments():
    if request.method == "POST":
        user_id = user_id_fetch
        assessment_type = request.form["assessment_type"]
        assessment_subject = request.form["assessment_subject"]
        assessment_issue_date = request.form["assessment_issue_date"]
        assessment_due_date_and_time = request.form["assessment_due_date_and_time"]
        assessment_grade_weight = request.form["assessment_grade_weight"]
        assessment_task_explanation = request.form["assessment_task_explanation"]
        query = text("INSERT INTO assessments (user_id, assessment_type, assessment_subject, assessment_issue_date, assessment_due_date_and_time, assessment_grade_weight, assessment_task_explanation) VALUES (:user_id, :assessment_type, :assessment_subject, :assessment_issue_date, :assessment_due_date_and_time, :assessment_grade_weight, :assessment_task_explanation);")
        connection.execute(query, {"user_id": user_id, "assessment_type": assessment_type, "assessment_subject": assessment_subject, "assessment_issue_date": assessment_issue_date, "assessment_due_date_and_time": assessment_due_date_and_time, "assessment_grade_weight": assessment_grade_weight, "assessment_task_explanation": assessment_task_explanation})
        connection.commit()
        return render_template("add_assessments.html", user_log_in_status = user_log_in_status)
    return render_template("add_assessments.html", user_log_in_status = user_log_in_status)
if __name__ == "__main__":
    app.run(debug = True, reloader_type = "stat", port = 5000)