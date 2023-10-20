import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models.models import db, User, Task
from resources.signup import SignUp
from resources.login import Login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = True
db.init_app(app)
CORS(app)
with app.app_context():
    db.create_all()

app.config['JWT_SECRET_KEY'] = 'tu-secret-key'
jwt = JWTManager(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World'}

api.add_resource(HelloWorld, '/')
api.add_resource(SignUp, '/api/auth/signup')

api.add_resource(Login, '/api/auth/login')

if __name__ == '__main__':
    print(f"Debug xx mode: {'on' if app.debug else 'off'}")
    app.run(debug=True)
