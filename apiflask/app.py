from flask import Flask, request
from flask_sqlachemy import SQLAlchemy

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI']='mysql+pymsql://root@localhost/flaskmysql'
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
    
    print(request.json)
    return 'recibido'


if __name__ == '__main__':
    app.run(debug=True)
