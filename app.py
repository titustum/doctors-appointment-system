import os
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
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/services')
def services():
    return render_template('services.html')


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
    upcoming_appointments = Appointment.query.filter(Appointment.appointment_time > datetime.now(), Appointment.status == "Scheduled").count()

    # Get total number of doctors
    total_doctors = Doctor.query.count()

    # Get the upcoming appointments (for displaying in the table)
    upcoming_appointments_list = Appointment.query.filter(Appointment.appointment_time > datetime.now(), Appointment.status == "Scheduled").all()

    # Render the dashboard template and pass the data
    return render_template('dashboard.html', 
                           total_appointments=total_appointments,
                           upcoming_appointments=upcoming_appointments,
                           total_doctors=total_doctors,
                           upcoming_appointments_list=upcoming_appointments_list,
                           departments = departments
                           )



# Route for displaying the form and handling POST requests
@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # Get form data from the POST request
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        department = request.form['department']
        doctor_id = request.form['doctor_id']
        appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d')
        appointment_time = request.form['appointment_time']
        visit_type = request.form['visit_type']
        message = request.form.get('message', '')  # Optional field
        insurance_provider = request.form.get('insurance', '')  # Optional field
        policy_number = request.form.get('policy', '')  # Optional field

        # Create a new appointment object
        new_appointment = Appointment(
            guest_name=name,
            guest_email=email,
            guest_phone=phone,
            guest_dob=dob,
            department_id=department,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            visit_type=visit_type,
            message=message,
            insurance_provider=insurance_provider,
            policy_number=policy_number
        ) 

        # Add the new appointment to the database
        db.session.add(new_appointment)
        db.session.commit()

        # Redirect to confirmation page
        return redirect(url_for('confirmation'))

    # Render the form on GET request
    departments = Department.query.all()
    doctors = Doctor.query.all()
    return render_template('book_appointment.html', doctors=doctors,departments=departments) 



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
