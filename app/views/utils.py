# -*- coding: utf-8 -*-
from flask import jsonify, current_app
from flask_restless import APIManager

from app.app import db

BASE_PATH = '/v<int:version>'
manager = APIManager(current_app, flask_sqlalchemy_db=db)

# Error messages.
ERROR_NOT_ENOUGH_STOCK = "There is not enough stock to complete the action."
ERROR_PRODUCT_ID_BAD_FORMAT = "Unexpected type for 'product_id'."
ERROR_PRODUCT_NOT_FOUND = "Product not found."
ERROR_USER_ID_BAD_FORMAT = "Unexpected type for 'user_id'."
ERROR_USER_LIST_DELETE_WRONG_STATE = "It is not possible to cancel a product which is not in the wish list."
ERROR_USER_LIST_NOT_FOUND = "The provided user list record does not exist."
ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS = "The gift you are trying to add to the user list, already exists."
ERROR_USER_NOT_FOUND = "User not found."


# Util methods.
def get_successful_response(message="Successful.", resource_id=None, extras=None):
    """
    Helper method to define a consistent response for all successful requests.
    :param message: (str) Message to be returned.
    :param resource_id: (object) Identifier of the created/edited record.
    :param extras: (dict) Additional fields to be added into the response.
    :return: (json) Jsonify response.
    """
    # Default body response.
    res = {"message": message}

    # If it is expected to return the ID of the created/updated resource, add it to the final response.
    if resource_id:
        res["resource_id"] = resource_id

    # Add any additional output for the response.
    if extras:
        res.update(extras)

    return jsonify(res)
