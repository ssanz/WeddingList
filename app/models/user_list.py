# -*- coding: utf-8 -*-
from sqlalchemy.dialects.postgresql import UUID

from app.app import db
from app.models import TheWeddingShopBase


class UserList(TheWeddingShopBase, db.Model):

    __tablename__ = 'user_list'
    __description__ = 'List of user products list.'

    PRODUCT_STATES = ['wish', 'purchased', 'cancelled']

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False)
    state = db.Column(db.VARCHAR(length=32), nullable=False)
    state.matches = PRODUCT_STATES
    create_date = db.Column(db.DateTime(timezone=False), nullable=False)
    write_date = db.Column(db.DateTime(timezone=False), nullable=False)

    product = db.relationship('Product', primaryjoin='UserList.product_id == Product.id', remote_side="Product.id")
    user = db.relationship('User', primaryjoin='UserList.user_id == User.id', remote_side="User.id")
