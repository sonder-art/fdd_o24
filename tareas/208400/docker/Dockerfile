# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código al contenedor
COPY . /app

# Comando por defecto: muestra el contenido de archivo_local.txt
CMD ["python", "app.py"]
