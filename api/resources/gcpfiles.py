
from flask_restful import Resource
from google.cloud import storage
import os
class GCPFiles(Resource):
    def __init__(self):
        self.client = storage.Client()

        self.bucket_key = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/felixernestoorduzgrimaldo/Documents/Estudio/MISO/repos/MISO-Conversor-Formato/api/file.json"
        self.bucket_name = os.environ.get('GCP_BUCKET_NAME', 'miso-4204-feog-exp1')

    def get(self, filetype, filename):
        if filetype not in ["original", "processed"]:
            return {"message": "Tipo de archivo no válido."}, 400

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(filename)

        # Generar URL de descarga
        url = blob.generate_signed_url(version="v4",
                                       expiration=datetime.timedelta(minutes=15),
                                       method="GET")

        return {"url": url}

    def upload_file(self, file, destination_blob_name):
        """Sube un archivo al bucket de GCP."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_file(file)

        return f"Archivo {destination_blob_name} subido a {self.bucket_name}."
