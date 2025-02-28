# Usa una imagen oficial de Python
FROM python:3.12

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instala las dependencias antes de copiar el código fuente
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ahora copia el resto del código fuente
COPY . .

# Expone el puerto si es necesario
EXPOSE 8000

# Usa el comando CMD para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
