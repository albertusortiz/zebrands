from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from ..database import Nivel

from ..schemas import NivelResponseModel
from ..schemas import NivelRequestModel

from ..middleware import get_current_user

router = APIRouter(prefix='/niveles')

@router.post('', response_model=NivelResponseModel)
async def crear_nivel_de_usuario(nivel: NivelRequestModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        nivel = Nivel.create(
            nombre=nivel.nombre,
            tipo=nivel.tipo
        )

        return nivel

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('', response_model=List[NivelResponseModel])
async def obtener_nivel_de_usuarios(token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:
        
        niveles = Nivel.select()

        return [nivel for nivel in niveles]

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('/{nivel_id}', response_model=NivelResponseModel)
async def obtener_nivel_id(nivel_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        nivel_id = Nivel.select().where(Nivel.id == nivel_id).first()

        if nivel_id is None:
            raise HTTPException(status_code=404, detail='Nivel ID no encontrado.')

        return nivel_id

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")