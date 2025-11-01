from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    schema_name = Column(String(100), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    usuarios = relationship("Usuario", back_populates="cliente")


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    cliente_id = Column(Integer, ForeignKey("public.clientes.id"), nullable=False)
    cliente = relationship("Cliente", back_populates="usuarios")


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    placa = Column(String(20), nullable=False, unique=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    ano = Column(Integer)
    tipo = Column(String(50))
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tires = relationship(
        "VehicleTire", back_populates="vehicle", cascade="all, delete-orphan"
    )


class Tire(Base):
    __tablename__ = "tires"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    size = Column(String(20))
    type = Column(String(50))
    season = Column(String(20))
    speed_rating = Column(String(5))
    load_index = Column(String(5))
    price = Column(Float)
    stock = Column(Integer, default=0)
    image_url = Column(String(255))


class VehicleTire(Base):
    __tablename__ = "vehicle_tires"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("tenant.vehiculos.id"), nullable=False)
    tire_id = Column(Integer, ForeignKey("tenant.tires.id"), nullable=False)
    position = Column(String(50), nullable=False)
    fecha_instalacion = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String(50))
    profundidad_actual = Column(Float)
    vehicle = relationship("Vehiculo", back_populates="tires")
    tire = relationship("Tire")
    history = relationship(
        "TireHistory", back_populates="vehicle_tire", cascade="all, delete-orphan"
    )


class TireHistory(Base):
    __tablename__ = "tire_history"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    vehicle_tire_id = Column(
        Integer, ForeignKey("tenant.vehicle_tires.id"), nullable=False
    )
    tipo_evento = Column(String(50))
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    notas = Column(String(500))
    profundidad_medida = Column(Float)
    vehicle_tire = relationship("VehicleTire", back_populates="history")


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))


class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    customer_id = Column(Integer, ForeignKey("tenant.customers.id"))
    total = Column(Float, nullable=False)
    payment_method = Column(String(50))
    customer = relationship("Customer")
    items = relationship(
        "SaleItem", back_populates="sale", cascade="all, delete-orphan"
    )


class SaleItem(Base):
    __tablename__ = "sale_items"
    __table_args__ = {"schema": "tenant"}
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("tenant.sales.id"), nullable=False)
    tire_id = Column(Integer, ForeignKey("tenant.tires.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_sale = Column(Float, nullable=False)
    sale = relationship("Sale", back_populates="items")
    tire = relationship("Tire")