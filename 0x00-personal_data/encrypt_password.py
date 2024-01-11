#!/usr/bin/env python3
'''
Module encrypt_password
'''
import bcrypt
from bcrypt import hashpw


def hash_password(password: str):
    ''' function that expects one string arg and
    returns a salted, hashed password
    '''
    password = password.encode() 
    hashed = hashpw(password, bcrypt.gensalt())
    return hashed
