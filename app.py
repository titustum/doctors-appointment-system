import os
from random import random
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'  # Use your preferred DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Folder to store images
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}  # Allowed image extensions
db = SQLAlchemy(app)

# Flash messages setup
app.secret_key = 'supersecretkey' # Change this to a more secure key

migrate = Migrate(app, db)


def create_app():
    return app


from models.models import *


# Routes
@app.route('/', methods=['GET'])
def index():
    departments = Department.query.all()
    doctors = Doctor.query.all()
    return render_template('home.html', doctors=doctors, departments=departments)


@app.route('/doctors', methods=['GET'])
def doctors():
    departments = Department.query.all()
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors, departments=departments)

@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    doctor =  Doctor.query.get(doctor_id)
    if not doctor:
        return redirect(url_for('doctors'))
    
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        time = request.form.get('time')
        message = request.form.get('message')

        # Create a new appointment instance
        appointment = Appointment(
            doctor_id=doctor.id,
            patient_name=name,
            patient_email=email,
            patient_phone=phone,
            patient_dob=datetime.strptime(request.form.get('dob'), '%Y-%m-%d'),  # Optional, if included in form
            preferred_date=datetime.strptime(date, '%Y-%m-%d'),
            preferred_time=time,
            issue_description=message,
            status='Scheduled'  # Default status
        )

        # Add the appointment to the database
        try:
            db.session.add(appointment)
            db.session.commit()
            flash("Appointment successfully booked!", 'success')
            return redirect(url_for('appointment_confirmation', appointment_id=appointment.id))  # Redirect to confirmation page
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while booking the appointment: {e}", 'danger')
    doctor.rating = round(random() * 10, 1)
    return render_template('book_appointment.html', doctor=doctor)


@app.route('/appointment-confirmation/<int:appointment_id>')
def appointment_confirmation(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('appointment_confirmation.html', appointment=appointment)




# View doctors that belong to a department
@app.route('/search_doctors', methods=['GET'])
def search_doctors():
    search_term = request.args.get('query', '').strip().lower()
    # Handle empty search terms
    if not search_term:
        doctors = []
    else:
        try:
            doctors = Doctor.query.filter(Doctor.name.ilike(f'%{search_term}%')).all()
        except Exception as e:
            doctors = []
            print(f"Error fetching doctors: {e}")

    return render_template('search_doctors.html', doctors=doctors)

# View doctors that belongs to department
@app.route('/departmental_doctors/<int:department_id>' , methods=['GET'])  
def departmental_doctors(department_id):
    department = Department.query.get(department_id) 
    doctors = Doctor.query.filter_by(department_id=department_id).all() 
    return render_template('categorized_doctors.html', doctors=doctors, department=department)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Extract data from the form
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # You can add logic here to save the form data (e.g., store in database, send an email, etc.)
        
        # Redirect the user after form submission
        return redirect(url_for('thank_you'))
    
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Simple route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Dummy authentication (replace with actual logic)
        if email == "test@domain.com" and password == "password123":
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


# Simple route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # For now, print the data (replace with actual DB logic)
        print(f"Name: {name}, Email: {email}, Password: {password}")
        
        # Dummy registration success (you should hash passwords and store them in the database)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Simple route for a dashboard (protected page after login)
@app.route('/dashboard')
def dashboard():

    departments = Department.query.all()

    # Get total number of appointments
    total_appointments = Appointment.query.count()

    # Get total number of upcoming appointments (status 'Scheduled')
    upcoming_appointments = Appointment.query.filter(Appointment.preferred_time > datetime.now(), Appointment.status == "Scheduled").count()

    # Get total number of doctors
    total_doctors = Doctor.query.count()

    # Get the upcoming appointments (for displaying in the table)
    upcoming_appointments_list = Appointment.query.filter(Appointment.preferred_time > datetime.now(), Appointment.status == "Scheduled").all()

    # Render the dashboard template and pass the data
    return render_template('dashboard.html', 
                           total_appointments=total_appointments,
                           upcoming_appointments=upcoming_appointments,
                           total_doctors=total_doctors,
                           upcoming_appointments_list=upcoming_appointments_list,
                           departments = departments
                           )



# Utility function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Route to handle adding a new doctor
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    # Get data from the request
    name = request.form['name']
    department_id = request.form['department_id']
    rating = request.form['rating']
    work_hours = request.form['work_hours']

    # Handle image upload
    image = request.files['image']  # 'image' is the name attribute of the input field
    if image:
        if allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)  # Save the image to the upload folder
            image_url = filename  # You could store the relative or full URL here
        else:
            return jsonify({"error": "Invalid file type"}), 400
    else:
        return jsonify({"error": "No image provided"}), 400

    # Add the new doctor to the database
    new_doctor = Doctor(
        name=name,
        department_id=department_id,
        image_url=image_url,
        rating=rating,
        work_hours=work_hours
    )

    try:
        db.session.add(new_doctor)
        db.session.commit()
        # Redirect to dashboard after adding doctor
        return redirect(url_for('dashboard'))  # Redirect to dashboard route
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__': 
    app.run(debug=True)
