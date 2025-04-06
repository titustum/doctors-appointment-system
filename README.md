# MediConnect - Doctor Appointment Booking System

MediConnect is a web-based system designed to help patients book appointments with doctors seamlessly. Patients can search for doctors based on departments, view their profiles, check availability, and book appointments with ease.

This README will guide you through setting up the MediConnect system locally, as well as provide an overview of the core features.

---

## Features

- **Doctor Search**: Patients can search for doctors by department and view detailed profiles, including their ratings, availability, and specializations.
- **Appointment Booking**: Patients can book appointments with doctors, specifying their preferred date, time, and providing a brief description of the issue.
- **Appointment Management**: Admins can view and manage appointments, including printing and filtering by doctor.
- **User Authentication**: Support for user registration and login for both patients and admins.

---

## Tech Stack

- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLite (or other databases like PostgreSQL or MySQL for production)
- **Authentication**: Flask-Login for session management
- **ORM**: SQLAlchemy
- **Other Libraries**: Flask-WTF, Flask-Mail (for email notifications), Werkzeug (for password hashing)

---

## Installation

### Prerequisites

Before running the project locally, ensure you have the following installed:

- Python 3.x
- Git
- pip (Python package installer)

### Steps to Set Up

1. **Clone the Repository**

   First, clone the project repository to your local machine:

   ```bash
   git clone https://github.com/titustum/doctors-appointment-system.git 
   cd doctors-appointment-system
   ```

2. **Create and Activate a Virtual Environment**

   It is recommended to create a virtual environment to manage dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**

   Initialize the SQLite database and create the required tables:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the Application**

   After setting up the database, you can run the Flask development server:

   ```bash
   flask run
   ```

   This will start the web server at `http://127.0.0.1:5000/`.

---

## Usage

### Register and Log In

- **Register as a new user**: Navigate to the `/register` page to create a new account.
- **Log in**: Once registered, you can log in using the `/login` page.
- **Admin Access**: Admins can manage the appointments via the `/admin` route.

### Booking an Appointment

1. **View Doctors**: Navigate to the `/doctors` page to view available doctors.
2. **Select a Doctor**: Click on a doctor’s profile to see their availability and book an appointment.
3. **Book Appointment**: Select your preferred date, time, and provide a brief description of your issue.
4. **Confirm Appointment**: After filling out the form, click **Confirm Appointment** to finalize the booking.

### Admin Panel

- Admins can view and manage all appointments via the `/admin/appointments` page.
- Appointments can be filtered by doctor, and admins can also print appointment details.

---

## Contribution Guidelines

We welcome contributions to the MediConnect project! To contribute:

1. Fork the repository on GitHub.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add feature'`).
4. Push your branch to your fork (`git push origin feature-name`).
5. Submit a pull request with a description of the changes.

Please ensure that your code follows the style guide and passes all tests before submitting a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: ORM for Python for interacting with databases.
- **Flask-WTF**: Forms and validation for Flask applications.
- **Tailwind CSS**: A utility-first CSS framework used for styling the UI.

---

## Contact

If you have any questions or feedback, feel free to open an issue on the GitHub repository or contact the maintainers via email.