from flask_restful import Resource, reqparse
import uuid
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Task, User, db
from flask_jwt_extended import jwt_required
from datetime import datetime
import os

class Tasks(Resource):
    @jwt_required()  # Requiere autenticación mediante un token Bearer
    def get(self):
        current_username = get_jwt_identity()  # Obtén el username del token JWT
        user = User.query.filter_by(username=current_username).first()

        if user is None:
            return {"message": "Usuario no encontrado"}, 404

        # Consulta las tareas del usuario actual desde la base de datos usando user.id
        tasks = Task.query.filter_by(user_id=user.id).all()

        # Convierte las tareas en un formato adecuado (por ejemplo, a diccionarios)
        tasks_list = [
            {"id": task.id, "user_id": task.user_id, "timestamp": task.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
            for task in tasks
        ]

        return tasks_list,200

    @jwt_required()
    def post(self):
        if 'file' not in request.files:
            return {"message": "No se encontró el archivo en la solicitud."}, 400

        uploaded_file = request.files['file']

        # Verifica que el archivo no esté vacío
        if uploaded_file.filename == '':
            return {"message": "El archivo está vacío."}, 400

        _, file_extension = os.path.splitext(uploaded_file.filename)

        # Genera un ID único para el archivo y concatena la extensión
        unique_filename = str(uuid.uuid4()) + file_extension

        # Usa el nombre único con extensión al guardar
        save_path = os.path.join("/Users/felixernestoorduzgrimaldo/Documents/Estudio/MISO/test_temp/", unique_filename)

        # Guarda el archivo en la ruta especificada
        uploaded_file.save(save_path)

        # Parsea los parámetros de la solicitud
        parser = reqparse.RequestParser()
        parser.add_argument('newFormat', type=str, required=True, help='Formato al que desea cambiar el archivo cargado', location='form')
        args = parser.parse_args()

        current_username = get_jwt_identity()  # Obtén el username del token JWT
        user = User.query.filter_by(username=current_username).first()


        # Crea una nueva tarea
        new_task = Task(
            user_id=user.id,
            originalFileName=uploaded_file.filename,  # Nombre original del archivo
            storedFileName=unique_filename,  # Nombre con UUID
            newFormat=args['newFormat'],
            timestamp=datetime.now(),
            status='uploaded'
        )

        # Guarda la tarea en la base de datos
        db.session.add(new_task)
        db.session.commit()

        return {"message": "Tarea creada exitosamente"}, 201  # 201 significa "Created"
