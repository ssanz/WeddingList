# -*- coding: utf-8 -*-
from flask_swagger_ui import get_swaggerui_blueprint
from yaml import Loader, load

from app.config import SWAGGER_API_URL, SWAGGER_API_YAML_PATH

# Load YAML file.
swagger_api_yml = load(open(SWAGGER_API_YAML_PATH, 'r', encoding='utf-8'), Loader=Loader)


# Create documentation blueprint.
swaggerui_api_blueprint = get_swaggerui_blueprint(
    SWAGGER_API_URL,
    SWAGGER_API_YAML_PATH,
    config={
        'app_name': "The Wedding Shop API",
        'spec': swagger_api_yml,
        'defaultModelRendering': 'model'
    }
)
swaggerui_api_blueprint.name = 'swagger_api_docs'
