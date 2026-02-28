# Plataforma de Catálogo de Bares, Restaurantes y Cafeterías

## Esquema de Directorios — FastAPI

```
project-root/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # Punto de entrada, inicialización de FastAPI
│   ├── config.py                   # Variables de entorno, settings (Pydantic BaseSettings)
│   ├── database.py                 # Configuración de SQLAlchemy / conexión a DB
│   │
│   ├── models/                     # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── category.py
│   │   ├── review.py
│   │   ├── group.py
│   │   ├── group_member.py
│   │   ├── group_place.py
│   │   ├── favorite.py
│   │   └── city.py
│   │
│   ├── schemas/                    # Schemas Pydantic (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── group.py
│   │   ├── favorite.py
│   │   └── city.py
│   │
│   ├── routers/                    # Endpoints agrupados por dominio
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login, register, refresh token
│   │   ├── users.py                # Perfil, configuración
│   │   ├── places.py               # CRUD lugares, búsqueda, filtros
│   │   ├── reviews.py              # Crear/editar/eliminar reseñas
│   │   ├── groups.py               # CRUD grupos, miembros, lugares del grupo
│   │   ├── favorites.py            # Guardar/quitar favoritos
│   │   └── cities.py               # Listar ciudades, filtrar
│   │
│   ├── services/                   # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── place_service.py
│   │   ├── google_maps_service.py  # Integración con Google Places API
│   │   ├── review_service.py
│   │   ├── group_service.py
│   │   └── favorite_service.py
│   │
│   ├── dependencies/               # Dependencias inyectables
│   │   ├── __init__.py
│   │   ├── auth.py                 # get_current_user, verificar JWT
│   │   └── database.py             # get_db session
│   │
│   ├── utils/                      # Utilidades transversales
│   │   ├── __init__.py
│   │   ├── security.py             # Hashing, JWT, tokens
│   │   ├── pagination.py           # Paginación genérica
│   │   └── google_maps.py          # Helper para parsear respuestas de Google
│   │
│   └── middleware/
│       ├── __init__.py
│       └── cors.py
│
├── alembic/                        # Migraciones de base de datos
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_places.py
│   ├── test_reviews.py
│   ├── test_groups.py
│   └── test_favorites.py
│
├── .env                            # Variables de entorno (no commitear)
├── .env.example
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Lista de Alcances

### Fase 1 — MVP (Core)

**Autenticación y Usuarios**
- Registro con email y contraseña
- Login con JWT (access + refresh token)
- Perfil de usuario (ver y editar datos básicos, avatar)
- Selección de ciudad principal del usuario

**Catálogo de Lugares**
- Integración con Google Places API para obtener: nombre, dirección, horarios, fotos, puntuación de Google, coordenada geográfica y teléfono
- Listado de lugares con paginación
- Detalle de lugar con toda la información sincronizada desde Google
- Filtro por ciudad
- Filtro por categoría (bar, restaurante, cafetería)
- Búsqueda por nombre o dirección
- Sincronización periódica de datos de Google (cron job o trigger manual)

**Sistema de Puntuación Propio**
- Crear reseña con puntuación (1-5 estrellas) y comentario
- Editar y eliminar reseña propia
- Cálculo de rating promedio propio (independiente del de Google)
- Visualización de ambas puntuaciones (Google + plataforma)

---

### Fase 2 — Social & Grupos

**Grupos**
- Crear grupo con nombre, descripción e imagen
- Invitar usuarios al grupo (por email o username)
- Roles dentro del grupo: owner, admin, member
- Agregar lugares al grupo con nota opcional
- Listar lugares guardados dentro de un grupo
- Abandonar grupo / expulsar miembros (admin+)
- Grupos públicos vs privados

**Favoritos**
- Guardar lugar como favorito personal (independiente de grupos)
- Listar mis favoritos con filtros

---

### Fase 3 — Experiencia y Descubrimiento

**Filtros Avanzados**
- Filtro por rango de puntuación (propia y/o Google)
- Filtro por rango de precio
- Filtro por "abierto ahora" (basado en horarios de Google)
- Ordenar por: puntuación, distancia, más recientes, más reseñados

**Mapa Interactivo**
- Vista de mapa con marcadores de lugares (integración Google Maps JS)
- Clic en marcador para ver tarjeta resumen del lugar
- Filtrar directamente desde el mapa

**Contenido Enriquecido**
- Galería de fotos de Google en el detalle del lugar
- Los usuarios pueden subir fotos propias a sus reseñas

---

### Fase 4 — Crecimiento

**Notificaciones**
- Notificación cuando alguien agrega un lugar a un grupo compartido
- Notificación cuando invitan al usuario a un grupo

**Panel de Administración**
- Dashboard para gestionar lugares, usuarios y reseñas
- Moderar contenido reportado
- Estadísticas de uso (lugares más guardados, ciudades más activas)

**API Pública (opcional)**
- Endpoints públicos limitados para integración con terceros
- Rate limiting y API keys

---

### Fuera de Alcance (por ahora)
- Reservas o pedidos online
- Sistema de pagos
- App móvil nativa (se prioriza web responsive)
- Chat entre usuarios
- Integración con redes sociales para compartir
