from sqlalchemy.orm import Session
from app.database import crud, models
from app.database.config import engine
from app.database.tenant_manager import create_tenant


def init_database():
    """Create the public schema and initial tables."""
    models.Base.metadata.create_all(
        bind=engine, tables=[models.Base.metadata.tables["public.clientes"]]
    )


def seed_demo_client(db: Session):
    """Create and seed the demo client 'REDx Soluciones'."""
    client_name = "REDx Soluciones"
    tenant = db.query(models.Cliente).filter_by(nombre=client_name).first()
    if tenant:
        print(f"Tenant '{client_name}' already exists.")
        return
    new_tenant = create_tenant(db, client_name)
    print(
        f"Tenant '{new_tenant.nombre}' with schema '{new_tenant.schema_name}' created."
    )
    from app.database.config import get_tenant_db

    with get_tenant_db(new_tenant.schema_name) as tenant_db:
        users = [
            {
                "username": "admin@redx.com",
                "email": "admin@redx.com",
                "password": "admin123",
                "role": "Administrador",
            },
            {
                "username": "usuario@redx.com",
                "email": "usuario@redx.com",
                "password": "usuario123",
                "role": "Usuario Administrador",
            },
            {
                "username": "tecnico@redx.com",
                "email": "tecnico@redx.com",
                "password": "tecnico123",
                "role": "Usuario Técnico",
            },
        ]
        for user_data in users:
            crud.create_user(tenant_db, user_data)
        tenant_db.commit()
        print(f"Created {len(users)} users for tenant '{new_tenant.nombre}'.")