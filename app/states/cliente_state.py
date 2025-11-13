import reflex as rx
import re
import sqlalchemy
from datetime import datetime
from sqlmodel import Field, select
import bcrypt
from app.database.db_rdtire import Cliente as ClienteL


from app.states.base_state import BaseState, Customer


    # nombre: str = Field(nullable=False)
    # ciudad: str = Field(nullable=False)
    # activo: bool = Field(default=True)
    # estado: str = Field(default="AC", max_length=2)
    # numero_vehiculos: Optional[int] = Field(default=1)
    # tipo_plan: Optional[str] = Field(default="BASICO", max_length=20)
    # fecha_creacion

class ClienteState(BaseState):
    useregistro: str = rx.LocalStorage("",sync= True)
    open_edit_customer_modal: bool = False
    nombre: str
    codigo_cliente: str
    ciudad: str
    username: str
    password: str
    confirm_password: str
    nombre_empresa: str
   

    