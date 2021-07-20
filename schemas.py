from datetime import date
from datetime import datetime

from typing import Any
from typing import Optional
from peewee import ModelSelect

from pydantic import validator
from pydantic import BaseModel

from peewee import ModelSelect

from pydantic.utils import GetterDict


class PeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class NivelRequestModel(BaseModel):
    nombre: str
    tipo: int

class NivelResponseModel(BaseModel):
    id: int
    nombre: str
    tipo: int

    class Config:
        orm_mode = True
        getter_dict = PeweeGetterDict

class MarcaRequestModel(BaseModel):
    nombre: str

class MarcaResponseModel(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
        getter_dict = PeweeGetterDict

class UsuarioRequestModel(BaseModel):
    nivel_id: int
    username: str
    password: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    email: str
    telefono: str
    direccion: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 8 or len(username) > 20:
            raise ValueError('La longitud debe encontrarse entre 8 y 20 caracteres.')

        return username

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 8 or len(password) > 50:
            raise ValueError('El password debe tener entre 8 y 50 caracteres.')

        return password

    @validator('nombre_completo')
    def nombre_completo_validator(cls, nombre_completo):
        if len(nombre_completo) < 8 or len(nombre_completo) > 50:
            raise ValueError('El nombre completo debe tener entre 3 y 100 caracteres.')

        return nombre_completo

    @validator('email')
    def email_validator(cls, email):
        if len(email) > 50:
            raise ValueError('El email no puede tener más de 50 caracteres.')

        return email

    @validator('telefono')
    def telefono_validator(cls, telefono):
        if len(telefono) > 15:
            raise ValueError('El telefóno no puede tener más de 15 digitós.')

        return telefono

class UsuarioResponseModel(BaseModel):
    id: int
    nivel_id: int
    username: str
    fecha_creacion: date

    class Config:
        orm_mode = True
        getter_dict = PeweeGetterDict

class ProductoRequestModel(BaseModel):
    marca_id: int
    sku: str
    nombre: str
    precio: float
    estatus: bool

    @validator('sku')
    def sku_validator(cls, sku):
        if len(sku) < 8 or len(sku) > 12:
            raise ValueError('SKU invalido.')

        return sku

    @validator('nombre')
    def nombre_validator(cls, nombre):
        if len(nombre) > 150:
            raise ValueError('El nombre no puede tener más de 150 caracteres.')

        return nombre

    @validator('precio')
    def precio_validator(cls, precio):
        if precio < 0:
            raise ValueError('El valor debe ser positivo.')

        return precio

    @validator('estatus')
    def estatus_validator(cls, estatus):
        if estatus < 0 or estatus > 1:
            raise ValueError('El estatus solo es ACTIVO[1] o INACTIVO[0].')

        return estatus

class ProductoResponseModel(BaseModel):
    id: int
    marca_id: int
    sku: str
    nombre: str
    precio: float
    fecha_alta: datetime
    estatus: bool

    class Config:
        orm_mode = True
        getter_dict = PeweeGetterDict

class SeguimientoUsuariosRequestModel(BaseModel):
    usuario_id: int
    producto_id: int

class SeguimientoUsuariosResponseModel(BaseModel):
    id: int
    usuario_id: int
    producto_id: int
    fecha_visita: datetime

    class Config:
        orm_mode = True
        getter_dict = PeweeGetterDict