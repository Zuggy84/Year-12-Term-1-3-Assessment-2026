from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
from datetime import datetime
app=Flask(__name__)
engine1=create_engine('sqlite:///Assessments.db', echo=True)
engine2=create_engine('sqlite:///Users.db', echo=True)
connection1=engine1.connect()
connection2=engine2.connect()
@app.route('/')
def home():
    return render_template('home_not_logged_in.html')
@app.route('/home_logged_in')
def home_logged_in():
    return render_template('home_logged_in.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        query=text('SELECT * FROM users WHERE username=:username AND password=:password;')
        results=connection2.execute(query, {'username': username, 'password': password}).fetchone()
        if results:
            return render_template('home_logged_in.html')
        else:
            user_not_logged_in=True
            return render_template('login.html', user_not_logged_in=user_not_logged_in)
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        query=text('INSERT INTO users (username, password) VALUES (:username, :password);')
        connection2.execute(query, {'username': username, 'password': password})
        connection2.commit()
        return render_template('home_logged_in.html')
    return render_template('register.html')
@app.route('/assessments')
def assessments():
    query=text('SELECT * FROM assessments;')
    results=connection1.execute(query).fetchall()
    return render_template('assessments.html', results=results)
if __name__=='__main__':
    app.run(debug=True, reloader_type='stat', port=5000)