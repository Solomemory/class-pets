from fastapi import APIRouter

from app.api.v1.routes import auth, pets, points, rules, students

api_router = APIRouter()
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(students.router, tags=['students'])
api_router.include_router(pets.router, tags=['pets'])
api_router.include_router(points.router, tags=['points'])
api_router.include_router(rules.router, tags=['rules'])
