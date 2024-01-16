#!/usr/bin/env python3
'''
Module api/v1/auth/basic_auth.py: basic authentication
'''
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    ''' class BasicAuth that inherits from Auth.
    class handles basic authentication
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''
        returns the base64 part of the authorization header for
        a basic authentication '''
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header.startswith('Basic '):
            base64_cred = authorization_header.split(' ')[-1]
            return base64_cred
        else:
            return None

    def decode_base64_authorization_header(self,
                                           authorization_header: str) -> str:
        '''
        returns the decoded base64 part of the authorization header for
        a basic authentication '''
        if authorization_header is None or type(authorization_header) != str:
            return None

        try:
            decoded = base64.b64decode(authorization_header)
            return decoded.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        ''' return the user email and password from the
        base64 decoded value '''
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' in decoded_base64_authorization_header:
            decoded = decoded_base64_authorization_header.split(':', 1)
            user_email, password = decoded[0], decoded[-1]
            return user_email, password
        else:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        ''' returns the User instance based on his email and password '''
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' method that overloads Auth and retrieves the User instance
        for a request
        '''
        try:
            # call the authorization_header from Auth
            authorized_header = super().authorization_header(request)
            # extract the header
            h = self.extract_base64_authorization_header(authorized_header)
            # decode the header
            decoded = self.decode_base64_authorization_header(h)
            # extract user credentials. it will return a tuple
            user_cred = self.extract_user_credentials(decoded)
            user_email, user_pwd = user_cred[0], user_cred[-1]
            # get user from user_cred
            user = self.user_object_from_credentials(user_email, user_pwd)
            return user
        except Exception:
            return None
