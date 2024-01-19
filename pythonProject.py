from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)

# Configure SQLAlchemy to use your SQL Server database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DIPAK\\SQLEXPRESS/PYTHONPROJECT?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(255))

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Register student route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_student = Student(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            date_of_birth=request.form['date_of_birth'],
            gender=request.form['gender'],
            contact_number=request.form['contact_number'],
            email=request.form['email']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
