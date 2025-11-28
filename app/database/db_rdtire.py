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
    tirehistory: List['TireHistory'] = Relationship(
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
    tirehistory: List['TireHistory'] = Relationship(
        back_populates="usuario"
    )
    usuarioinsp: List['VehiculoInspection'] = Relationship(
        back_populates="inspector"
    )

class ConfiCuenta(rx.Model, table=True):
    tipo: str = Field(nullable=False, index=True, max_length=3)
    km_rotacion: int = Field(default=10000)
    tipo_combustible: str = Field(default="Diesel", nullable=False, max_length=20)
    tipo_presion: str = Field(default="PSI", nullable=False, max_length=3)
    ref_logo: str = Field(nullable=False, max_length=400)
    tiempo_app: int = Field(default=30)
    tiempo_user: int = Field(default=15)
    activo: bool = Field(default=True)
    iva_sri: int = Field(default=15)
    cliente_id: int = Field(nullable=False, index=True)
    cliente: str = Field(nullable=False, max_length=100)
    

class TireEventApp(rx.Model, table=True):
    tipo: str = Field(nullable=False, index=True, max_length=3)
    code: str = Field(nullable=False, unique=True, max_length=50)
    nombre: str = Field(nullable=False, max_length=100)
    variable: bool = False   
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )

class Roles(rx.Model, table=True):
    nombre: str = Field(nullable=False, unique=True)
    descripcion: Optional[str] = None 

class Menu(rx.Model, table=True):
    nombre: str = Field(nullable=False, unique=True)
    icon: Optional[str] = None
    orden: Optional[int] = None

class Menus_roles(rx.Model, table=True):
    menu: str = Field(nullable=False)
    rol: str = Field(nullable=False)
    icon: Optional[str] = None
    orden: Optional[int] = None 
    path: Optional[str] = None

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
    odometro_actual: int = Field(default=0, nullable=False)
    tipo_combustible: str = Field(default="Diesel", nullable=False)
    capacidad_tanque: int = 10
    medida_tire: str = Field(default="215/75R17.5", nullable=False)
    numero_tire: int = Field(default=4, nullable=False) 
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
    vehicleinsp: List['VehiculoInspection'] = Relationship(
        back_populates="vehiculo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Tire(rx.Model, table=True):
    brand: str = Field(nullable=False, index=True)
    size: str = Field(nullable=False, index=True)
    dot: str = Field(nullable=False)
    model: Optional[str] = None
    type: Optional[str] = "RADIAL"
    season: Optional[str] = None
    speed_rating: Optional[str] = None
    load_index: Optional[str] = None
    price: Optional[float] = 1.0
    stock: Optional[int] = 1
    asignado_a_vehiculo: bool = False
    estado: str = Field(default="INV", max_length=3, nullable=False)
    image_url: Optional[str] = None
    fecha_creacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    fecha_actualizacion: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
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
    profundidad_actual: float = Field(default=0.0, nullable=False)
    odometro_actual: int = Field(default=0, nullable=False)
    presion_tire_actual: int = Field(default=0, nullable=False)
    vehicle: 'Vehiculo' = Relationship(back_populates="tires")
    tire_id: int = Field(foreign_key="tire.id")
    tire: 'Tire' = Relationship(back_populates="vehicle_tires")
    tirehistory: List['TireHistory'] = Relationship(
        back_populates="vehicletire",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )    

class VehiculoInspection(rx.Model, table=True):
    vehiculo_id: int = Field(foreign_key="vehiculo.id")
    fecha: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={'server_default': sqlalchemy.func.now()},
        nullable=False,
    )
    odometro: int = Field(default=0, nullable=False)
    inspector_id: int = Field(foreign_key="usuario.id")
    estado_general: str = Field(default="APTO", max_length=20)
    notas: Optional[str] = None
    vehiculo: Vehiculo = Relationship(back_populates="vehicleinsp")
    inspector: Usuario = Relationship(back_populates="usuarioinsp")


class TireHistory(rx.Model, table=True):
    vehicletireid: int = Field(foreign_key="vehicletire.id")
    tipo_evento: Optional[str] = Field(default="INSPECCION")
    fecha: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False,
    )
    notas: Optional[str] = None
    profundidad_medida: float = Field(default=0.0, nullable=False)
    odometro_lectura: int = Field(default=0, nullable=False)
    presion_tire: int = Field(default=0, nullable=False)
    realizador: Optional[str] = None
    estado_visual: Optional[str] = Field(
        default=None,
        nullable=True,
        # p.ej: "Cortes,grietas;Desgaste irregular"
        # o JSON si luego quieres parsear mejor
    ) 
    criticidad: Optional[str] = Field(
        default="OK",
        max_length=10,  # OK / OBS / CRITICA
        nullable=False,
    )
    # Para ROTACION / MONTAJE / DESMONTAJE (posición vieja/nueva, o posición al desmontar)
    posicion_anterior: Optional[str] = None
    posicion_nueva: Optional[str] = None

    # Para BAJA / DESMONTAJE
    motivo_baja: Optional[str] = None  # p.ej. "Desgaste", "Daño irreparable", "Corte lateral"

    # Para REPARACION
    tipo_reparacion: Optional[str] = None   # p.ej. "Parche interno", "Reencauche"
    costo_reparacion: Optional[float] = None
    vehicletire: 'VehicleTire' = Relationship(back_populates="tirehistory")
    cliente_id: int = Field(default=None, foreign_key='cliente.id')
    cliente: Cliente = Relationship(back_populates="tirehistory")
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Usuario = Relationship(back_populates="tirehistory")


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
   
