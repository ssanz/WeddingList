# -*- coding: utf-8 -*-
from flask import jsonify, current_app

from app.docs.setup import swaggerui_api_blueprint
from app.views.healthcheck import healthcheck
from app.views.homepage import homepage

# Set up public URLs.
public_urls = [
    '/healthcheck',
    f"{current_app.config['SWAGGER_API_URL']}/",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui.css",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui-bundle.js",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui-standalone-preset.js"
]

# Register blueprints.
current_app.register_blueprint(swaggerui_api_blueprint, url_prefix=current_app.config["SWAGGER_API_URL"])
