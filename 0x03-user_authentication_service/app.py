#!/usr/bin/env python3
'''
Module app.py - Basic Flask app
'''
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    ''' function that returns a JSON payload form '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    ''' function thast registers a user '''
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except Exception:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    ''' function that logs in a user
    user must be an existing user '''
    try:
        email = request.form['email']
        password = request.form['password']
        if not AUTH.valid_login(email, password):
            abort(401, description="Invalid login credentials")
        user_session = AUTH.create_session(email)

        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', user_session)

        return response
    except Exception:
        abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
