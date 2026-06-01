import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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

# ── Reporte 1: usuarios agrupados por ciudad ──────────────────────────────────
# GET /api/reportes/por-ciudad
# Devuelve cuántos usuarios hay en cada ciudad
# Ejemplo de respuesta:
# [{"city": "Asunción", "total": 5}, {"city": "CDE", "total": 3}]
@app.route('/api/reportes/por-ciudad', methods=['GET'])
def report_by_city():
    results = db.session.query(
        User.city,
        func.count(User.id).label('total')
    ).group_by(User.city).all()

    return jsonify([{
        'city':  city,
        'total': total
    } for city, total in results])

# ── Reporte 2: usuarios activos vs inactivos ──────────────────────────────────
# GET /api/reportes/estado
# Devuelve el conteo de usuarios activos e inactivos
# Ejemplo de respuesta:
# {"activos": 8, "inactivos": 2, "total": 10}
@app.route('/api/reportes/estado', methods=['GET'])
def report_status():
    activos   = User.query.filter_by(status='Activo').count()
    inactivos = User.query.filter_by(status='Inactivo').count()
    total     = activos + inactivos

    return jsonify({
        'activos':   activos,
        'inactivos': inactivos,
        'total':     total
    })

# ── Reporte 3: usuarios por rol ───────────────────────────────────────────────
# GET /api/reportes/por-rol
# Devuelve cuántos usuarios hay por cada rol
@app.route('/api/reportes/por-rol', methods=['GET'])
def report_by_role():
    results = db.session.query(
        User.role,
        func.count(User.id).label('total')
    ).group_by(User.role).all()

    return jsonify([{
        'role':  role,
        'total': total
    } for role, total in results])

# ── Health check ──────────────────────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'servicio': 'ms-reportes'})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
