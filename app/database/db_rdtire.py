import reflex as rx
import sqlalchemy


from typing import List, Optional
from sqlmodel import Field, Relationship
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)
 
#   nombre: str = Field(nullable=False)
#     apellido: str = Field(nullable=False)
#     email: str = Field(nullable=False)
#     celular: str = Field(nullable=False)
#     ciudad: str = Field(nullable=False)
#     username: str = Field(nullable=False, index=True)
#     password: str = Field(nullable=False)
#     estado: str = Field(default="AC", max_length=2)

class Cliente(rx.Model, table=True):
    nombre: str = Field(nullable=False)
    ciudad: str = Field(nullable=False)
    activo: bool = Field(default=True)
    estado: str = Field(default="AC", max_length=2)
    codigo_cliente: str = Field(nullable=False, unique=True)
    numero_vehiculos: Optional[int] = Field(default=1)
    tipo_plan: Optional[str] = Field(default="BASICO", max_length=20)
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    usuario: List['Usuario'] = Relationship(
        back_populates="cliente"
    )
    vehiculo: List['Vehiculo'] = Relationship(
        back_populates="cliente"
    )
    tire: List['Tire'] = Relationship(
        back_populates="cliente"
    )
    tire_history: List['TireHistory'] = Relationship(
        back_populates="cliente"
    )


class Usuario(rx.Model, table=True):
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, index=True)
    password_hash:str = Field(nullable=False)
    role: str = Field(nullable=False, default="Usuario Técnico")
    activo: bool = Field(default=True)    
    estado: str = Field(default="AC", max_length=2)
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    update_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    cliente_id: int = Field(default=None, foreign_key='cliente.id')
    cliente: Cliente = Relationship(back_populates="usuario")    
    
class Roles(rx.Model, table=True):
    nombre: str = Field(nullable=False, unique=True)
    descripcion: Optional[str] = None 

class InventoryAdjustment(rx.Model, table=True):
    timestamp: str
    reason: str
    amount: int

class Cuenta_temporal(rx.Model, table=True):
    usuario_temp: str = Field(nullable=False, unique=True)
    clave_temp: Optional[str] = None    
    email_evio: Optional[str] = None
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    fecha_expiracion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )


class Vehiculo(rx.Model, table=True):
    placa: str = Field(nullable=False, unique=True)
    marca: str = Field(nullable=False)
    modelo: str = Field(nullable=False)
    anio: Optional[int] = 2000
    tipo: str = Field(nullable=False, default="CAMIONETA")
    estado: str = Field(default="AC", max_length=2)
    creado_por: Optional[str] = None
    fecha_registro: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    tires: List['VehicleTire'] = Relationship(
        back_populates="vehicle",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    cliente_id: int = Field(default=None, foreign_key='cliente.id')
    cliente: Cliente = Relationship(back_populates="vehiculo")   


class Tire(rx.Model, table=True):
    brand: str = Field(nullable=False, index=True)
    size: str = Field(nullable=False, index=True)
    dot: str = Field(nullable=False)
    model: Optional[str] = None
    type: Optional[str] = None
    season: Optional[str] = None
    speed_rating: Optional[str] = None
    load_index: Optional[str] = None
    price: Optional[float] = 1.0
    stock: Optional[int] = 1
    asignado_a_vehiculo: bool = False
    estado: str = Field(default="AC", max_length=2)
    image_url: Optional[str] = None
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    cliente_id: int = Field(default=None, foreign_key='cliente.id')
    cliente: Cliente = Relationship(back_populates="tire")
    vehicle_tires: List['VehicleTire'] = Relationship(
        back_populates="tire")
    saleitems: List['SaleItem'] = Relationship(
        back_populates="tire")


class VehicleTire(rx.Model, table=True):
    vehicle_id: int = Field(foreign_key="vehiculo.id")
    position: str = Field(nullable=False)
    fecha_instalacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    estado: Optional[str] = None
    profundidad_actual: Optional[float] = None
    vehicle: 'Vehiculo' = Relationship(back_populates="tires")
    tire_id: int = Field(foreign_key="tire.id")
    tire: 'Tire' = Relationship(back_populates="vehicle_tires")
    tirehistory: List['TireHistory'] = Relationship(
        back_populates="vehicletire",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )



class TireHistory(rx.Model, table=True):
    vehicletireid: int = Field(foreign_key="vehicletire.id")
    tipo_evento: Optional[str] = None
    fecha: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    notas: Optional[str] = None
    profundidad_medida: Optional[float] = None
    realizador: Optional[str] = None
    vehicletire: 'VehicleTire' = Relationship(back_populates="tirehistory")
    cliente_id: int = Field(default=None, foreign_key='cliente.id')
    cliente: Cliente = Relationship(back_populates="tire_history")


class Customer(rx.Model, table=True):
    name: str = Field(nullable=False)
    email: Optional[str] = None
    phone: Optional[str] = None
    direccion: Optional[str] = None
    ruc_cedula: Optional[int] = None
    estado: str = Field(default="AC", max_length=2)
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )   


class Sale(rx.Model, table=True):
    timestamp: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    customer_id: int = Field(foreign_key="customer.id")
    total: float = Field(nullable=False)
    payment_method: Optional[str] = None
    customer: 'Customer' = Relationship()
    items: List['SaleItem'] = Relationship(
        back_populates="sale",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    


class SaleItem(rx.Model, table=True):
    sale_id: int = Field(foreign_key="sale.id")
    tire_id: int = Field(foreign_key="tire.id")
    quantity: int = Field(nullable=False)
    price_at_sale: float = Field(nullable=False)
    sale: 'Sale' = Relationship(back_populates="items")
    tire: 'Tire' = Relationship(back_populates="saleitems")
   
