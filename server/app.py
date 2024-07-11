#!/usr/bin/env python3

# Standard library imports

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Remote library imports
from flask import request, jsonify, session, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api, bcrypt
# Add your model imports
from models import User, Ship,Port

# Views go here!
@app.route('/ships', methods=['GET'])
def get_ships():
    ships = Ship.query.all()
    ships_data = [ship.to_dict() for ship in ships]
    return make_response(ships_data, 200)

@app.route('/ports', methods=['GET'])
def get_ports():
    ports = Port.query.all()
    port_data = [port.to_dict() for port in ports]
    return make_response(port_data, 200)

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')
    balance = data.get('balance')
  
    if not name or not email or not password or not balance:
        return jsonify({"error": "All fields are required"}), 422
    
    new_user = User(
        name=name,
        email=email,
        _password_hash=password,
        balance=balance,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    return jsonify({'success': True, 'message': 'Login successful'})


@app.route('/checksession', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return make_response(user.to_dict(), 200)
    else:
        return {"error": "Unauthorised."}, 401   

if __name__ == '__main__':
    app.run(port=5555, debug=True)

