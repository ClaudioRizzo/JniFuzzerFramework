# -*- coding: utf-8 -*-

"""
tsbackend.models.users
~~~~~~~~~~~~~~~~~~~~~~

This module contains helper functions for performing user management tasks on
the database to support the routes defined in `tsbackend.views.users`.

"""
from functools import wraps
from typing import Union

from flask import current_app, session, redirect
from passlib.hash import sha256_crypt

from flask_server.utils import ConstantTime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


def authenticate_user(username, password) -> bool:
    """Authenticate a user given some credentials.

    Args:
        username (str): The username to look up.
        password (str): The password to verify with.

    Returns:
        bool: Whether or not the user has successfully authenticated.
    """
    # Find user with the same username
    user = find_user(username)

    # Protect against user enumeration timing attacks
    with ConstantTime(0.5):
        if user is None:
            return False

        return sha256_crypt.verify(password, user['password'])


def find_user(username) -> Union[dict, None]:
    """Find a user in the database.

    Args:
        username (str): The username to lookup.

    Returns:
        Union[dict, None]: The user document if it exists, otherwise None.
    """
    return current_app.db.users.find_one({'username': username})


def add_user(username, password) -> bool:
    """Add a user to the database.

    Args:
        username (str): The username to add.
        password (str): The password of the user to add.

    Returns:
        bool: Whether or not the user was successfully created.
    """
    # Check if user already present
    if find_user(username):
        return False
    # Add new user with hashed password
    hashed_pwd = sha256_crypt.hash(password)
    current_app.db.users.insert_one({'username': username,
                                     'password': hashed_pwd})
    return True


def is_logged_in(f):
    """Function wrapper for checking if the user is authorised.

    Args:
        f (function): The function to wrap.

    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        # Be aware that we expect the token to be the first args (args[0])
        # If it is something else, token auth won't work
        token = "" if 'token' not in kwargs else kwargs['token']
        token_usrid = verify_auth_token(token)
        
        if 'logged' in session:
            return f(*args, **kwargs)
        elif token_usrid:
            return f(*args, **kwargs)
        else:
            return redirect('/login', code=302)

    return wrapped


def get_current_userid(token=""):
    '''Returns the currentl logged user. If no user is in the sessions
    an empty string is returned'''
    token_usrid = verify_auth_token(token)
    if 'username' in session:
        return session['username']
    elif token_usrid:
        return token_usrid
    else:
        return ''

def generate_auth_token(expiration=600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': get_current_userid()})


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        if token == "" or token is None:
            return None
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    
    return data['id'] 