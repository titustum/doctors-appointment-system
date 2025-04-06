from datetime import datetime
from app import db

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

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Scheduled")  # Status could be 'Scheduled', 'Completed', 'Cancelled'
    
    # Foreign keys
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    # Guest details (no specific User model)
    guest_name = db.Column(db.String(100), nullable=False)  # Full Name of guest (patient)
    guest_email = db.Column(db.String(100), nullable=False)  # Email Address of guest
    guest_phone = db.Column(db.String(15), nullable=False)  # Phone Number of guest
    guest_dob = db.Column(db.Date, nullable=False)  # Date of Birth (mm/dd/yyyy)
    
    # Appointment details (department, doctor, visit type)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)  # Foreign key to department
    doctor_name = db.Column(db.String(100), nullable=False)  # Doctor name selected
    preferred_date = db.Column(db.Date, nullable=False)  # Preferred appointment date (mm/dd/yyyy)
    preferred_time = db.Column(db.String(50), nullable=False)  # Preferred appointment time (Morning, Afternoon, Evening)

    # Reason for visit
    visit_type = db.Column(db.String(50), nullable=False)  # Type of visit (New, Follow-up, etc.)
    issue_description = db.Column(db.Text, nullable=True)  # Brief description of the issue (optional)

    # Insurance information (optional)
    insurance_provider = db.Column(db.String(100), nullable=True)  # Insurance provider
    policy_number = db.Column(db.String(100), nullable=True)  # Policy number

    def __repr__(self):
        return f'<Appointment {self.id} with Dr. {self.doctor_name} on {self.preferred_date} at {self.preferred_time}>'
