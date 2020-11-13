# -*- coding: utf-8 -*-

"""
tsbackend.app
~~~~~~~~~~~~~

Initializes the Flask application.

In the first step the module obtains the correct configuration from the
instance folder (a means for supplying possibly sensitive deployment specific
information without committing it to source control).

Then the database connection is set up and finally each routes blueprint is
imported and loaded. It's important that this step occurs entirely within the
`app.app_context()` context manager so that those modules have access to the
`flask.current_app` object.

"""
from flask import Flask
from flask_cors import CORS

from flask_server import config, database


def create_app():
    app = Flask(__name__, instance_relative_config=True,
                          static_folder='../react_application/build/static', 
                          template_folder="../react_application/build")
    CORS(app, supports_credentials=True)

    # Import configuration settings
    app.config.from_object(config.TestingConfig)
    app.config.from_pyfile('config.py')

    with app.app_context():
        # Set up database connection pool
        app.db = database.connect_to_analysis_db()

        # Import blueprints containing routes and views
        from flask_server.views.users import users_bp
        from flask_server.views.apks import apks_bp
        from flask_server.views.workers import workers_bp
        from flask_server.views.rendering import rendering_bp
        from flask_server.views.signatures import signatures_bp

        app.register_blueprint(users_bp)
        app.register_blueprint(apks_bp)
        app.register_blueprint(workers_bp)
        app.register_blueprint(rendering_bp)
        app.register_blueprint(signatures_bp)

    return app
