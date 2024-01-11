#!/usr/bin/env python3
'''
Module encrypt_password
'''
import bcrypt


def hash_password(password: str):
    ''' function that expects one string arg and
    returns a salted, hashed password
    '''
    password = b'{password}'
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
