# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json
import os
import uuid

import pytest
from jose import jwt

from app.app import db, create_app
from app.models.product import Product
from app.models.user import User
from app.models.user_list import UserList

app = create_app()


def get_headers(secret="Super$ecretK3y", token_data=None, login=None, exp=None, audience=None):
    """
    TODO: Improve authentication method.
    Helper function to generate the required header for a token user.
    :param secret: (str) Secret name in AWS. Default value will be from 'TEST_JWT_SECRET' constant.
    :param token_data: (dict) User info such as login or when it is expired.
    :param login: (str) User login. Only used if there is token data. Default value will be 'TEST_JWT_USER'.
    :param exp: (int) Expired token date minus 01-01-1970 in seconds. Only used if there is token data. Default
        value will be today plus one day.
    :param audience: (list) User audience (for access permissions). Default value will be ['pulse_api']
    :return:
    """
    if not token_data:
        token_data = {
            'login': login,
            'exp': exp or int((datetime.now() + timedelta(days=1) - datetime(1970, 1, 1)).total_seconds()),
            'aud': audience or ['pulse_api']
        }

    token = jwt.encode(token_data, secret, algorithm='HS256')

    return {
        'Authorization': f'Bearer {token}'
    }


# Fixtures.
@pytest.fixture
def test_session():
    """
    PyTest fixture to run the application.
    """
    app.config['TESTING'] = True

    test_app = app.test_client()

    with app.app_context():
        # Restart DB.
        db.init_app(app)
        db.drop_all(app=app)
        db.session.commit()
        db.create_all(app=app)

        # Insert demo data.
        # # Users.
        now = datetime.utcnow()
        user_data = {
            "id": str(uuid.uuid4()),
            "login": "demo@theweddingshop.com",
            "password": "demo",
            "name": "Demo user",
            "create_date": now,
            "last_login": now,
            "write_date": now
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        # # Products.
        demo_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'products.json')
        with open(demo_data_path, 'r') as outfile:
            demo_data = json.load(outfile)

        for product_data in demo_data:
            now = datetime.utcnow()
            product_data.update({
                "price": float(product_data["price"][:-3]),
                "create_date": now,
                "write_date": now
            })
            product = Product(**product_data)
            db.session.add(product)

        db.session.commit()

    yield test_app  # To be returned

    # Actions to be done AFTER each test is finished.
