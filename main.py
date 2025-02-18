from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

# Inicialización de la aplicación y la base de datos
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Definir el modelo de datos con SQLAlchemy
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'Task({self.id}, {self.name})'

# Definir el formato de los datos a devolver usando marshal_with
taskFields = {
    'id': fields.Integer,
    'name': fields.String,
}

# Clase Items (para manejar múltiples tareas)
class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        # Recuperar todas las tareas de la base de datos
        tasks = Task.query.all()
        return tasks

    @marshal_with(taskFields)
    def post(self):
        # Crear una nueva tarea y agregarla a la base de datos
        data = request.json
        task = Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        return task

# Clase Item (para manejar una tarea específica)
class Item(Resource):
    @marshal_with(taskFields)
    def get(self, pk):
        # Recuperar una tarea específica por su ID
        task = Task.query.filter_by(id=pk).first()
        return task

    @marshal_with(taskFields)
    def put(self, pk):
        # Actualizar una tarea específica
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        if task:
            task.name = data['name']
            db.session.commit()
            return task
        return {'message': 'Task not found'}, 404

    @marshal_with(taskFields)
    def delete(self, pk):
        # Eliminar una tarea específica
        task = Task.query.filter_by(id=pk).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted'}
        return {'message': 'Task not found'}, 404

# Agregar las rutas para los recursos
api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<int:pk>')

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
