# -*- coding: utf-8 -*-
from sqlalchemy import CheckConstraint

from app.app import db
from app.models import TheWeddingShopBase


class Product(TheWeddingShopBase, db.Model):

    __tablename__ = 'product'
    __description__ = 'List of products available for the users.'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(length=256), nullable=False)
    brand = db.Column(db.VARCHAR(length=256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock_quantity = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(timezone=False), nullable=False)
    write_date = db.Column(db.DateTime(timezone=False), nullable=False)

    __table_args__ = (
        CheckConstraint('id > 0', name='id_greater_than_zero'),
        CheckConstraint('price > 0.0', name='price_greater_than_zero')
    )
