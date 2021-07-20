from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Producto
from ..database import Usuario
from ..database import SeguimientoUsuario

from ..schemas import SeguimientoUsuariosRequestModel
from ..schemas import SeguimientoUsuariosResponseModel

router = APIRouter(prefix='/api/v1/seguimiento')

@router.post('', response_model=SeguimientoUsuariosResponseModel)
async def seguimiento_de_usuarios(seguimiento: SeguimientoUsuariosRequestModel):

    if Usuario.select().where(Usuario.id == seguimiento.usuario_id).first() is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    if Producto.select().where(Producto.id == seguimiento.producto_id).first() is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado')


    seguimiento = SeguimientoUsuario.create(
        usuario_id = seguimiento.usuario_id,
        producto_id = seguimiento.producto_id
    )

    return seguimiento

@router.get('', response_model=List[SeguimientoUsuariosResponseModel])
async def obtener_seguimiento_de_usuarios(page: int = 1, limit : int = 10):
    
    seguimientos = SeguimientoUsuario.select().paginate(page, limit)

    return [seguimiento for seguimiento in seguimientos]

@router.get('/{seguimiento_id}', response_model=SeguimientoUsuariosResponseModel)
async def obtener_seguimiento_id(seguimiento_id: int):

    seguimiento_id = SeguimientoUsuario.select().where(SeguimientoUsuario.id == seguimiento_id).first()

    if seguimiento_id is None:
        raise HTTPException(status_code=404, detail='Seguimiento de usuario no encontrado.')

    return seguimiento_id