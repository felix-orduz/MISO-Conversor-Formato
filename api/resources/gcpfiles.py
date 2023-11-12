from flask import Response
from flask_restful import Resource
from google.cloud import storage
import os
from google.api_core.exceptions import NotFound  # Importa NotFound desde google.api_core.exceptions

class GCPFiles(Resource):
    def __init__(self):
        self.client = storage.Client()

        self.bucket_key = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "file.json"
        self.bucket_name = os.environ.get('GCP_BUCKET_NAME', 'miso-4204-feog-exp1')

    def get(self, filetype, filename):
        if filetype not in ["uploaded", "processed"]:
            return {"message": "Tipo de archivo no válido."}, 400

        # Establecer la ruta en el bucket según el tipo de archivo
        file_path = f"{filetype}/{filename}"  # Ejemplo: 'uploaded/mi_archivo.txt'

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_path)

        try:
            # Intentar descargar el archivo
            file_obj = blob.download_as_bytes()

            # Crear una respuesta con el archivo
            response = Response(file_obj, mimetype='application/octet-stream')
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return response

        except NotFound:
            # Manejar el caso en que el archivo no se encuentra
            return {"message": "Archivo no encontrado."}, 404

    def upload_file(self, file, destination_blob_name):
        """Sube un archivo al bucket de GCP."""
        destination_blob_name = f"uploaded/{destination_blob_name}"
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_file(file)

        return f"Archivo {destination_blob_name} subido a {self.bucket_name}."
