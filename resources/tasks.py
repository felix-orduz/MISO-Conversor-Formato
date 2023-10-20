from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Task, User
from flask_jwt_extended import jwt_required

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
