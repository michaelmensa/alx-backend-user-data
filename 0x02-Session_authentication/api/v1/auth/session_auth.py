#!/usr/bin/env python3
'''
Module session_auth.py: Session Authentication
'''
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    ''' class that implements session authentication.
    inherits from Auth class '''
    # cls attr initialized by an empty dict
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' method that creates a Session ID for a user_id
        return None if user_id is None
        return None if user_id is not a str

        generate Session ID using uuid.uuid4()
        user_id_by_session = {SessionID: user_id}
        return Session ID
        '''
        if type(user_id) != str:
            return None
        if user_id:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id

            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' method that returns a User ID based on a session ID
        return None if session_id is None
        return None if session_id is not str
        must use .get() dict method
        '''
        if type(session_id) != str:
            return None
        if session_id:
            for key in self.user_id_by_session_id.keys():
                if key == session_id:
                    user_id = self.user_id_by_session_id.get(session_id)
                    return user_id

    def current_user(self, request=None):
        ''' method that (overload) returns a User instance based
        based on a cookie value:
        must use self.session_cookie(...) and self.user_id_for_session_id(...)
        to return the User ID based on the cookie _my_session_id
        you will be able to retrieve a User instance from the db- You can
        use User.get(...) for retrieving a User from the db
        '''
        if request:
            try:
                # get the cookie from the request
                cookie = self.session_cookie(request)
                # get user_id from the cookie value
                user_id = self.user_id_for_session_id(cookie)
                # get user using User.get
                return User.get(user_id)
            except Exception:
                return None

    def destroy_session(self, request=None):
        ''' method that deletes the user session / logout:
        if request is equal to None, return False
        if request doesn't contain Session ID cookie, return False
        if Session ID of the request is not linked to any User ID, return
        False
        Otherwise delete in self.user_id_by_session_id (as key of this dict)
        and return True
        '''
        if request:
            cookie = self.session_cookie(request)
            if cookie is None:
                return False
            user_id = self.user_id_for_session_id(cookie)
            if user_id is None:
                return False
            if cookie in self.user_id_by_session_id.keys():
                self.user_id_by_session_id.pop(cookie)
                return True
        return False
