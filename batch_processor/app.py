from flask import Flask
from celery import Celery
from apscheduler.schedulers.background import BackgroundScheduler
import os
from sqlalchemy import create_engine, MetaData, Table

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configuración de SQLAlchemy para conectar a la base de datos
DATABASE_URI = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URI)
metadata = MetaData()
metadata.bind = engine

# Función que lee de la tabla y encola en Redis
def process_uploaded_tasks():
    # Acceso a la tabla "task" usando SQLAlchemy
    task_table = Table('tasks', metadata, autoload_with=engine)
    conn = engine.connect()

    # Buscar registros con estado "uploaded"
    uploaded_tasks = conn.execute(task_table.select().where(task_table.c.status == "uploaded")).fetchall()

    # Poner en cola (por ejemplo, guardando en Redis)
    for task in uploaded_tasks:
        # Tu lógica para encolar cada tarea en Redis aquí
        task_data = {
            "id": task.id,
            "storedFileName": task.storedFileName,
            "newFormat": task.newFormat
        }
        # Aquí encolamos el task_data en Redis usando Celery
        celery.send_task("process_task_from_queue", args=[task_data])
        task_id = task.id
        # Actualiza el estado de la tarea en la base de datos a "enqueued"
        conn.execute(task_table.update().where(task_table.c.id == task_id).values(status='enqueued'))
        conn.commit()  # Confirmar la transacción

    conn.close()

# Función para programar la tarea
def schedule_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=process_uploaded_tasks, trigger="interval", seconds=30)
    scheduler.start()

schedule_tasks()

if __name__ == "__main__":
    app.run()
