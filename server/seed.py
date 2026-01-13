from app import app, db
from models import Message

with app.app_context():
    db.drop_all()   # Optional: clean slate
    db.create_all() # Ensure tables exist

    # Add a sample message
    msg = Message(body="Hello ", username="Ian")
    db.session.add(msg)
    db.session.commit()
    print("Database seeded with 1 message")
