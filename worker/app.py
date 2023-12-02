from google.cloud import pubsub_v1
from celery import Celery
from sqlalchemy import create_engine, MetaData, Table, update
import os
import ffmpeg
from google.cloud import storage
import json
import ast
from flask import Flask, request

# Configuración de SQLAlchemy
app = Flask(__name__)
DATABASE_URI = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.bind = engine
task_table = Table('tasks', metadata, autoload_with=engine)


app = Flask(__name__)

@app.route("/pubsub/push", methods=["POST"])
def pubsub_push():
    envelope = request.get_json()
    message = envelope['message']

    if not message:
        return 'Mensaje vacío', 400

    try:
        # Decodificar de bytes a string (asumiendo que el mensaje viene en base64)
        message_str = message['data'].decode("utf-8")
        task_data = ast.literal_eval(message_str)

        process_task_from_queue(task_data)
        return 'OK', 200

    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
        return 'Error al procesar el mensaje', 500
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

def process_task_from_queue(task_data):
    # Convertir el archivo
    converted_file_name = convert_file_format(task_data["storedFileName"], task_data["newFormat"])

    # Actualizar la base de datos con el status 'processed'
    conn = engine.connect()
    stmt = (
        update(task_table).
        where(task_table.c.id == task_data["id"]).
        values(status='processed')
    )
    conn.execute(stmt)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
