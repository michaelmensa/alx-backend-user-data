#!/usr/bin/env python3
'''
Module auth.py: to manage API authentication
'''
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    '''
    class to manage API authentication
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' public method that checks which path requires auth '''
        if path is not None and excluded_paths:
            if not path.endswith('/'):
                path += '/'
            for excluded_path in excluded_paths:
                if excluded_path.endswith('*') \
                        and path.startswith(excluded_path[:-1]):
                    return False
                elif path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' returns None, request will be the flask request object '''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        ''' returns None, request will be the flask request object '''
        return None

    def session_cookie(self, request=None):
        ''' method that returns a cookie value from a request
        return None if request is None
        return the value of the cookie named _my_session_id from request
        cookie name must be defined by the env var SESSION_NAME
        use .get() method for dict
        '''
        if request:
            cookie = getenv('SESSION_NAME')
            return request.cookies.get(cookie)
