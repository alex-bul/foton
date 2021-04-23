import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    processes = orm.relation("Process", back_populates='customer')
    pages = orm.relation("CatalogPage", back_populates='owner')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
