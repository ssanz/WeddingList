# -*- coding: utf-8 -*-
from app.models.product import Product
from app.views.utils import BASE_PATH, manager


COLLECTION_NAME = "product"

product_blueprint = manager.create_api_blueprint(
    Product,
    methods=['GET'],
    url_prefix=BASE_PATH,
    collection_name=COLLECTION_NAME,
    primary_key='id'
)
