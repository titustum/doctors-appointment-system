from werkzeug.security import generate_password_hash
from app import app, db
from models.models import User  # Assuming your User model is imported here

def seed_users():
    # List of dummy users
    users = [
        {"name": "General Admin", "email": "admin@email.com", "password": "password123"},
        {"name": "Jane Smith", "email": "janesmith@email.com", "password": "password123"},
        {"name": "Robert Brown", "email": "robertb@email.com", "password": "password123"},
        {"name": "Alice Green", "email": "alicegreen@email.com", "password": "password123"},
        {"name": "Charlie Blue", "email": "charlieblue@email.com", "password": "password123"},
    ]

    for user_data in users:
        # Hash the password before storing it
        hashed_password = generate_password_hash(user_data["password"])
        user = User(name=user_data["name"], email=user_data["email"], password_hash=hashed_password)

        # Add user to the session and commit to the database
        db.session.add(user)

    # Commit the transaction
    db.session.commit()

    print("Users have been seeded successfully!")

# Run the seeder
if __name__ == "__main__":
    with app.app_context():
        seed_users()
