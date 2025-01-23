FROM python:3.11.0

# Instalar dependencias
WORKDIR /src/model
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando por defecto
CMD ["fastapi", "run", "app.py"]