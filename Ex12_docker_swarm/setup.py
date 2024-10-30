from app import app
from models import db


def setup_database():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
