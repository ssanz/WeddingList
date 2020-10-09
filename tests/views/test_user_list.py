# -*- coding: utf-8 -*-
import json

from app.models.product import Product
from app.models.user import User
from app.models.user_list import UserList
# 'test_session' is a PyTest fixture to be used in the tests. Do not remove.
from tests.conftests import test_session, get_headers

ADD_GIFT_TO_LIST_URL = "user_list/add_gift_to_list"


def test_add_gift_to_list_success(test_session):
    """
    Test add gift to list.

    Check that with the correct body, the endpoint successfully works.
    """
    url = f"/v1/{ADD_GIFT_TO_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product = Product.query.filter_by().first()

    body = {
        "user_id": str(user.id),
        "product_id": product.id
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 201
    assert response.json["status_code"] == 201

    with test_session.application.app_context():
        assert UserList.query.filter_by(id=response.json["resource_id"]).scalar() is not None
