from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pyodbc

app = Flask(__name__)

# Configure SQLAlchemy and Flask-Login
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DIPAK\\SQLEXPRESS/PYTHONPROJECT?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a secret key for Flask
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Define a Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(255))

# Define an Admin model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

# Create the database tables
db.create_all()

# Home route
@app.route('/')
@login_required
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Register student route
@app.route('/register', methods=['GET', 'POST'])
@login_required
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
        flash('Student registered successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form['username']).first()
        if admin and admin.password == request.form['password']:
            login_user(admin)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin_login.html')

# Admin logout route
@app.route('/admin_logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)