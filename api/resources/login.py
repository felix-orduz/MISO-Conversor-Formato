from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.models import db, User

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Verificar que el usuario exista
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'El usuario no existe'}, 400

        # Verificar que la contraseña sea correcta
        if not check_password_hash(user.password, password):
            return {'message': 'Contraseña incorrecta'}, 400

        # Crear el token de acceso
        access_token = create_access_token(identity=username)
        return {'token': access_token}, 200
