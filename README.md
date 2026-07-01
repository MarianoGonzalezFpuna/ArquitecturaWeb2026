# 🌐 ArquitecturaWeb2026 – Microservicios con Docker

**Facultad Politécnica – Universidad Nacional de Asunción**  
**Materia:** Arquitectura WEB
**Profesor:** Rodrigo Benítez  
**Integrantes:** Mariano González - 5.027.858
                 Tiara Caccuri  - 7.213.555

---

## 📌 Descripción

Aplicación web de gestión de usuarios implementada con arquitectura de **microservicios**, donde cada operación principal es ejecutada por un servicio independiente corriendo en un contenedor **Docker**, desplegado en **Render** con base de datos **Supabase (PostgreSQL)**.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│         App Principal (Flask + UI)              │
│     https://arquitecturaweb2026.onrender.com    │
└────────┬──────────────┬────────────────┬────────┘
         │              │                │
         ▼              ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ ms-consulta │  │ ms-insercion│  │ ms-reportes │
│  (Docker)   │  │  (Docker)   │  │  (Docker)   │
│  GET users  │  │  POST/PUT/  │  │  Reportes   │
│             │  │  DELETE     │  │  estadístic │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
               ┌────────────────┐
               │    Supabase    │
               │  (PostgreSQL)  │
               └────────────────┘
```

La app principal **no accede directamente a la base de datos** — delega todas las operaciones a los microservicios correspondientes.

---

## 🔗 URLs de los Servicios

| Servicio | URL | Descripción |
|----------|-----|-------------|
| App Principal | https://arquitecturaweb2026.onrender.com | Interfaz web principal |
| ms-consulta | https://ms-consulta.onrender.com | Consulta de usuarios |
| ms-insercion | https://ms-insercion.onrender.com | Inserción, edición y eliminación |
| ms-reportes | https://ms-reportes-87pa.onrender.com | Reportes estadísticos |

---

## 📦 Microservicios

### ms-consulta
Responsable de todas las **consultas** de usuarios.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/usuarios` | Retorna todos los usuarios |
| GET | `/api/usuarios/<id>` | Retorna un usuario por ID |
| GET | `/health` | Estado del servicio |

### ms-insercion
Responsable de **inserción, actualización y eliminación** de usuarios.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/usuarios` | Crea un nuevo usuario |
| PUT | `/api/usuarios/<id>` | Actualiza un usuario |
| DELETE | `/api/usuarios/<id>` | Elimina un usuario |

### ms-reportes
Responsable de los **reportes estadísticos**.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/reportes/por-ciudad` | Usuarios agrupados por ciudad |
| GET | `/api/reportes/estado` | Usuarios activos vs inactivos |
| GET | `/api/reportes/por-rol` | Usuarios agrupados por rol |

---

## 🗂️ Estructura del Repositorio

```
ArquitecturaWeb2026/
├── flask-crud-sqlite-main/     # App principal con UI
│   ├── app.py                  # Rutas Flask (delega a microservicios)
│   ├── requirements.txt
│   ├── templates/
│   │   ├── index.html
│   │   ├── add_user.html
│   │   └── edit_user.html
│   └── static/
│       └── style.css
├── ms-consulta/                # Microservicio de consulta
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── ms-insercion/               # Microservicio de inserción
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── ms-reportes/                # Microservicio de reportes
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| Python + Flask | Backend de cada microservicio |
| Docker | Contenedor de cada microservicio |
| Render | Plataforma de despliegue |
| Supabase (PostgreSQL) | Base de datos compartida |
| HTML + CSS | Frontend de la app principal |

---

## 🗄️ Modelo de Datos

```sql
CREATE TABLE "user" (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    city    VARCHAR(120) NOT NULL,
    contact VARCHAR(100) NOT NULL,
    email   VARCHAR(150) NOT NULL DEFAULT '',
    role    VARCHAR(50)  NOT NULL DEFAULT 'Usuario',
    status  VARCHAR(20)  NOT NULL DEFAULT 'Activo'
);
```

---

## ✅ Cumplimiento del Tema 1 – Microservicios

| Requisito | Estado |
|-----------|--------|
| Al menos 2 consultas como microservicio | ✅ `GET /api/usuarios` y `GET /api/usuarios/<id>` |
| Al menos 1 inserción como microservicio | ✅ `POST /api/usuarios` |
| Servicios en contenedor Docker | ✅ Cada microservicio tiene su propio `Dockerfile` |
| Mínimo 3 microservicios | ✅ ms-consulta, ms-insercion, ms-reportes |

---
