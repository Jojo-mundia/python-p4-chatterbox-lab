#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # Allow React frontend

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Chatterbox API</h1>'

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([msg.to_dict() for msg in messages]), 200)

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')

    if not body or not username:
        return make_response({"error": "body and username are required"}, 400)

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()
    return make_response(jsonify(new_message.to_dict()), 201)

# PATCH a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    body = data.get('body')

    if not body:
        return make_response({"error": "body is required to update"}, 400)

    message.body = body
    message.updated_at = datetime.utcnow()
    db.session.commit()
    return make_response(jsonify(message.to_dict()), 200)

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return make_response({"message": f"Message {id} deleted successfully"}, 200)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
