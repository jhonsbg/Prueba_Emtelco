from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    identification = db.Column(db.String)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(50))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
