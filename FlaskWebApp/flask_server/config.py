# -*- coding: utf-8 -*-

"""
tsbackend.config
~~~~~~~~~~~~~~~~

Here is the initialization config for the Taint Saviour Backend deployment.
Deployment specific configurations (and sensitive settings) can be found in
`/instance` folder.

"""
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
    DOWNLOAD_RESULT_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/results/'

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
