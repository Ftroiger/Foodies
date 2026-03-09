# Configuración de Base de Datos y Alembic

## 1. Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/foodies

SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

APP_NAME=Foodies API
DEBUG=False
```

La clase `Settings` en `app/config.py` usa `python-dotenv` para cargar estas variables automáticamente:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ...
```

> **Importante:** `load_dotenv()` busca el archivo `.env` en el directorio de trabajo actual. Asegúrate de ejecutar los comandos desde `Foodies/Foodies/` o de colocar el `.env` en esa carpeta.

---

## 2. Conexión a la Base de Datos

### Opción A: PostgreSQL local

1. Tener PostgreSQL instalado y corriendo en el puerto `5432`.
2. Crear la base de datos:

```sql
CREATE DATABASE foodies;
```

3. Configurar la `DATABASE_URL` en el `.env`:

```env
DATABASE_URL=postgresql+psycopg2://<usuario>:<contraseña>@localhost:5432/foodies
```

### Opción B: Docker Compose

Levantar el servicio de base de datos definido en `docker-compose.yml`:

```bash
docker-compose up -d db
```

Esto crea un contenedor PostgreSQL 16 con:
- **Usuario:** `user`
- **Contraseña:** `password`
- **Base de datos:** `foodies`
- **Puerto:** `5432`

Para esta opción, la `DATABASE_URL` sería:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/foodies
```

---

## 3. Estructura de Archivos Relevantes

```
Foodies/
├── alembic.ini            # Configuración de Alembic
├── alembic/
│   ├── env.py             # Entorno de migraciones (lee DATABASE_URL desde Settings)
│   ├── script.py.mako     # Template para archivos de migración
│   └── versions/          # Archivos de migración generados
├── app/
│   ├── config.py          # Clase Settings (python-dotenv + os.getenv)
│   ├── database.py        # Engine y SessionLocal de SQLAlchemy
│   └── models/            # Modelos SQLAlchemy
├── .env                   # Variables de entorno (NO subir al repositorio)
├── docker-compose.yml
└── requirements.txt
```

---

## 4. Comandos de Alembic

### Requisitos previos

```bash
pip install -r requirements.txt
```

Todos los comandos se ejecutan desde el directorio raíz del proyecto (`Foodies/Foodies/`).

### Generar una migración automática

Detecta cambios en los modelos SQLAlchemy y genera un script de migración:

```bash
alembic revision --autogenerate -m "descripción del cambio"
```

Ejemplo:

```bash
alembic revision --autogenerate -m "crear tablas iniciales"
```

El archivo generado se guarda en `alembic/versions/`.

### Aplicar todas las migraciones pendientes

```bash
alembic upgrade head
```

### Aplicar una migración específica

```bash
alembic upgrade <revision_id>
```

### Revertir la última migración

```bash
alembic downgrade -1
```

### Revertir todas las migraciones

```bash
alembic downgrade base
```

### Ver el historial de migraciones

```bash
alembic history --verbose
```

### Ver la migración actual aplicada

```bash
alembic current
```

### Ver las migraciones pendientes

```bash
alembic heads
```

---

## 5. Flujo de Trabajo Típico

1. **Modificar un modelo** en `app/models/`.
2. **Generar la migración:**

   ```bash
   alembic revision --autogenerate -m "agregar campo X a tabla Y"
   ```

3. **Revisar el archivo generado** en `alembic/versions/` para verificar que los cambios son correctos.
4. **Aplicar la migración:**

   ```bash
   alembic upgrade head
   ```

---

## 6. Solución de Problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `password authentication failed for user "user"` | Credenciales incorrectas en `DATABASE_URL` | Verificar usuario y contraseña en el `.env` |
| `could not connect to server` | PostgreSQL no está corriendo | Iniciar el servicio o levantar Docker con `docker-compose up -d db` |
| `database "foodies" does not exist` | La base de datos no fue creada | Ejecutar `CREATE DATABASE foodies;` en psql |
| `Target database is not up to date` | Hay migraciones pendientes | Ejecutar `alembic upgrade head` |
| `No changes detected` | Los modelos no tienen cambios nuevos | Verificar que los modelos estén importados en `alembic/env.py` |
