from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelo de Tareas
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    completa = db.Column(db.Boolean, default=False)


# Ruta principal
@app.route("/")
def inicio():
    tareas = Tarea.query.all()
    return render_template("base.html", tareas=tareas)


# Agregar tarea
@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form.get("titulo")
    if titulo:
        nueva_tarea = Tarea(titulo=titulo, completa=False)
        db.session.add(nueva_tarea)
        db.session.commit()
    return redirect(url_for("inicio"))


# Cambiar estado (pendiente/completa)
@app.route("/actualizar/<int:tarea_id>")
def actualizar(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    tarea.completa = not tarea.completa
    db.session.commit()
    return redirect(url_for("inicio"))


# Editar tarea (formulario)
@app.route("/editar/<int:tarea_id>", methods=["GET", "POST"])
def editar(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    if request.method == "POST":
        nuevo_titulo = request.form.get("titulo")
        if nuevo_titulo:
            tarea.titulo = nuevo_titulo
            db.session.commit()
            return redirect(url_for("inicio"))
    return render_template("editar.html", tarea=tarea)


# Eliminar tarea
@app.route("/eliminar/<int:tarea_id>")
def eliminar(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for("inicio"))


# Inicializar base de datos y ejecutar
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
