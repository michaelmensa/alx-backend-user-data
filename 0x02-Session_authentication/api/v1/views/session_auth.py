#!/usr/bin/env python3
'''
Module session_auth.py: New view for Session Authentication
'''
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, make_response, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    ''' function that routes to login page '''
    # retrieve email and password parameters
    email = request.form.get('email')
    passwd = request.form.get('password')

    # returning error messages in json when email and passwd is missing
    if email == "" or email is None:
        return jsonify({'error': 'email missing'}), 400
    if passwd == "" or passwd is None:
        return jsonify({'error': 'password missing'}), 400

    # retrieve User instance based on the email.
    try:
        users = User.search({'email': email})
        if not users or users == []:
            return jsonify({'error': 'no user found for this email'}), 404
        for user in users:
            if user.is_valid_password(passwd):
                user_id = user.id
                # create a session ID for the user ID
                from api.v1.app import auth
                session_id = auth.create_session(user_id)
                # creating a JSON response
                response = jsonify(user.to_json())
                # setting the session ID as a cookie
                resp = make_response(response)
                resp.set_cookie('_my_session_id', value=session_id)
                return resp
        return jsonify({'error': 'wrong password'}), 401
    except Exception:
        return None


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session():
    ''' function that deletes session / logout '''
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    return jsonify({}), 200
