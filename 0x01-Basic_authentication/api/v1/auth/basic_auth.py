#!/usr/bin/env python3
'''
Module api/v1/auth/basic_auth.py: basic authentication
'''
from api.v1.auth.auth import Auth


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
