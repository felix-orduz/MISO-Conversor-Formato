import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from sqlalchemy import create_engine, MetaData, Table, update
from models.models import db, User, Task
import ffmpeg
import logging
import ast
from google.cloud import storage
import base64

class Ping(Resource):
    def get(self):
        try:
            # Establecer una conexión y ejecutar una consulta SQL
            tasks = Task.query.all()
            return {'tasks': [dict(id=task.id) for task in tasks]}, 200
        except Exception as e:
            return {'message': str(e)}, 500


logging.basicConfig(level=logging.INFO)
logging.info("Este es un mensaje de info en el log")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['DEBUG'] = True


CORS(app)
api = Api(app)
db.init_app(app)


@app.route("/pubsub/push", methods=["POST"])
def pubsub_push():
    envelope = request.get_json()
    message = envelope['message']

    if not message:
        return 'Mensaje vacío', 400

    try:
        # Decodificar de bytes a string (asumiendo que el mensaje viene en base64)
        message_str = message['data']
        logging.info(f"Mensaje: {message_str}")
        # task_data = ast.literal_eval(message_str)
        decoded_message = base64.b64decode(message_str).decode("utf-8")
        task_data = ast.literal_eval(decoded_message)
        logging.info(f"task_data: {task_data}")
        process_task_from_queue(task_data)
        return 'OK', 200

    except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")
        return 'Error al procesar el mensaje', 500


def process_task_from_queue(task_data):

    logging.info(f"Inicia Conversion: {task_data}")
    # Convertir el archivo
    converted_file_name = convert_file_format(task_data["storedFileName"], task_data["newFormat"])
    logging.info(f"finaliza Conversion: {converted_file_name}")
    # Actualizar la base de datos con el status 'processed'
    try:
        # Encuentra la tarea por su ID y actualiza su estado
        task = Task.query.filter_by(id=task_data["id"]).first()
        logging.info(f"task: {task}")
        if task:
            task.status = 'processed'
            db.session.commit()
    except Exception as e:
        logging.error(f"Error al actualizar la tarea: {e}")
        db.session.rollback()

def convert_file_format(storedFileName, newFormat):

    bucket_name = os.environ.get('GCP_BUCKET_NAME', 'miso-4204-feog-exp1')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Ruta del archivo original en el bucket
    file_path = f"uploaded/{storedFileName}"
    blob_input = bucket.blob(file_path)
    input_file = f"/tmp/{storedFileName}"

    # Descargar el archivo a un directorio temporal
    blob_input.download_to_filename(input_file)

    file_name, _ = os.path.splitext(storedFileName)
    output_file_name = f"{file_name}.{newFormat}"
    output_file = f"/tmp/{output_file_name}"

    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)

    ffmpeg.run(stream)

    destination_blob_name = f"processed/{file_name}.{newFormat}"
    blob = bucket.blob(destination_blob_name)

    with open(output_file, 'rb') as file_obj:
        blob.upload_from_file(file_obj)


    return output_file

api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    print(f"Debug xx mode: {'on' if app.debug else 'off'}")
    app.run(debug=True)
