# -*- coding: utf-8 -*-
from flask import current_app, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, MethodNotAllowed, NotFound, NotImplemented

from app.docs.setup import swaggerui_api_blueprint
from app.views.healthcheck import healthcheck
from app.views.homepage import homepage
from app.views.product import product_blueprint
from app.views.user import user_blueprint
from app.views.user_list import user_list_blueprint

# Set up public URLs.
public_urls = [
    '/healthcheck',
    f"{current_app.config['SWAGGER_API_URL']}/",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui.css",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui-bundle.js",
    f"{current_app.config['SWAGGER_API_URL']}/swagger-ui-standalone-preset.js"
]


@product_blueprint.url_value_preprocessor
@user_blueprint.url_value_preprocessor
@user_list_blueprint.url_value_preprocessor
def path_preprocessor(endpoint, values):
    """
    Preprocessor function that will:
    - Remove the dynamic values from the URL prefix. If the dynamic values are not removed, it will raise a
     "TypeError" exception "got an unexpected keyword argument 'xxxxx'" (where 'xxxxx' is the key).
     Some documentation can be found here: https://flask.palletsprojects.com/en/1.0.x/patterns/urlprocessors/
    :param endpoint: (str) Endpoint.
    :param values: (dict) Dynamic values from the path.
    """
    # Remove the 'version' code from the dynamic values.
    values.pop('version')


# Register blueprints.
# # Documentation.
current_app.register_blueprint(swaggerui_api_blueprint, url_prefix=current_app.config["SWAGGER_API_URL"])
# # Endpoints.
current_app.register_blueprint(product_blueprint)
current_app.register_blueprint(user_blueprint)
current_app.register_blueprint(user_list_blueprint)


@current_app.errorhandler(BadRequest)
@current_app.errorhandler(Forbidden)
@current_app.errorhandler(MethodNotAllowed)
@current_app.errorhandler(NotFound)
@current_app.errorhandler(NotImplemented)
def wsgi_tool_error_handler(e):
    """
    Error handler for a HTTP Exception raised by the APP.
    """
    status_code = e.code
    result = {
        "error_message": e.description,
        "error_code": e.name.upper().replace(" ", "_")
    }
    return jsonify(result), status_code


@current_app.errorhandler(Exception)
def handle_uncaught_error(e):
    """
    Error handler for unexpected internal server error exceptions. This exceptions must be fixed in case we got one.
    """
    status_code = 500

    result = {
        "error_message": "Unknown or unexpected error.",
        "error_code": "INTERNAL_SERVER_ERROR"
    }
    return jsonify(result), status_code
