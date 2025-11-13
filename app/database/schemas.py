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

class TireSchemaNuevo(BaseModel):
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

      
        