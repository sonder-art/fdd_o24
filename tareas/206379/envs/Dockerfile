# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala virtualenv
RUN pip install --no-cache-dir virtualenv

# Copia el archivo de requerimientos (requirements.txt) al contenedor
COPY requirements_pandas.txt .

# Crea un entorno virtual y activa el entorno
RUN virtualenv venv

# Instala los paquetes en el entorno virtual
RUN ./venv/bin/pip install --no-cache-dir -r requirements_pandas.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Define el comando por defecto para ejecutar la aplicación
CMD ["./venv/bin/python", "app.py"]