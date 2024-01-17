#!/usr/bin/env python3
'''
Module session_auth.py: Session Authentication
'''
from api.v1.auth.auth import Auth
import uuid


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
