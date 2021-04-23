import sqlalchemy
import datetime

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase


class CatalogPage(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'catalog_pages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True,)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    icon = sqlalchemy.Column(sqlalchemy.String, default='')
    fields_type = sqlalchemy.Column(sqlalchemy.String)
    form_value = sqlalchemy.Column(sqlalchemy.String)
    request_data = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)
    is_delete = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    owner = orm.relation('User')