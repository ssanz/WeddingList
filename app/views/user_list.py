# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.exc import DataError
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, NotImplemented

from flask import current_app, request
from sqlalchemy import and_

from app.app import db
from app.models.user import User
from app.models.product import Product
from app.models.user_list import UserList
from app.views.utils import BASE_PATH, ERROR_NOT_ENOUGH_STOCK, ERROR_PRODUCT_ID_BAD_FORMAT, ERROR_PRODUCT_NOT_FOUND,\
    ERROR_USER_ID_BAD_FORMAT, ERROR_USER_LIST_ACTION_WRONG_STATE, ERROR_USER_LIST_NOT_FOUND,\
    ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS, ERROR_USER_NOT_FOUND, get_successful_response, manager

COLLECTION_NAME = "user_list"

user_list_blueprint = manager.create_api_blueprint(
    UserList,
    methods=['GET'],
    url_prefix=BASE_PATH,
    collection_name=COLLECTION_NAME,
    exclude_columns=['product_id', 'user_id', 'user.password'],
    primary_key='id'
)


def _add_gift_to_list(user_id, product_id):
    """
    Common method to add a gift (product) to the list of the user.
    :param user_id: (str) User identifier.
    :param product_id: (int) Product identifier.
    :return: (int) User list identifier.
    :raises:
        - BadRequest -> If the product type format is not valid.
        - NotFound -> If any of the resources (User or Product) does not exists.
        - Forbidden -> If there is not enough stock or the record already exists.
    """
    # # Check IDs format.
    try:
        user = db.session.query(User).get(user_id)
    except DataError:
        raise BadRequest(ERROR_USER_ID_BAD_FORMAT)

    try:
        product_id = int(product_id)
        product = db.session.query(Product).get(product_id)
    except (ValueError, TypeError):
        raise BadRequest(ERROR_PRODUCT_ID_BAD_FORMAT)

    # # Check that product exists.
    if not user:
        raise NotFound(ERROR_USER_NOT_FOUND)

    if not product:
        raise NotFound(ERROR_PRODUCT_NOT_FOUND)

    # # Check that there is enough stock.
    if product.in_stock_quantity <= 0:
        raise Forbidden(ERROR_NOT_ENOUGH_STOCK)

    # # Check that the product does not exists for the user.
    ul = UserList.query.filter(and_(UserList.user_id == user_id,
                                    UserList.product_id == product_id,
                                    UserList.state.in_(["wish", "purchased"]))).scalar()
    if ul:
        raise Forbidden(ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS)

    # Create the object.
    now = datetime.utcnow()
    user_list_data = {
        "user_id": user_id,
        "product_id": product_id,
        "state": "wish",
        "create_date": now,
        "write_date": now,
    }
    user_list = UserList(**user_list_data)
    product.in_stock_quantity = product.in_stock_quantity - 1
    db.session.add(user_list)
    db.session.commit()
    db.session.add(product)
    db.session.commit()

    return user_list


def _update_gift_from_list(user_list_id, action):
    """
    Common method to update an existing gift from the user list.
    :param user_list_id: (int)
    :param action: (str) Action to be taken. Allowed actions: 'delete' and 'purchase'.
    :raises:
        - NotFound -> If the user list record does NOT exists.
        - Forbidden -> If the action is not allowed for whatever reason.
    """
    ul = UserList.query.get(user_list_id)

    # Check if the record exists for the provided ID.
    if not ul:
        raise NotFound(ERROR_USER_LIST_NOT_FOUND)

    if action in ["delete", "purchase"] and ul.state != "wish":
        # Only a record in 'wish' status can be cancelled or purchased.
        raise Forbidden(ERROR_USER_LIST_ACTION_WRONG_STATE)

    new_state = "cancelled" if action == "delete" else "purchased"
    ul.state = new_state
    ul.write_date = datetime.utcnow()
    db.session.add(ul)
    db.session.commit()


@current_app.route(f"{BASE_PATH}/{COLLECTION_NAME}", methods=['POST'])
@current_app.route(f"{BASE_PATH}/{COLLECTION_NAME}/<int:user_list_id>", methods=['DELETE'])
def create_delete_user_list(version, user_list_id=None):
    """
    Requests to add or remove a gift to/from the user list.
    """
    if version != 1:
        raise NotImplemented

    if request.method.upper() == "POST":
        body = request.get_json()
        user_id = body.get("user_id")
        product_id = body.get("product_id")

        ul = _add_gift_to_list(user_id=user_id, product_id=product_id)

        message = "A user gift was added successfully into the list."
        resource_id = ul.id
        status_code = 201

    else:
        _update_gift_from_list(user_list_id, "delete")

        message = "The user gift has been successfully removed from the list."
        resource_id = None
        status_code = 200

    response = get_successful_response(message=message, resource_id=resource_id)

    return response, status_code


@current_app.route(f"{BASE_PATH}/{COLLECTION_NAME}/<int:user_list_id>/purchase", methods=['PUT'])
def purchase_gift(version, user_list_id=None):
    """
    Requests to purchase a gift from the user list.
    """
    if version != 1:
        raise NotImplemented

    _update_gift_from_list(user_list_id, "purchase")

    message = "A user gift was purchased successfully from the wish list."
    response = get_successful_response(message=message)

    return response, 200
