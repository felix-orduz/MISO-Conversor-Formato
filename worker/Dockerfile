# Usamos una imagen base de Python
FROM python:3.10.11

# Instalar dependencias y FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .

# Instalar las bibliotecas de Python requeridas
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Comando para iniciar tu aplicación
CMD ["celery", "-A", "app:celery_app", "worker", "--loglevel=info"]
