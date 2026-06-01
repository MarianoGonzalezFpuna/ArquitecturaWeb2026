# Usamos Python 3.11 liviano
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el requirements para aprovechar cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 5001
EXPOSE 5001

# Comando para arrancar con gunicorn (servidor de producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
