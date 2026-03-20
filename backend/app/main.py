from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.schema_upgrade import apply_schema_upgrade
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # MVP 阶段直接创建表，后续可切换 Alembic 迁移。
    Base.metadata.create_all(bind=engine)
    apply_schema_upgrade(engine)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get('/health')
def health_check() -> dict[str, str]:
    return {'status': 'ok'}
