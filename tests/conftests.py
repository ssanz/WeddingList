# -*- coding: utf-8 -*-
from datetime import datetime
import json
import os
import uuid

import pytest

from app.app import db, create_app
from app.models.product import Product
from app.models.user import User
from app.models.user_list import UserList

app = create_app()


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
