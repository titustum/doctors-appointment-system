from app import create_app, db
from models.models import Doctor, Appointment, Department
from datetime import datetime, timedelta
import random
import faker  # Using the Faker library to generate fake data

app = create_app()

# Create a function to seed data
def seed_data():
    # Clear existing data (optional)
    db.drop_all()
    db.create_all()

    # Add Departments (representing the doctor's specialty)
    departments = [
        Department(name='General Medicine'),
        Department(name='Cardiology'),
        Department(name='Neurology'),
        Department(name='Pediatrics'),
        Department(name='Dermatology'),
        Department(name='Oncology')
    ]
    
    db.session.add_all(departments)
    db.session.commit()

    # Add Doctors (linking them to departments)
    doctors = [
        Doctor(name='Dr. Sarah Johnson', department_id=2, image_url='photo-1559839734-2b71ea197ec2.avif', rating="4.5", work_hours="9 AM - 5 PM"),
        Doctor(name='Dr. Michael Chen', department_id=3, image_url='photo-1594824476967-48c8b964273f.avif', rating="4.7", work_hours="10 AM - 6 PM"),
        Doctor(name='Dr. Lisa Rodriguez', department_id=4, image_url='photo-1612349317150-e413f6a5b16d.avif', rating="4.6", work_hours="8 AM - 4 PM"),
        Doctor(name='Dr. Robert Williams', department_id=5, image_url='photo-1622253692010-333f2da6031d.avif', rating="4.8", work_hours="9 AM - 5 PM")
    ]
    
    db.session.add_all(doctors)
    db.session.commit()

    # Create a Faker instance to generate random guest data
    fake = faker.Faker()

    # Add Appointments (linking doctors and guests)
    appointment_times = [
        datetime(2025, 4, 1, 9, 0), datetime(2025, 4, 1, 10, 0), datetime(2025, 4, 1, 14, 30),
        datetime(2025, 4, 2, 8, 30), datetime(2025, 4, 2, 11, 0), datetime(2025, 4, 2, 13, 0),
        datetime(2025, 4, 3, 15, 0), datetime(2025, 4, 4, 9, 15), datetime(2025, 4, 5, 10, 45)
    ]

    visit_types = ['New Patient Consultation', 'Follow-up Visit', 'Routine Check-up', 'Urgent Care']

    # Generate some fake appointments for demonstration
    appointments = []
    for i in range(10):  # Create 10 appointments
        doctor = random.choice(doctors)
        department = db.session.get(Department, doctor.department_id)
        appointment_time = random.choice(appointment_times)
        status = random.choice(['Scheduled', 'Completed', 'Cancelled'])
        visit_type = random.choice(visit_types)

        # Create fake guest data
        guest_name = fake.name()
        guest_email = fake.email()
        guest_phone = fake.phone_number()
        guest_dob = fake.date_of_birth(minimum_age=18, maximum_age=75)
        preferred_date = fake.date_this_month()
        preferred_time = fake.time()

        # Create an appointment for a guest
        appointment = Appointment(
            appointment_time=appointment_time,
            status=status,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            guest_dob=guest_dob,
            department_id=department.id,
            doctor_id=doctor.id,
            doctor_name=doctor.name,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            visit_type=visit_type,
            issue_description=fake.text(max_nb_chars=200),
            insurance_provider=fake.company(),
            policy_number=fake.uuid4()
        )
        appointments.append(appointment)

    db.session.add_all(appointments)
    db.session.commit()

    print("Data seeded successfully.")

# Run the seeder
if __name__ == '__main__':
    with app.app_context():
        seed_data()
