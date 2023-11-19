from google.cloud import pubsub_v1
from celery import Celery
from sqlalchemy import create_engine, MetaData, Table, update
import os
import ffmpeg
from google.cloud import storage
import json
import ast

# Configuración de Celery
BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery_app = Celery('worker', broker=BROKER_URL)

# Configuración de SQLAlchemy
DATABASE_URI = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.bind = engine
task_table = Table('tasks', metadata, autoload_with=engine)


# Configuración de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("estudio-gcp-301920", "video_converter-sub")

def callback(message):
    print(f"Recibido mensaje: {message}")
    print(f"mensaje Data: {message.data}")
    try:
        # Decodificar de bytes a string
        message_str = message.data.decode("utf-8")

        # Intenta decodificar como JSON si los datos son un string
        if isinstance(message_str, str):
            task_data = json.loads(message_str)
        # Si ya es un diccionario, úsalo directamente
        elif isinstance(message_str, dict):
            task_data = ast.literal_eval(message_str)
        else:
            raise ValueError("Formato de mensaje no reconocido")

        process_task_from_queue.delay(task_data)
        message.ack()

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error al procesar el mensaje: {e}")


# Escucha de mensajes
subscriber.subscribe(subscription_path, callback=callback)


def convert_file_format(storedFileName, newFormat):

    bucket_name = os.environ.get('GCP_BUCKET_NAME', 'miso-4204-feog-exp1')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Ruta del archivo original en el bucket
    blob_input = bucket.blob(f"uploaded/{storedFileName}")
    input_file = f"/tmp/{storedFileName}"
    # Descargar el archivo a un directorio temporal
    blob_input.download_to_filename(input_file)

    file_name, _ = os.path.splitext(storedFileName)
    output_file_name = f"{file_name}.{newFormat}"
    output_file = f"/tmp/{output_file_name}"
    # input_file = os.path.join(os.environ.get('SAVE_PATH', '/file_conversor/uploaded/'), storedFileName)
    # output_file = os.path.join(os.environ.get('CONVERT_PATH', '/file_conversor/processed/'), file_name +'.'+newFormat )

    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)

    ffmpeg.run(stream)

    destination_blob_name = f"processed/{file_name}.{newFormat}"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(output_file)

    return output_file

@celery_app.task(name='process_task_from_queue')
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
    celery_app.start()
