# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.exc import DataError
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, NotImplemented

from flask import current_app, request

from app.app import db
from app.models.user import User
from app.models.product import Product
from app.models.user_list import UserList
from app.views.utils import BASE_PATH, ERROR_NOT_ENOUGH_STOCK, ERROR_PRODUCT_ID_BAD_FORMAT, ERROR_PRODUCT_NOT_FOUND,\
    ERROR_USER_ID_BAD_FORMAT, ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS, ERROR_USER_NOT_FOUND, get_successful_response,\
    manager

COLLECTION_NAME = "user_list"

user_list_blueprint = manager.create_api_blueprint(
    UserList,
    methods=['GET'],
    url_prefix=BASE_PATH,
    collection_name=COLLECTION_NAME,
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
    ul = UserList.query.filter_by(user_id=user_id, product_id=product_id).scalar()
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


def _remove_gift_from_list(user_list_id):
    """
    Common method to remove an existing gift from the user list.
    :param user_list_id: (int)
    :raises:
        - NotFound -> If the user list does not exists.
        - Forbidden -> If the product was already cancelled or purchased.
    """
    try:
        ul = UserList.query.get(user_list_id)
    except:
        raise

    if ul.state != "gift":
        raise

    ul.state = "cancelled"


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
        _remove_gift_from_list(user_list_id)

        message = "The user gift has been successfully removed from the list."
        resource_id = None
        status_code = 200

    response = get_successful_response(message=message, resource_id=resource_id)

    return response, status_code
