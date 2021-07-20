from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Nivel

from ..schemas import NivelResponseModel
from ..schemas import NivelRequestModel

router = APIRouter(prefix='/api/v1/niveles')

@router.post('', response_model=NivelResponseModel)
async def crear_nivel_de_usuario(nivel: NivelRequestModel):

    if Nivel.select().where(Nivel.tipo == nivel.tipo).exists():
        raise HTTPException(status_code=409, detail='El tipo de nivel de usuario ya se encuentra en uso.')

    nivel = Nivel.create(
        nombre=nivel.nombre,
        tipo=nivel.tipo
    )

    return nivel

@router.get('', response_model=List[NivelResponseModel])
async def obtener_nivel_de_usuarios():
    
    niveles = Nivel.select()

    return [nivel for nivel in niveles]

@router.get('/{nivel_id}', response_model=NivelResponseModel)
async def obtener_nivel_id(nivel_id: int):

    nivel_id = Nivel.select().where(Nivel.id == nivel_id).first()

    if nivel_id is None:
        raise HTTPException(status_code=404, detail='Nivel ID no encontrado.')

    return nivel_id