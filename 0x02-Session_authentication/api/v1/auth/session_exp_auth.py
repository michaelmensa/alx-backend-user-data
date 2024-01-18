#!/usr/bin/env python3
'''
Module session_exp_auth.py: Session authentication with an expiry
'''
from models.user import User
from flask import request
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    ''' class that implements session authenticaton with an expiry '''
    def __init__(self):
        ''' constructor method '''
        super().__init__()
        # assign an instance attribute session_duration to an ENV VARIABLE
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        ''' method that creates session with user_id '''
        # create session ID by calling super()
        session_id = super().create_session(user_id)
        if session_id:
            # store the session dictionary in user_id_by_session_id
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            # return created session ID
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        ''' method that gets user id from session id '''
        # return None is session ID is None
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0 or 'created_at' not in session_dict:
            return None
        timespan = timedelta(seconds=self.session_duration)
        exp = session_dictionary['created_at'] + timespan
        if exp < datetime.now():
            return None
        return session_dict['user_id']
