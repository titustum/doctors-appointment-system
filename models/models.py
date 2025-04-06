from datetime import datetime, timezone
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Department Model (Doctors Specialties)
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(100), nullable=True)  # Optional image URL for department

    # Relationship with Doctor model
    doctors = db.relationship('Doctor', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name}>'

# Doctor Model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)  # Foreign key to Department
    image_url = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.String(300), nullable=False)  # Doctor's rating
    work_hours = db.Column(db.String(300), nullable=False)  # Working hours of the doctor

    # Relationship with Appointment model
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.name}, Department {self.department.name}, Rating: {self.rating}>'
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Appointment Model 
class Appointment(db.Model): 
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Status of Appointment
    status = db.Column(db.String(50), nullable=False, default="Scheduled")  # Options: 'Scheduled', 'Completed', 'Cancelled'
    # Foreign Keys
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # Patient Details
    patient_name = db.Column(db.String(100), nullable=False)  # Full Name
    patient_email = db.Column(db.String(100), nullable=False)  # Email Address
    patient_phone = db.Column(db.String(15), nullable=False)  # Phone Number
    patient_dob = db.Column(db.Date, nullable=False)  # Date of Birth (mm/dd/yyyy)
    # Appointment Details
    preferred_date = db.Column(db.Date, nullable=False)  # Preferred Appointment Date
    preferred_time = db.Column(db.String(50), nullable=False)  # Preferred Time (Morning, Afternoon, Evening)
    visit_type = db.Column(db.String(50), nullable=False)  # Type of Visit (New, Follow-up, etc.)
    issue_description = db.Column(db.Text, nullable=True)  # Brief Description of the Issue (Optional)
    # Insurance Information (Optional)
    insurance_provider = db.Column(db.String(100), nullable=True)  # Insurance Provider
    policy_number = db.Column(db.String(100), nullable=True)  # Policy Number
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Record Creation Time
    # Representation
    def __repr__(self):
        return f'<Appointment {self.id} with Doctor ID {self.doctor_id} on {self.preferred_date} at {self.preferred_time}>'
    






