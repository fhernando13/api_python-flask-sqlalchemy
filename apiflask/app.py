from crypt import methods
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Tarea(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True)
    descripcion = db.Column(db.String(100))

    def __init__(self, titulo, descripcion):

        self.titulo = titulo
        self.descripcion = descripcion

db.create_all()

class TareaSchema(ma.Schema):

    class Meta:
        fields = ('id','titulo','descripcion')

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    
    titulo =  request.json['titulo']
    descripcion = request.json['descripcion']

    new_tarea = Tarea(titulo, descripcion)
    db.session.add(new_tarea)
    db.session.commit()

    return tarea_schema.jsonify(new_tarea)

@app.route('/leer_tareas', methods=['GET'])
def leer_tareas():
    
    all_tareas = Tarea.query.all()
    resultado = tareas_schema.dump(all_tareas)
    return jsonify(resultado)

@app.route('/leer_tarea_unica/<id>', methods=['GET'])
def leer_tarea_unica(id):

    tarea = Tarea.query.get(id)
    return tarea_schema.jsonify(tarea)

@app.route('/actualizar_tarea/<id>', methods=['PUT'])
def actualizar_tarea(id):

    tarea = Tarea.query.get(id)
    titulo =  request.json['titulo']
    descripcion = request.json['descripcion']

    tarea.titulo = titulo
    tarea.descripcion = descripcion

    db.session.commit()

    return tarea_schema.jsonify(tarea)

@app.route('/eliminar_tarea/<id>', methods=['DELETE'])
def eliminar_tarea(id):

    tarea = Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()

    return tarea_schema.jsonify(tarea)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Bienvenido a mi API'})

if __name__ == '__main__':
    app.run(debug=True)
