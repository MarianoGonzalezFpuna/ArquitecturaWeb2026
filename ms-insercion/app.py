import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.ierwwpjmbdbccbgoccjm:naDUd8vck1Nue0mJ@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100), nullable=False)
    city    = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(150), nullable=False, default='')
    role    = db.Column(db.String(50),  nullable=False, default='Usuario')
    status  = db.Column(db.String(20),  nullable=False, default='Activo')

# ── POST: crear usuario ───────────────────────────────────────────────────────
@app.route('/api/usuarios', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('city') or not data.get('contact'):
        return jsonify({'error': 'Faltan campos requeridos: name, city, contact'}), 400

    new_user = User(
        name    = data['name'],
        city    = data['city'],
        contact = data['contact'],
        email   = data.get('email', ''),
        role    = data.get('role', 'Usuario'),
        status  = data.get('status', 'Activo'),
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'id': new_user.id,
            'name': new_user.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ── PUT: actualizar usuario ───────────────────────────────────────────────────
@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    # Solo actualiza los campos que vienen en el body
    if 'name'    in data: user.name    = data['name']
    if 'city'    in data: user.city    = data['city']
    if 'contact' in data: user.contact = data['contact']
    if 'email'   in data: user.email   = data['email']
    if 'role'    in data: user.role    = data['role']
    if 'status'  in data: user.status  = data['status']

    try:
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado', 'id': user.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ── DELETE: eliminar usuario ──────────────────────────────────────────────────
@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado', 'id': id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ── Health check ──────────────────────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'servicio': 'ms-insercion'})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
