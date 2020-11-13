# -*- coding: utf-8 -*-

"""
tsbackend.utils
~~~~~~~~~~~~~~~

This module provides utility functions used throughout the backend library.

"""
import threading
import time

from flask import jsonify


class ConstantTime:
    """A context manager for ensuring constant time branching."""

    def __init__(self, length):
        self.length = length

    def __enter__(self):
        self.timer = threading.Thread(target=time.sleep, args=[self.length])
        self.timer.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.timer.join()


def error(msg=''):
    """Helper for returning an error response.

    Args:
        msg (str): The message to return in the response.

    Returns:
        str: A stringified response to failure.
    """
    return jsonify({'success': False, 'message': msg})
