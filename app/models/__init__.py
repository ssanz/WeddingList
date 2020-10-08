# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declared_attr


class TheWeddingShopBase(object):

    restricted_fields = []

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def columns(self):
        columns = self.__table__.columns.keys()
        return columns

    def as_dict(self):
        unrestricted = [e for e in self.__table__.columns if e.name not in self.restricted_fields]
        return {c.name: getattr(self, c.name) for c in unrestricted}
