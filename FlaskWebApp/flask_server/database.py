# -*- coding: utf-8 -*-

"""
tsbackend.database
~~~~~~~~~~~~~~~~~~

This module wraps Mongo interactions with the backend database of the analysis
subsystem.

"""
from flask import current_app
from pymongo import MongoClient

import os

PRODUCTION = os.environ.get('PRODUCTION')


def connect_to_analysis_db():

    if PRODUCTION:
        return MongoClient(
            username=current_app.config['ANALYSIS_DB']['user'],
            password=current_app.config['ANALYSIS_DB']['pwd'],
            authSource=current_app.config['ANALYSIS_DB']['authdb'],
            host=current_app.config['ANALYSIS_DB']['host'],
            port=current_app.config['ANALYSIS_DB']['port'],
            ssl=True,
            ssl_ca_certs='/etc/ssl/mongodb.pem')[current_app.config['ANALYSIS_DB']['db']]
    else:
        return MongoClient(
            host=current_app.config['ANALYSIS_DB']['host'],
            port=current_app.config['ANALYSIS_DB']['port'])[current_app.config['ANALYSIS_DB']['db']]
