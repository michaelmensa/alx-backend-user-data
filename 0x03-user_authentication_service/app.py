#!/usr/bin/env python3
'''
Module app.py - Basic Flask app
'''
from flask import Flask, jsonify, request, abort, redirect, url_for
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' function that logs out a user. user must be an existing user '''
    try:
        session_id = request.form['session_id']
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            user_id = user.id
            AUTH.destroy_session(user_id)
            return redirect('/')
        else:
            abort(403)
    except Exception:
        abort(403)


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
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
