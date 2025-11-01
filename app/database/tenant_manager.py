from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.models import Base, Cliente
from app.database.config import engine
import logging


def init_tenant_schema(schema_name: str):
    """Create all tables for a new tenant schema."""
    with engine.connect() as connection:
        try:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
            bind_engine = engine.execution_options(
                schema_translate_map={"tenant": schema_name}
            )
            Base.metadata.create_all(
                bind=bind_engine,
                tables=[
                    table
                    for table in Base.metadata.tables.values()
                    if table.schema == "tenant"
                ],
            )
            connection.commit()
            logging.info(f"Schema '{schema_name}' and tables created successfully.")
        except Exception as e:
            connection.rollback()
            logging.exception(f"Failed to create schema '{schema_name}': {e}")
            raise


def create_tenant(db: Session, nombre_cliente: str) -> Cliente:
    """Create a new client and its corresponding schema."""
    schema_name = nombre_cliente.lower().replace(" ", "_").replace("-", "_")
    if db.query(Cliente).filter_by(schema_name=schema_name).first():
        raise ValueError(f"Schema '{schema_name}' already exists.")
    new_cliente = Cliente(nombre=nombre_cliente, schema_name=schema_name)
    db.add(new_cliente)
    db.flush()
    init_tenant_schema(schema_name)
    return new_cliente


def list_all_tenants(db: Session) -> list[Cliente]:
    """List all active tenants."""
    return db.query(Cliente).filter_by(activo=True).all()


def get_tenant_by_id(db: Session, cliente_id: int) -> Cliente | None:
    """Get a tenant by its ID."""
    return db.query(Cliente).filter_by(id=cliente_id).first()


def get_schema_for_client(db: Session, cliente_id: int) -> str | None:
    """Get the schema name for a given client ID."""
    cliente = get_tenant_by_id(db, cliente_id)
    return cliente.schema_name if cliente else None


def delete_tenant(db: Session, cliente_id: int):
    """Delete a tenant and its schema."""
    cliente = get_tenant_by_id(db, cliente_id)
    if not cliente:
        raise ValueError("Tenant not found.")
    schema_name = cliente.schema_name
    with engine.connect() as connection:
        try:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE'))
            db.delete(cliente)
            connection.commit()
            logging.info(
                f"Schema '{schema_name}' and tenant '{cliente.nombre}' deleted."
            )
        except Exception as e:
            connection.rollback()
            logging.exception(f"Failed to delete schema '{schema_name}': {e}")
            raise