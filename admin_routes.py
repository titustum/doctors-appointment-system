from functools import wraps
from flask import render_template, redirect, flash, url_for, request, session
from app import app, db
from models import Doctor 

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    doctors = Doctor.query.all()
    bookings = []  # Replace with actual booking data
    return render_template('dashboard.html', doctors=doctors, bookings=bookings)

@app.route('/admin/delete_doctor/<int:id>', methods=['POST'])
def admin_delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_doctor', methods=['POST'])
def admin_add_doctor():
    name = request.form['name']
    specialty = request.form['specialty']
    image_url = request.form['image_url']
    new_doctor = Doctor(name=name, specialty=specialty, image_url=image_url)
    db.session.add(new_doctor)
    db.session.commit()
    flash('Doctor added successfully!', 'success')
