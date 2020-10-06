# -*- coding: utf-8 -*-
import pytest

from app.app import create_app

app = create_app()

# Fixtures.
@pytest.fixture
def test_session():
    """
    PyTest fixture to run the application.
    """
    app.config['TESTING'] = True

    test_app = app.test_client()

    yield test_app  # To be returned

    # TODO: Actions to be done AFTER each test is finished.
