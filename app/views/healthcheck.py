# -*- coding: utf-8 -*-
from flask import jsonify, current_app


@current_app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """
    Health check endpoint.
    :return: The endpoint will return a status code and a successful message.
    Example:
        {
            "message": "Welcome to The Wedding Shop API!"
        }
    """
    # Set default values.
    status_code = 200
    response = {
        "message": "Welcome to The Wedding Shop API!"
    }
    return jsonify(response), status_code
