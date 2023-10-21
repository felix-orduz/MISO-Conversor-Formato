from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from models.models import db, User
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')
        email = data.get('email')

        # Validar que las contraseñas coincidan
        if password1 != password2:
            return {'message': 'Las contraseñas no coinciden'}, 400

        # Validar que el usuario y el correo electrónico sean únicos
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': 'El usuario o el correo electrónico ya existen'}, 400

        # Validar que la contraseña cumpla con los lineamientos de seguridad (esto deberás definirlo tú)
        if len(password1) < 6:
            return {'message': 'La contraseña debe tener al menos 6 caracteres'}, 400

        # Crear el nuevo usuario
        new_user = User(username=username, email=email, password=generate_password_hash(password1))
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Cuenta creada con éxito'}, 201
