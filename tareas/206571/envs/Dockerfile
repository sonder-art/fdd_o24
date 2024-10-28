# Usa una imagen base de Python
FROM python:3.9-slim

# Actualiza el sistema e instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libpng-dev \
    libjpeg-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos primero
COPY requirements_pandas.txt .

# Instala virtualenv
RUN pip install --no-cache-dir virtualenv

# Crea un entorno virtual
RUN virtualenv venv

# Instala las dependencias dentro del entorno virtual
RUN ./venv/bin/pip install --no-cache-dir -r requirements_pandas.txt

# Copia el resto de la aplicación
COPY . .

# Comando por defecto al ejecutar el contenedor
CMD ["./venv/bin/python", "app.py"]
