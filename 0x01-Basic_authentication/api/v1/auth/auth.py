#!/usr/bin/env python3
'''
Module auth.py: to manage API authentication
'''
from flask import request
from typing import List, TypeVar


class Auth():
    '''
    class to manage API authentication
    '''

    def require_auth(self, path: str, exluded_paths: List[str]) -> bool:
        ''' public method '''
        return False

    def authorization_header(self, request=None) -> str:
        ''' returns None, request will be the flask request object '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' returns None, request will be the flask request object '''
        return None
