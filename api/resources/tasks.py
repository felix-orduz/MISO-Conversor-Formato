from flask_restful import Resource, reqparse
import uuid
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Task, User, db
from flask_jwt_extended import jwt_required
from datetime import datetime
from resources.gcpfiles import GCPFiles
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
        unique_uuid = str(uuid.uuid4())
        # Genera un ID único para el archivo y concatena la extensión
        unique_filename = unique_uuid + file_extension

        # Usa el nombre único con extensión al guardar
        save_path = os.path.join(os.environ.get('SAVE_PATH', '/file_conversor/uploaded/'), unique_filename)

        # Guarda el archivo en la ruta especificada
        #uploaded_file.save(save_path)

        # Crear instancia de GCPFiles y subir el archivo
        file = request.files['file']
        gcp_files = GCPFiles()
        gcp_files.upload_file(file, unique_filename)

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

        server_uri = os.environ.get('SERVER_URI', 'http://localhost:5001/')
        original_file_url = f"{server_uri}files/original/{new_task.storedFileName}"
        processed_file_url = f"{server_uri}files/processed/{unique_uuid}.{new_task.newFormat}"

        task_info = {
            "id": new_task.id,
            "user_id": new_task.user_id,
            "timestamp": new_task.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "original_file_url": original_file_url,
            "processed_file_url": processed_file_url,
            "status":new_task.status
        }

        return task_info, 201  # 201 significa "Created"

    @jwt_required()
    def get(self, id_task=None):
        current_username = get_jwt_identity()  # Obtén el username del token JWT
        user = User.query.filter_by(username=current_username).first()
        server_uri = os.environ.get('SERVER_URI', 'http://localhost:5001/')

        if user is None:
            return {"message": "Usuario no encontrado"}, 404

        # Si se proporciona id_task, recupera la tarea específica
        if id_task:
            task = Task.query.filter_by(id=id_task, user_id=user.id).first()

            if task is None:
                return {"message": "Tarea no encontrada"}, 404

            # Genera las URLs para recuperar/descargar los archivos
            original_file_url = f"{server_uri}files/original/{task.storedFileName}"
            filename,_ = os.path.splitext(task.storedFileName)
            processed_file_url = f"{server_uri}files/processed/{filename}.{task.newFormat}"

            task_info = {
                "id": task.id,
                "user_id": task.user_id,
                "timestamp": task.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "original_file_url": original_file_url,
                "processed_file_url": processed_file_url,
                "status":task.status
            }

            return task_info, 200

        # Si no se proporciona id_task, devuelve la lista de tareas
        else:
            tasks = Task.query.filter_by(user_id=user.id).all()

            tasks_list = []
            for task in tasks:
                original_file_url = f"{server_uri}files/original/{task.storedFileName}"
                filename, _ = os.path.splitext(task.storedFileName)
                processed_file_url = f"{server_uri}files/processed/{filename}.{task.newFormat}"

                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "timestamp": task.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "original_file_url": original_file_url,
                    "processed_file_url": processed_file_url,
                    "status":task.status
                }
                tasks_list.append(task_dict)

            return tasks_list, 200

    @jwt_required()
    def delete(self, id_task):
        current_username = get_jwt_identity()  # Obtén el username del token JWT
        user = User.query.filter_by(username=current_username).first()

        if user is None:
            return {"message": "Usuario no encontrado"}, 404

        task = Task.query.filter_by(id=id_task, user_id=user.id).first()

        if task is None:
            return {"message": "Tarea no encontrada"}, 404

        if task.status != 'processed':
            return {"message": "Tarea no esta en estado processed"}, 400

        # Elimina la tarea de la base de datos
        db.session.delete(task)
        db.session.commit()

        return {}, 204  # 204 significa "No Content", usado para respuestas exitosas sin contenido
