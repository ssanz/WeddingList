# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest, NotFound, NotImplemented

import pdfkit
from flask import current_app, make_response, render_template
from sqlalchemy import and_
from sqlalchemy.exc import DataError

from app.models.product import Product
from app.models.user import User
from app.models.user_list import UserList
from app.views.utils import BASE_PATH, ERROR_USER_ID_BAD_FORMAT, ERROR_USER_NOT_FOUND, manager

COLLECTION_NAME = "user"

user_blueprint = manager.create_api_blueprint(
    User,
    methods=['GET'],
    exclude_columns=['password'],
    url_prefix=BASE_PATH,
    collection_name=COLLECTION_NAME,
    primary_key='id'
)


def _user_list_report(user_id):
    """
    Common method to update an existing gift from the user list.
    :param user_id: (int) User identifier.
    :return: (pdf) Report on PDF format.
    :raises:
        - BadRequest -> If the user ID is in a wrong format.
        - NotFound -> If the user record does NOT exists.
    """
    try:
        user = User.query.get(user_id)
    except DataError:
        raise BadRequest(ERROR_USER_ID_BAD_FORMAT)

    if not user:
        raise NotFound(ERROR_USER_NOT_FOUND)

    user_lists = UserList.query.filter(and_(UserList.user_id == user.id, UserList.state.in_(["wish", "purchased"])))

    wish_product_ids = []
    purchased_product_ids = []

    # Loop through the user products list to set which ones are in the wish list and which ones in the purchased list.
    for ul in user_lists:
        if ul.state == "wish":
            wish_product_ids.append(ul.product_id)
        else:
            purchased_product_ids.append(ul.product_id)

    # Get the wish and purchased products by IDs and their totals.
    wish_products = Product.query.filter(Product.id.in_(wish_product_ids)).scalar() or []
    wish_products = wish_products if isinstance(wish_products, list) else [wish_products]
    wish_total = sum([w.price for w in wish_products]) or 0.0

    purchased_products = Product.query.filter(Product.id.in_(purchased_product_ids)).scalar() or []
    purchased_products = purchased_products if isinstance(purchased_products, list) else [purchased_products]
    purchased_total = sum([p.price for p in purchased_products]) or 0.0

    # Create the template context.
    context = {
        "title": "Report",
        "user": user,
        "wish_products": wish_products,
        "wish_total": wish_total,
        "purchased_products": purchased_products,
        "purchased_total": purchased_total
    }

    # Create PDF file from HTML.
    html = render_template('user_list_report.html', **context, methods=['GET'])
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=report.pdf"

    return response


@current_app.route(f"{BASE_PATH}/{COLLECTION_NAME}/<string:user_id>/report")
def user_list_report(version, user_id):
    """
    Request to display the user list report.
    """
    if version != 1:
        raise NotImplemented

    return _user_list_report(user_id), 200
