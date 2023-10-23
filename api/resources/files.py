from flask_restful import Resource
from flask import send_from_directory
import os

class Files(Resource):
    def get(self, filetype, filename):

        if filetype == "original":
            path = os.environ.get('SAVE_PATH', '/file_conversor/uploaded/')
        elif filetype == "processed":
            path = os.environ.get('CONVERT_PATH', '/file_conversor/processed/')
        else:
            return {"message": "Tipo de archivo no válido."}, 400

        return send_from_directory(path, filename, as_attachment=True)
