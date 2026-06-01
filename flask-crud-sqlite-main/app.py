from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.ierwwpjmbdbccbgoccjm:naDUd8vck1Nue0mJ@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "1234abcd"

db = SQLAlchemy(app)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    city     = db.Column(db.String(120), nullable=False)
    contact  = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(150), nullable=False, default='')
    role     = db.Column(db.String(50),  nullable=False, default='Usuario')
    status   = db.Column(db.String(20),  nullable=False, default='Activo')

with app.app_context():
    db.create_all()

# ── INDEX con búsqueda ────────────────────────────────────────────────────────
@app.route("/")
def index():
    q = request.args.get('q', '').strip()
    if q:
        users = User.query.filter(
            (User.name.ilike(f'%{q}%')) |
            (User.city.ilike(f'%{q}%')) |
            (User.email.ilike(f'%{q}%'))
        ).all()
    else:
        users = User.query.all()
    return render_template("index.html", users=users, q=q)

# ── ADD ───────────────────────────────────────────────────────────────────────
@app.route("/add", methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        new_user = User(
            name    = request.form['name'],
            city    = request.form['city'],
            contact = request.form['contact'],
            email   = request.form['email'],
            role    = request.form['role'],
            status  = request.form['status'],
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'Error al agregar usuario!'
    return render_template("add_user.html")

# ── EDIT ──────────────────────────────────────────────────────────────────────
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.name    = request.form['name']
        user.city    = request.form['city']
        user.contact = request.form['contact']
        user.email   = request.form['email']
        user.role    = request.form['role']
        user.status  = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit_user.html", user=user)

# ── DELETE ────────────────────────────────────────────────────────────────────
@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

# ── TOGGLE STATUS (activo/inactivo) ───────────────────────────────────────────
@app.route("/toggle/<int:id>")
def toggle_status(id):
    user = User.query.get_or_404(id)
    user.status = 'Inactivo' if user.status == 'Activo' else 'Activo'
    db.session.commit()
    return redirect(url_for('index'))

# ══════════════════════════════════════════════════════════════════════════════
#  API / MICROSERVICIOS  (JSON)
# ══════════════════════════════════════════════════════════════════════════════

# MS1 – Consulta: todos los usuarios
@app.route("/api/usuarios", methods=['GET'])
def api_get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id, 'name': u.name, 'city': u.city,
        'contact': u.contact, 'email': u.email,
        'role': u.role, 'status': u.status
    } for u in users])

# MS2 – Consulta: usuario por ID
@app.route("/api/usuarios/<int:id>", methods=['GET'])
def api_get_user(id):
    u = User.query.get_or_404(id)
    return jsonify({
        'id': u.id, 'name': u.name, 'city': u.city,
        'contact': u.contact, 'email': u.email,
        'role': u.role, 'status': u.status
    })

# MS3 – Inserción: crear usuario
@app.route("/api/usuarios", methods=['POST'])
def api_create_user():
    data = request.get_json()
    new_user = User(
        name    = data['name'],
        city    = data['city'],
        contact = data['contact'],
        email   = data.get('email', ''),
        role    = data.get('role', 'Usuario'),
        status  = data.get('status', 'Activo'),
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado', 'id': new_user.id}), 201

# MS4 – Reporte: usuarios por ciudad
@app.route("/api/reportes/por-ciudad", methods=['GET'])
def api_report_by_city():
    from sqlalchemy import func
    results = db.session.query(User.city, func.count(User.id)).group_by(User.city).all()
    return jsonify([{'city': city, 'total': total} for city, total in results])

# MS5 – Reporte: activos vs inactivos
@app.route("/api/reportes/estado", methods=['GET'])
def api_report_status():
    activos   = User.query.filter_by(status='Activo').count()
    inactivos = User.query.filter_by(status='Inactivo').count()
    return jsonify({'activos': activos, 'inactivos': inactivos})

if __name__ == "__main__":
    app.run(debug=True)
