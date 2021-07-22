from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from ..database import Marca

from ..schemas import MarcaRequestModel
from ..schemas import MarcaResponseModel

from ..middleware import get_current_user

router = APIRouter(prefix='/marcas')

@router.post('', response_model=MarcaResponseModel)
async def crear_marca(marca: MarcaRequestModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        marca = Marca.create(
            nombre=marca.nombre
        )

        return marca

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('', response_model=List[MarcaResponseModel])
async def obtener_marcas(token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:
        
        marcas = Marca.select()

        return [marca for marca in marcas]

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('/{marca_id}', response_model=MarcaResponseModel)
async def obtener_marca_id(marca_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        marca_id = Marca.select().where(Marca.id == marca_id).first()

        if marca_id is None:
            raise HTTPException(status_code=404, detail='ID de marca no encontrada.')

        return marca_id

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")