# Foodies API

Plataforma de catálogo de bares, restaurantes y cafeterías.

## Requisitos

- Python 3.12+
- PostgreSQL 16+
- Google Maps API Key

## Instalación local

```bash
# Crear entorno virtual
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## Documentación API

Una vez corriendo el servidor, visitar:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
