# -*- coding: utf-8 -*-
import time

from flask import Flask, g, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='./templates')
    app.config.from_pyfile('./config.py')

    db.init_app(app)
    Migrate(app, db)

    def before_request():
        """
        This method will be executed before each request.
        It will authenticate the user (unless the path is in a list of unrestricted URLs).
        It will also initialise the start time which will be used for monitoring
        the execution time of the request.
        """
        g.start = time.time()

        if request.method == 'OPTIONS' or request.path in views.public_urls:
            return

        # Get the version.
        path = request.path.strip('/').split('/')
        g.version = path[0]

    def after_request(response):
        """
        This method will be executed after each request.
        """
        # TODO: Send log reports to a monitor service such as DataDog?
        return response

    with app.app_context():
        # Import APP libraries.
        # from app.auth import authenticate
        from app import views

        # Set before and after requests.
        app.before_request(before_request)
        app.after_request(after_request)

        return app
