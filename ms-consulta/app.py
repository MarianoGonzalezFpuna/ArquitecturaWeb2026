import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Lee la DATABASE_URL desde las variables de entorno de Render
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.ierwwpjmbdbccbgoccjm:naDUd8vck1Nue0mJ@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Mismo modelo que la app principal
class User(db.Model):
    __tablename__ = 'user'
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100), nullable=False)
    city    = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(150), nullable=False, default='')
    role    = db.Column(db.String(50),  nullable=False, default='Usuario')
    status  = db.Column(db.String(20),  nullable=False, default='Activo')

# ── Consulta 1: todos los usuarios ───────────────────────────────────────────
# GET /api/usuarios
# Devuelve la lista completa de usuarios en formato JSON
@app.route('/api/usuarios', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id':      u.id,
        'name':    u.name,
        'city':    u.city,
        'contact': u.contact,
        'email':   u.email,
        'role':    u.role,
        'status':  u.status
    } for u in users])

# ── Consulta 2: usuario por ID ────────────────────────────────────────────────
# GET /api/usuarios/<id>
# Devuelve un usuario específico por su ID
@app.route('/api/usuarios/<int:id>', methods=['GET'])
def get_user_by_id(id):
    u = User.query.get_or_404(id)
    return jsonify({
        'id':      u.id,
        'name':    u.name,
        'city':    u.city,
        'contact': u.contact,
        'email':   u.email,
        'role':    u.role,
        'status':  u.status
    })

# ── Health check ──────────────────────────────────────────────────────────────
# GET /health
# Render usa esto para saber si el servicio está vivo
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'servicio': 'ms-consulta'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
