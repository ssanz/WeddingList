# -*- coding: utf-8 -*-
import json
import uuid

from sqlalchemy import and_

from app.app import db
from app.models.product import Product
from app.models.user import User
from app.models.user_list import UserList
from app.views.utils import ERROR_NOT_ENOUGH_STOCK, ERROR_PRODUCT_ID_BAD_FORMAT, ERROR_PRODUCT_NOT_FOUND,\
    ERROR_USER_ID_BAD_FORMAT, ERROR_USER_LIST_ACTION_WRONG_STATE, ERROR_USER_LIST_NOT_FOUND,\
    ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS, ERROR_USER_NOT_FOUND
from app.views.user_list import COLLECTION_NAME as USER_LIST_URL
# 'test_session' is a PyTest fixture to be used in the tests. Do not remove.
from tests.conftests import test_session, get_headers


def test_add_gift_to_list_success(test_session):
    """
    Test add gift to list success.

    Check that with the correct body, the endpoint does not raise any exception, the record has been created and the
    stock has been decreased by one.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product = Product.query.filter(Product.in_stock_quantity > 0).first()

    old_stock = product.in_stock_quantity

    body = {
        "user_id": str(user.id),
        "product_id": product.id
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 201

    with test_session.application.app_context():
        assert UserList.query.filter_by(id=response.json["resource_id"]).scalar() is not None
        product = Product.query.get(product.id)
        assert product.in_stock_quantity == (old_stock - 1)


def test_add_gift_to_list_user_wrong_format(test_session):
    """
    Test add gift to list user wrong format.

    Check that with a wrong user ID format, it raises a BadRequest exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    body = {
        "user_id": "wrong_user_id",
        "product_id": 1
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 400
    assert response.json["error_message"] == ERROR_USER_ID_BAD_FORMAT


def test_add_gift_to_list_user_not_found(test_session):
    """
    Test add gift to list user not found.

    Check that if the user does not exists, it raises a NotFound exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    body = {
        "user_id": str(uuid.uuid4()),
        "product_id": 1
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 404
    assert response.json["error_message"] == ERROR_USER_NOT_FOUND


def test_add_gift_to_list_product_wrong_format(test_session):
    """
    Test add gift to list product wrong format.

    Check that with a wrong product ID format, it raises a BadRequest exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()

    body = {
        "user_id": str(user.id),
        "product_id": "bad_product_id"
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 400
    assert response.json["error_message"] == ERROR_PRODUCT_ID_BAD_FORMAT


def test_add_gift_to_list_product_not_found(test_session):
    """
    Test add gift to list product not found.

    Check that if the product does not exists, it raises a NotFound exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()

    body = {
        "user_id": str(user.id),
        "product_id": 0
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 404
    assert response.json["error_message"] == ERROR_PRODUCT_NOT_FOUND


def test_add_gift_to_list_not_enough_stock(test_session):
    """
    Test add gift to list not enough stock.

    Check that if there is not enough stock, it raises a Forbidden exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product = Product.query.filter_by(in_stock_quantity=0).first()

    body = {
        "user_id": str(user.id),
        "product_id": product.id
    }

    # Call the add gift to list endpoint.
    response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    assert response.status_code == 403
    assert response.json["error_message"] == ERROR_NOT_ENOUGH_STOCK


def test_add_gift_to_list_already_exists(test_session):
    """
    Test add gift to list not enough stock.

    Check that if there is not enough stock, it raises a Forbidden exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product_ids = [user_list.product_id for user_list in UserList.query.filter_by(user_id=user.id)]
        product = Product.query.filter(and_(Product.in_stock_quantity > 0, ~Product.id.in_(product_ids))).first()

    body = {
        "user_id": str(user.id),
        "product_id": product.id
    }

    with test_session.application.app_context():
        # Call the add gift to list endpoint.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

        # Check that the request was successful.
        assert response.status_code == 201

        # Call the add the same gift to list.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

    # Check that this time the same request raises a forbidden action.
    assert response.status_code == 403
    assert response.json["error_message"] == ERROR_USER_LIST_PRODUCT_ALREADY_EXISTS


def test_remove_gift_from_list_success(test_session):
    """
    Test remove gift from list success.

    Check that if a correct DELETE request is send through an existing record, it is possible to delete it.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product_ids = [user_list.product_id for user_list in UserList.query.filter_by(user_id=user.id)]
        product = Product.query.filter(and_(Product.in_stock_quantity > 0, ~Product.id.in_(product_ids))).first()

        body = {
            "user_id": str(user.id),
            "product_id": product.id
        }

        # Create a user list record.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

        # Check that the request was successful.
        assert response.status_code == 201

        # Delete the user list record.
        ul_id = response.json['resource_id']
        delete_url = f"{url}/{ul_id}"
        response = test_session.delete(delete_url, headers=headers, content_type="application/json")

        # Check that this time the same request raises a forbidden action.
        assert response.status_code == 200

        # Check that the record has been deleted.
        assert UserList.query.filter_by(id=ul_id, state="cancelled").scalar() is not None


def test_remove_gift_from_list_not_found(test_session):
    """
    Test remove gift from list not found.

    Check that if a DELETE request is send to remove an unexisting record, it raises a NotFound exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        # Try to delete an unexistent user list record.
        delete_url = f"{url}/9999"
        response = test_session.delete(delete_url, headers=headers, content_type="application/json")

        # Check that this time the same request raises a forbidden action.
        assert response.status_code == 404
        assert response.json["error_message"] == ERROR_USER_LIST_NOT_FOUND


def test_remove_gift_from_list_wrong_state(test_session):
    """
    Test remove gift from list wrong state.

    Check that if a DELETE request is send to a record that is NOT in 'wish' status, it raises a Forbidden exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product_ids = [user_list.product_id for user_list in UserList.query.filter_by(user_id=user.id)]
        product = Product.query.filter(and_(Product.in_stock_quantity > 0, ~Product.id.in_(product_ids))).first()

        body = {
            "user_id": str(user.id),
            "product_id": product.id
        }

        # Create a user list record.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

        # Check that the request was successful.
        assert response.status_code == 201

        # Update record with any of the stats in which it must raise the exception and try to delete it.
        fail_states = ["cancelled", "purchased"]
        ul = UserList.query.get(response.json['resource_id'])

        for new_state in fail_states:
            ul.state = new_state
            db.session.add(ul)
            db.session.commit()

            # Delete the user list record.
            delete_url = f"{url}/{ul.id}"
            response = test_session.delete(delete_url, headers=headers, content_type="application/json")

            # Check that this time the same request raises a forbidden action.
            assert response.status_code == 403
            assert response.json["error_message"] == ERROR_USER_LIST_ACTION_WRONG_STATE


def test_purchase_gift_from_list_success(test_session):
    """
    Test purchase gift from list success.

    Check that if a correct PUT request is send through an existing record, it is possible to purchase it.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product_ids = [user_list.product_id for user_list in UserList.query.filter_by(user_id=user.id)]
        product = Product.query.filter(and_(Product.in_stock_quantity > 0, ~Product.id.in_(product_ids))).first()

        body = {
            "user_id": str(user.id),
            "product_id": product.id
        }

        # Create a user list record.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

        # Check that the request was successful.
        assert response.status_code == 201

        # Purchase the user list record.
        ul_id = response.json['resource_id']
        purchase_url = f"{url}/{ul_id}/purchase"
        response = test_session.put(purchase_url, headers=headers, content_type="application/json")

        # Check that this time the same request raises a forbidden action.
        assert response.status_code == 200

        # Check that the record has been deleted.
        assert UserList.query.filter_by(id=ul_id, state="purchased").scalar() is not None


def test_purchase_gift_from_list_not_found(test_session):
    """
    Test purchase gift from list not found.

    Check that if a PUT request is send to purchase an unexisting record, it raises a NotFound exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        # Try to purchase an unexistent user list record.
        purchase_url = f"{url}/9999/purchase"
        response = test_session.put(purchase_url, headers=headers, content_type="application/json")

        # Check that this time the same request raises a forbidden action.
        assert response.status_code == 404
        assert response.json["error_message"] == ERROR_USER_LIST_NOT_FOUND


def test_purchase_gift_from_list_wrong_state(test_session):
    """
    Test purchase gift from list wrong state.

    Check that if a PUT request is send to a record that is NOT in 'wish' status, it raises a Forbidden exception.
    """
    url = f"/v1/{USER_LIST_URL}"
    headers = get_headers()

    with test_session.application.app_context():
        user = User.query.filter_by().first()
        product_ids = [user_list.product_id for user_list in UserList.query.filter_by(user_id=user.id)]
        product = Product.query.filter(and_(Product.in_stock_quantity > 0, ~Product.id.in_(product_ids))).first()

        body = {
            "user_id": str(user.id),
            "product_id": product.id
        }

        # Create a user list record.
        response = test_session.post(url, data=json.dumps(body), headers=headers, content_type="application/json")

        # Check that the request was successful.
        assert response.status_code == 201

        # Update record with any of the stats in which it must raise the exception and try to purchase it.
        fail_states = ["cancelled", "purchased"]
        ul = UserList.query.get(response.json['resource_id'])

        for new_state in fail_states:
            ul.state = new_state
            db.session.add(ul)
            db.session.commit()

            # Purchase the user list record.
            purchase_url = f"{url}/{ul.id}/purchase"
            response = test_session.put(purchase_url, headers=headers, content_type="application/json")

            # Check that this time the same request raises a forbidden action.
            assert response.status_code == 403
            assert response.json["error_message"] == ERROR_USER_LIST_ACTION_WRONG_STATE
