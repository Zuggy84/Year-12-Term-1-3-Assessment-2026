from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from datetime import datetime
app=Flask(__name__)
engine=create_engine('sqlite:///Assessment_Tracker.db', echo=True)
connection=engine.connect()
user_log_in_status=False
@app.route('/')
def home():
    return render_template('home.html', user_log_in_status=user_log_in_status)
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method=='POST':
        user_name=request.form['user_name']
        user_password=request.form['user_password']
        query=text('SELECT * FROM users WHERE user_name=:user_name AND user_password=:user_password;')
        results=connection.execute(query, {'user_name': user_name, 'user_password': user_password}).fetchone()
        if results:
            query=text('SELECT user_id FROM users WHERE user_name=:user_name AND user_password=:user_password;')
            results=connection.execute(query, {'user_name': user_name, 'user_password': user_password}).fetchone()
            if results:
                user_id_users=results
            user_log_in_status=True
            return render_template('home.html', user_log_in_status=user_log_in_status, user_id_users=user_id_users)
        else:
            user_log_in_unsuccessful=True
            return render_template('log_in.html', user_log_in_unsuccessful=user_log_in_unsuccessful)
    return render_template('log_in.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        user_name=request.form['user_name']
        user_password=request.form['user_password']
        query=text('INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password);')
        connection.execute(query, {'user_name': user_name, 'user_password': user_password})
        connection.commit()
        query=text('SELECT user_id FROM users WHERE user_name=:user_name AND user_password=:user_password;')
        results=connection.execute(query, {'user_name': user_name, 'user_password': user_password}).fetchone()
        if results:
            user_id_users=results
        user_log_in_status=True
        return render_template('home.html', user_log_in_status=user_log_in_status, user_id_users=user_id_users)
    return render_template('register.html')
@app.route('/assessments')
def assessments():
    query=text('SELECT * FROM assessments;')
    results=connection.execute(query).fetchall()
    return render_template('assessments.html', assessments=results)
@app.route('/subjects')
def subjects():
    query=text('SELECT assessment_subject FROM assessments;')
    results=connection.execute(query).fetchall()
    return render_template('subjects.html', subjects=results)
if __name__=='__main__':
    app.run(debug=True, reloader_type='stat', port=5000)