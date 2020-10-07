# -*- coding: utf-8 -*-
from app.app import db
from app.models import TheWeddingShopBase


class UserList(TheWeddingShopBase, db.Model):

    __tablename__ = 'user_list'
    __description__ = 'List of user products list.'

    PRODUCT_STATES = ['wish', 'purchased', 'cancelled']

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column('user_id', db.String, db.ForeignKey('user.id'), nullable=False),
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False)
    state = db.Column(db.VARCHAR(length=32), nullable=False)
    state.matches = PRODUCT_STATES
    create_date = db.Column(db.DateTime(timezone=False), nullable=False)
    write_date = db.Column(db.DateTime(timezone=False), nullable=False)
