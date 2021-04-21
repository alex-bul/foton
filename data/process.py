import sqlalchemy
import datetime

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase


class Process(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'processes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    customer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    catalog_id = sqlalchemy.Column(sqlalchemy.Integer)
    request_data = sqlalchemy.Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    result_code = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    result = sqlalchemy.Column(sqlalchemy.String)

    customer = orm.relation('User')
