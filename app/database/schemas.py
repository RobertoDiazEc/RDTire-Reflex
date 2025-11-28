from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"

class UsuarioSchemaNuevo(BaseModel):
    username: str = Field(min_length=8, frozen=True)
    email: EmailStr = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password_hash:str 
    role: str 
    cliente_id: int 
    
class UsuarioSchemaEditar(BaseModel):
    username: str = Field(min_length=8, frozen=True)
    email: EmailStr = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    role: str 
     
class VehiculoSchemaNuevo(BaseModel):
    placa: str = Field(min_length=6, frozen=True)
    marca: str 
    modelo: str
    anio: int
    tipo: str
    odometro_actual: int
    tipo_combustible: str
    capacidad_tanque: int
    medida_tire: str
    numero_tire: int 

class VehiculoSchemaEditar(BaseModel):
    marca: str 
    modelo: str
    anio: int
    tipo: str
    odometro_actual: int
    tipo_combustible: str
    capacidad_tanque: int
    medida_tire: str
    numero_tire: int 

class TireSchemaNuevo(BaseModel):
    brand: str
    size: str
    dot: str
    type: str = Field(default="RADIAL")
    season: str = None
    speed_rating: str = None
    load_index: str = None
    price: float = 10
    stock: int = Field(default=1, maximum=4)
    image_url: str | None = None   

class TireSchemaEditar(BaseModel):
    brand: str
    size: str
    dot: str
    type: str = Field(default="RADIAL")
    season: str = None
    speed_rating: str = None
    load_index: str = None
    price: float = 10
    stock: int = 1
    image_url: str | None = None    
    asignado_a_vehiculo: bool = False  

class ClienteSchemaNuevo(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: EmailStr = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")    

class ClienteSchemaEditar(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: EmailStr = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

class VehicleTireSchemaNuevo(BaseModel):
    position: str
    fecha_instalacion: date = Field(default_factory=date.today)
    estado: str
    profundidad_actual: float = Field(minimum=0.0, maximum=19.0)
    odometro_actual: int = Field(default=0, nullable=False)
    presion_tire_actual: int = Field(default=0, nullable=False)      
        
class HistoryTireSchemaNuevo(BaseModel):
    tipo_evento: str
    fecha: date = Field(default_factory=date.today)
    notas: str
    profundidad_medida: float = Field(minimum=0.0, maximum=19.0)
    odometro_lectura: int = Field(default=0, nullable=False)
    presion_tire: int = Field(default=0, nullable=False)        