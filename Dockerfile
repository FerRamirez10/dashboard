# Usa una imagen base de Python ligera (Python 3.9, basado en Debian Buster)
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY . .

# Indica el puerto en el que la aplicación escuchará.
# Railway inyectará el valor de la variable de entorno PORT.
EXPOSE $PORT

# Define el comando que se ejecutará cuando el contenedor se inicie
# Este comando iniciará Gunicorn, apuntando a tu aplicación Dash
CMD ["gunicorn", "app.PY:app.server", "--bind", "0.0.0.0:$PORT", "--workers", "2"]