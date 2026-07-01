import os
import requests
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234abcd"

# ── URLs de los microservicios ─────────────────────────────────────────────────
# Cada operación se delega al microservicio correspondiente
MS_CONSULTA  = "https://ms-consulta.onrender.com"
MS_INSERCION = "https://ms-insercion.onrender.com"
MS_REPORTES  = "https://ms-reportes-87pa.onrender.com"

# ── INDEX con búsqueda ────────────────────────────────────────────────────────
@app.route("/")
def index():
    q = request.args.get('q', '').strip()
    try:
        # Llama al microservicio de consulta para obtener todos los usuarios
        response = requests.get(f"{MS_CONSULTA}/api/usuarios", timeout=10)
        users = response.json()

        # Filtrado local por búsqueda si hay query
        if q:
            users = [u for u in users if
                q.lower() in u['name'].lower() or
                q.lower() in u['city'].lower() or
                q.lower() in u['email'].lower()
            ]
    except Exception as e:
        users = []
        print(f"Error consultando ms-consulta: {e}")

    return render_template("index.html", users=users, q=q)

# ── ADD ───────────────────────────────────────────────────────────────────────
@app.route("/add", methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        # Llama al microservicio de inserción con los datos del formulario
        payload = {
            "name":    request.form['name'],
            "city":    request.form['city'],
            "contact": request.form['contact'],
            "email":   request.form['email'],
            "role":    request.form['role'],
            "status":  request.form['status'],
        }
        try:
            response = requests.post(
                f"{MS_INSERCION}/api/usuarios",
                json=payload,
                timeout=10
            )
            if response.status_code == 201:
                return redirect(url_for("index"))
            else:
                return f"Error al agregar usuario: {response.text}"
        except Exception as e:
            return f"Error conectando al microservicio: {e}"

    return render_template("add_user.html")

# ── EDIT ──────────────────────────────────────────────────────────────────────
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    try:
        # Llama al microservicio de consulta para obtener el usuario por ID
        response = requests.get(f"{MS_CONSULTA}/api/usuarios/{id}", timeout=10)
        user = response.json()
    except Exception as e:
        return f"Error consultando usuario: {e}"

    if request.method == "POST":
        # Llama al microservicio de inserción para actualizar
        payload = {
            "name":    request.form['name'],
            "city":    request.form['city'],
            "contact": request.form['contact'],
            "email":   request.form['email'],
            "role":    request.form['role'],
            "status":  request.form['status'],
        }
        try:
            response = requests.put(
                f"{MS_INSERCION}/api/usuarios/{id}",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                return redirect(url_for('index'))
            else:
                return f"Error al actualizar: {response.text}"
        except Exception as e:
            return f"Error conectando al microservicio: {e}"

    return render_template("edit_user.html", user=user)

# ── DELETE ────────────────────────────────────────────────────────────────────
@app.route("/delete/<int:id>")
def delete_user(id):
    try:
        # Llama al microservicio de inserción para eliminar
        requests.delete(f"{MS_INSERCION}/api/usuarios/{id}", timeout=10)
    except Exception as e:
        print(f"Error eliminando usuario: {e}")
    return redirect(url_for('index'))

# ── TOGGLE STATUS ─────────────────────────────────────────────────────────────
@app.route("/toggle/<int:id>")
def toggle_status(id):
    try:
        # Primero consulta el usuario actual
        response = requests.get(f"{MS_CONSULTA}/api/usuarios/{id}", timeout=10)
        user = response.json()

        # Cambia el estado
        nuevo_status = 'Inactivo' if user['status'] == 'Activo' else 'Activo'

        # Actualiza via microservicio de inserción
        requests.put(
            f"{MS_INSERCION}/api/usuarios/{id}",
            json={"status": nuevo_status},
            timeout=10
        )
    except Exception as e:
        print(f"Error en toggle: {e}")

    return redirect(url_for('index'))
# ── REPORTES ──────────────────────────────────────────────────────────────────
@app.route("/reportes")
def reportes():
    try:
        r_ciudad = requests.get(f"{MS_REPORTES}/api/reportes/por-ciudad", timeout=10)
        r_estado = requests.get(f"{MS_REPORTES}/api/reportes/estado", timeout=10)
        r_rol    = requests.get(f"{MS_REPORTES}/api/reportes/por-rol", timeout=10)
        data_ciudad = r_ciudad.json()
        data_estado = r_estado.json()
        data_rol    = r_rol.json()
    except Exception as e:
        data_ciudad = []
        data_estado = {}
        data_rol    = []
    return render_template("reportes.html",
        data_ciudad=data_ciudad,
        data_estado=data_estado,
        data_rol=data_rol
    )
if __name__ == "__main__":
    app.run(debug=True)
