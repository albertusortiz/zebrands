from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Producto

from ..schemas import ProductoRequestModel
from ..schemas import ProductoResponseModel
from ..schemas import ProductoRequestPutModel

router = APIRouter(prefix='/api/v1/productos')

@router.post('', response_model=ProductoResponseModel)
async def crear_producto(producto: ProductoRequestModel):
    
    if Producto.select().where(Producto.sku == producto.sku).exists():
        raise HTTPException(status_code=409, detail='Este SKU ya existe en el catálogo.')

    if Marca.select().where(Marca.id == producto.marca_id).first() is None:
        raise HTTPException(status_code=404, detail='Marca no encontrada.')

    producto = Producto.create(
        marca_id = producto.marca_id,
        sku = producto.sku,
        nombre = producto.nombre,
        precio = producto.precio,
        estatus = producto.estatus
    )

    return producto

@router.get('', response_model=List[ProductoResponseModel])
async def obtener_productos(page: int = 1, limit : int = 10):
    
    productos = Producto.select().paginate(page, limit)

    return [producto for producto in productos]

@router.get('/{producto_id}', response_model=ProductoResponseModel)
async def obtener_producto_id(producto_id: int):

    producto_id = Producto.select().where(Producto.id == producto_id).first()

    if producto_id is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado.')

    return producto_id

@router.put('/{producto_id}', response_model=ProductoResponseModel)
async def actualizar_producto(producto_id: int, review_request: ProductoRequestPutModel):

    producto_id = Producto.select().where(Producto.id == producto_id).first()

    if producto_id is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado.')

    producto_id.marca_id = review_request.marca_id
    producto_id.sku = review_request.sku
    producto_id.nombre = review_request.nombre
    producto_id.precio = review_request.precio
    producto_id.estatus = review_request.estatus

    producto_id.save()

    return producto_id

@router.delete('/{producto_id}', response_model=ProductoResponseModel)
async def eliminar_un_producto(producto_id: int):

    producto_id = Producto.select().where(Producto.id == producto_id).first()

    if producto_id is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado.')
    
    producto_id.delete_instance()

    return producto_id