# -*- coding: utf-8 -*-
import json
import uuid

from app.models.product import Product
from app.models.user import User

from app.views.user import COLLECTION_NAME as USER_URL
from app.views.user_list import COLLECTION_NAME as USER_LIST_URL
from app.views.utils import ERROR_USER_ID_BAD_FORMAT, ERROR_USER_NOT_FOUND
# 'test_session' is a PyTest fixture to be used in the tests. Do not remove.
from tests.conftests import test_session, get_headers


def test_report_success(test_session):
    """
    Test report success.

    Check that if a user exists, it is possible to retrieve a report from them.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        # Get a user and two products.
        user = User.query.filter_by().first()
        products = Product.query.filter().limit(2).all()

        # Generate at least a gift in the wish list.
        body = {
            "user_id": str(user.id),
            "product_id": products[0].id
        }
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")
        assert response.status_code == 201

        # Generate at least a gift in the purchased list.
        body = {
            "user_id": str(user.id),
            "product_id": products[1].id
        }

        # # Add the product to the wish list.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")
        assert response.status_code == 201

        # # Purchase the product.
        ul_id = response.json['resource_id']
        purchase_url = f"{url}/{ul_id}/purchase"
        response = test_session.put(purchase_url, headers=headers, content_type="application/json")
        assert response.status_code == 200

        # Get the user list record.
        url = f"/v1/{USER_URL}/{user.id}/report"
        response = test_session.get(url, headers=headers)

        # Check that the request was successful.
        assert response.status_code == 200
        assert response.mimetype == "application/pdf"


def test_report_user_id_bad_format(test_session):
    """
    Test report user id bad format.

    Check that if a user is in a bad format, the request raises a BadRequest exception.
    """
    headers = get_headers()

    with test_session.application.app_context():
        url = f"/v1/{USER_URL}/1/report"

        # Call the report endpoint.
        response = test_session.get(url, headers=headers)

        # Check the response.
        assert response.status_code == 400
        assert response.json["error_message"] == ERROR_USER_ID_BAD_FORMAT


def test_report_user_not_found(test_session):
    """
    Test report user not found.

    Check that if a user does NOT exists, the request raises a NotFound exception.
    """
    headers = get_headers()

    with test_session.application.app_context():
        url = f"/v1/{USER_URL}/{str(uuid.uuid4())}/report"

        # Call the report endpoint.
        response = test_session.get(url, headers=headers)

        # Check the response.
        assert response.status_code == 404
        assert response.json["error_message"] == ERROR_USER_NOT_FOUND
