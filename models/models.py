from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    originalFileName = db.Column(db.String, nullable=False)  # Nombre original del archivo
    storedFileName = db.Column(db.String, nullable=False)    # Nombre del archivo con UUID
    newFormat = db.Column(db.String, nullable=True)          # Formato al que se desea cambiar (si lo requieres)
    status = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Task {self.id}>'
