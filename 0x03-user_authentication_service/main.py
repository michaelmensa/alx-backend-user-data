#!/usr/bin/env python3
"""
Main file
"""
import requests


BASE_URL = 'http://0.0.0.0:5000'

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    ''' test user registration '''
    url = f'{BASE_URL}/users'
    payload = {'email': email, 'password': password}
    r = requests.post(url, params=payload)
    assert r.json() == {'email': email, 'message': 'user created'}
    r = requests.post(url, params=payload)
    assert r.status_code == 400
    assert r.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    ''' test wrong password '''
    url = f'{BASE_URL}/sessions'
    payload = {'email': email, 'password': password}
    r = requests.post(url, params=payload)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    ''' test correct login '''
    url = f'{BASE_URL}/sessions'
    payload = {'email': email, 'password': password}
    r = requests.post(url, params=payload)
    assert r.status_code == 200
    session_id = r.json().get('session_id')
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    ''' profile from unlogged user '''
    r = requests.get(f'{BASE_URL}/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    ''' checks for logged profile '''
    headers = {'Cookie': f'session_id={session_id}'}
    r = requests.get(f'{BASE_URL}/profile', headers=headers)
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    ''' logs out from profile '''
    headers = {'Cookie': f'session_id={session_id}'}
    r = requests.delete(f'{BASE_URL}/profile', headers=headers)
    assert r.status_code == 200


def reset_password_token(email: str) -> str:
    ''' resets password '''
    payload = {'email': email}
    r = requests.post(f'{BASE_URL}/reset_password')
    assert r.status_code == 200
    reset_token = r.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    ''' updates password '''
    payload = {
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
            }
    r = requests.put(f'{BASE_URL}/reset_password', params=payload)
    assert r.status_code == 200


if __name__ == "__main__":

    # register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
