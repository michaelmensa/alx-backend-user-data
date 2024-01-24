#!/usr/bin/env python3
'''
Module app.py - Basic Flask app
'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    ''' function that returns a JSON payload form '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    ''' function that registers a user '''
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'}), 200
    except Exception:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    ''' function that logs in a user
    user must be an existing user '''
    email = request.form['email']
    password = request.form['password']
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' function that logs out a user. user must be an existing user '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    ''' function that implements the respond to the GET /profile '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or not user:
        abort(403)
    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    ''' function that respond to /reset_password route '''
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify({'email': email, 'reset_token': reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    ''' function that resets password '''
    try:
        email = request.form['email']
        new_password = request.form['new_password']
        reset_token = request.form['reset_token']
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except Exception:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
