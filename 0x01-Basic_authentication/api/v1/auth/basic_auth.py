#!/usr/bin/env python3
'''
Module api/v1/auth/basic_auth.py: basic authentication
'''
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


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
            decoded = decoded_base64_authorization_header.split(':')
            user_email, password = decoded[0], decoded[-1]
            return user_email, password
        else:
            return None, None
