from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = "supersecret"
app.permanent_session_lifetime = timedelta(minutes=30)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/censusdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models
from models import HouseholdMember

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    household_id = request.form['household_id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    married = request.form['married']

    new_member = HouseholdMember(
        household_id=household_id,
        name=name,
        age=age,
        gender=gender,
        married=married
    )
    db.session.add(new_member)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    members = HouseholdMember.query.all()
    return render_template('admin.html', members=members)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000)
