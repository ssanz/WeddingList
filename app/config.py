# -*- coding: utf-8 -*-
import os

# Database.
SQLALCHEMY_DATABASE_URI = os.environ["PSQL_DATABASE_URI"]

# Documentation.
BASE_DOCUMENTATION_PATH_V1 = '/v1'
SWAGGER_API_URL = f"{BASE_DOCUMENTATION_PATH_V1}/api_docs"
SWAGGER_API_YAML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'docs/openapi_docs.yaml')
