#!/usr/bin/env python3
'''
Module auth.py: user authentication
'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    ''' method that takes a password string arg
    and return bytes '''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    ''' function that generates a string repr of a new UUID '''
    return str(uuid.uuid4())


class Auth():
    ''' Auth class to interact with the authentication database
    '''
    def __init__(self):
        ''' constructor method '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' method that takes email, and password and returns
        a User Object '''
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass
        password = _hash_password(password).decode('utf-8')
        new_user = self._db.add_user(email, password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        ''' method that checks valid logins '''
        try:
            existing_user = self._db.find_user_by(email=email)
            h_password = existing_user.hashed_password.encode()
            password = password.encode()

            if bcrypt.checkpw(password, h_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        ''' method that creates session and returns session ID
        from email '''
        # find user and create session for him
        try:
            existing_user = self._db.find_user_by(email=email)
            generated_id = _generate_uuid()
            existing_user.session_id = generated_id
            return existing_user.session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str):
        ''' method that returns either User or None from session id '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            else:
                return None
        except NoResultFound:
            pass

    def destroy_session(self, user_id: int) -> None:
        ''' method that takes user_id as arg and deletes user object
        returns None
        '''
        try:
            user = self._db.find_user_by(id=user_id)
            if user.session_id is not None:
                user.session_id = None
            return None
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        ''' method that gets reset password token '''
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=user.reset_token)
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        ''' method that updates password
        use reset_token to find user. raise ValueError is user not exist
        Otherwise, hash password and update user password and reset_token
        field to None'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
