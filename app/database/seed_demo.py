from app.database.config import get_db
from app.database.init_db import init_database, seed_demo_client


def main():
    print("Inicializando base de datos...")
    init_database()
    print("Base de datos inicializada.")
    with get_db() as db:
        print("Creando cliente de demostración 'REDx Soluciones'...")
        seed_demo_client(db)
        print("Cliente de demostración creado.")


if __name__ == "__main__":
    main()