from app.db.base import Base
from app.db.schema_upgrade import apply_schema_upgrade
from app.db.session import SessionLocal, engine
from app.seeds.seed_data import run_seed


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    apply_schema_upgrade(engine)
    with SessionLocal() as session:
        run_seed(session)
    print('Seed completed.')
