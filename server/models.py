from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class User(db.Model, SerializerMixin):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  balance = db.Column(db.Integer, nullable=False)
