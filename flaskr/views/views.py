from flask import Flask, request
from flask_restful import Resource
import re

from ..models import db,User, UserSchema

app = Flask(__name__)

user_schema = UserSchema()

class Users(Resource):

    def get(self):
        return [user_schema.dump(user) for user in User.query.all()]

    def post(self):
        try: 
            userId = request.json['identification']
            userName = request.json['name']
            userGenre = request.json['genre']
            userPhone = request.json['phone']
            userEmail = request.json['email']
            validation = True

            regular_phrase = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            emailValidation = re.match(regular_phrase, userEmail) is not None

            existingId = User.query.filter_by(identification = userId).all()
            
            if len(existingId) != 0:
                validation = False
                menssageError = "Usuario ya existente"

            if len(userId) < 4 or len(userId) > 11 :
                validation = False
                menssageError = "Identificación no valida"
            
            if len(userName) < 1 or len(userName) > 100 :
                validation = False
                menssageError = "Longitud de nombre no valido"
            
            if userGenre != "Masculino" and userGenre != "Femenino" and userGenre != "Otro":
                validation = False
                menssageError = "Genero no valido"

            if len(userPhone) != 10:
                validation = False
                menssageError = "Longitud de teléfono no valida"
            
            if userPhone[0] != '3' and userPhone[0] != '6':
                validation = False
                menssageError = "El numero de teléfono debe empezar por 3 o 6"
                print(userPhone[0])

            if emailValidation == False:
                validation = False
                menssageError = "Correo no valido"

            
            if validation:
                newUser = User(identification = userId, name = userName, genre = userGenre, phone = userPhone, email = userEmail)
                db.session.add(newUser)
                db.session.commit()
                return{'message': 'Usuario creado exitosamente'}
            else:
                return{'message': menssageError}
            
        except Exception as e:
            return{'message': 'No es posible crear el usuario'}