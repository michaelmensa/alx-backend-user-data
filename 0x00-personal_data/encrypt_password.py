#!/usr/bin/env python3
'''
Module encrypt_password
'''
import bcrypt
from bcrypt import hashpw, checkpw


def hash_password(password: str) -> bytes:
    ''' function that expects one string arg and
    returns a salted, hashed password
    '''
    password = password.encode() 
    hashed = hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' function that validates password '''
    password = password.encode() 
    if checkpw(password, hashed_password):
        return True
    else:
        return False
