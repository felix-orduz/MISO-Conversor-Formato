from celery import Celery
from sqlalchemy import create_engine, MetaData, Table, update
import os
import ffmpeg

# Configuración de Celery
BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
celery_app = Celery('worker', broker=BROKER_URL)

# Configuración de SQLAlchemy
DATABASE_URI = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.bind = engine
task_table = Table('tasks', metadata, autoload_with=engine)

def convert_file_format(storedFileName, newFormat):

    file_name, _ = os.path.splitext(storedFileName)
    input_file = os.path.join(os.environ.get('SAVE_PATH', '/file_conversor/uploaded/'), storedFileName)

    output_file = os.path.join(os.environ.get('CONVERT_PATH', '/file_conversor/processed/'), file_name +'.'+newFormat )

    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream)
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
        values(status='processed', storedFileName=converted_file_name)
    )
    conn.execute(stmt)
    conn.close()

if __name__ == "__main__":
    celery_app.start()
