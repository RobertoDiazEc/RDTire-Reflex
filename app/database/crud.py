from sqlalchemy.orm import Session
from app.database import models
import hashlib


def get_user_by_username(db: Session, username: str) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()


def create_user(db: Session, user_in: dict) -> models.Usuario:
    password_hash = hashlib.sha256(user_in["password"].encode()).hexdigest()
    db_user = models.Usuario(
        username=user_in["username"],
        email=user_in["email"],
        password_hash=password_hash,
        role=user_in["role"],
    )
    db.add(db_user)
    db.flush()
    return db_user


def get_vehicles(db: Session) -> list[models.Vehiculo]:
    return db.query(models.Vehiculo).all()


def create_vehicle(db: Session, vehicle_in: dict) -> models.Vehiculo:
    db_vehicle = models.Vehiculo(**vehicle_in)
    db.add(db_vehicle)
    db.flush()
    return db_vehicle


def get_tires(db: Session) -> list[models.Tire]:
    return db.query(models.Tire).all()