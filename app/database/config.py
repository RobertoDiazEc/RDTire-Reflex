import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/rdtire_db"
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database session for the public schema."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_tenant_db(tenant_schema: str):
    """Get a database session for a specific tenant schema."""
    if not tenant_schema:
        raise ValueError("Tenant schema must be provided.")
    connectable = engine.execution_options(
        schema_translate_map={"tenant": tenant_schema}
    )
    db = SQLAlchemySession(bind=connectable, autocommit=False, autoflush=False)
    try:
        yield db
    finally:
        db.close()