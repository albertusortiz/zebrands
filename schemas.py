from datetime import date

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

class UsuarioRequestModel(BaseModel):
    nivel_id: int
    username: str
    password: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    email: str
    telefono: str
    direccion: str

    @validator('nivel_id')
    def nivel_id_validator(cls, nivel_id):
        if nivel_id < 9 or nivel_id > 10:
            raise ValueError('Nivel de usuario invalido.')

        return nivel_id

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