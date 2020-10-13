# -*- coding: utf-8 -*-
import passlib  # DO NOT REMOVE: Necessary internally for 'password' field.

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import PasswordType, force_auto_coercion

from app.app import db
from app.models import TheWeddingShopBase

force_auto_coercion()


class User(TheWeddingShopBase, db.Model):

    __tablename__ = 'user'
    __description__ = 'List of users that can access to the service.'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    login = db.Column(db.VARCHAR(length=256), unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    name = db.Column(db.VARCHAR(length=256), nullable=False)
    create_date = db.Column(db.DateTime(timezone=False), nullable=False)
    last_login = db.Column(db.DateTime(timezone=False))
    write_date = db.Column(db.DateTime(timezone=False), nullable=False)
