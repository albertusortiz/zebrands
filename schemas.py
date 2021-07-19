from datetime import date
from typing import Optional
from pydantic import validator
from pydantic import BaseModel

class UsuarioBaseModel(BaseModel):
    nivel_id: int
    username: str
    password: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    email: str
    telefono: str
    direccion: str

    @validator('nivel_id')
    def nivel_usuario_validator(cls, nivel_id):
        if nivel_id < 9 or nivel_id > 10:
            raise ValueError('Nivel de usuario invalido.')

        return nivel_id