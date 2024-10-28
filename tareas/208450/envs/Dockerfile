# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Codigo para manejar ambientes y el codigo necesario
# Instala las dependencias del sistema necesarias para compilar extensiones en C/C++
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpython3-dev \
    build-essential \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*
    
# Instala virtualenv
RUN pip install --no-cache-dir virtualenv

# Crea un entorno virtual
RUN virtualenv /opt/venv

# Activa el entorno virtual
ENV PATH="/opt/venv/bin:$PATH"

# Copia los archivos de requerimientos 
COPY requirements_pandas.txt .

# Instala los requerimientos en el entorno virtual
RUN pip install --no-cache-dir -r requirements_pandas.txt

# Copia el resto de tu aplicación
COPY . .

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]