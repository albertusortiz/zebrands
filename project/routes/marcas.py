from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Marca

from ..schemas import MarcaRequestModel
from ..schemas import MarcaResponseModel

router = APIRouter(prefix='/api/v1/marcas')

@router.post('', response_model=MarcaResponseModel)
async def crear_marca(marca: MarcaRequestModel):

    marca = Marca.create(
        nombre=marca.nombre
    )

    return marca

@router.get('', response_model=List[MarcaResponseModel])
async def obtener_marcas():
    
    marcas = Marca.select()

    return [marca for marca in marcas]

@router.get('/{marca_id}', response_model=MarcaResponseModel)
async def obtener_marca_id(marca_id: int):

    marca_id = Marca.select().where(Marca.id == marca_id).first()

    if marca_id is None:
        raise HTTPException(status_code=404, detail='ID de marca no encontrada.')

    return marca_id