# -*- coding: utf-8 -*-
# 'test_session' is a PyTest fixture to be used in the tests. Do not remove.
from tests.conftests import test_session


def test_healthcheck(test_session):
    """
    Test healthcheck.
    The health check endpoint must return a 200 response in case the service is up and running.
    """
    # Call the healthcheck endpoint.
    response = test_session.get("/healthcheck")

    assert response.status_code == 200
