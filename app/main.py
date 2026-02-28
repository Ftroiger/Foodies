from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.routers import auth, users, places, reviews, groups, favorites, cities

app = FastAPI(
    title="Foodies API",
    description="Plataforma de catálogo de bares, restaurantes y cafeterías",
    version="1.0.0",
)

add_cors_middleware(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(places.router)
app.include_router(reviews.router)
app.include_router(groups.router)
app.include_router(favorites.router)
app.include_router(cities.router)


@app.get("/")
def root():
    return {"message": "Bienvenido a Foodies API"}
