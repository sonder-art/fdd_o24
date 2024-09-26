# Usa una imagen base de Python 3.9 slim
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements_pandas.txt .

# Instala virtualenv
RUN python -m venv venv

# Activa el virtualenv y luego instala las dependencias
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements_pandas.txt

# Copia el código de la aplicación en el contenedor
COPY . .

# Activa virtualenv y define el comando por defecto para ejecutar la aplicación
CMD ["bash", "-c", ". venv/bin/activate && python app.py"]
