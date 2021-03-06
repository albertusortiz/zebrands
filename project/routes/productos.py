from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from ..database import Producto, Usuario
from ..database import Marca
from ..database import SeguimientoUsuario

from ..schemas import ProductoRequestModel
from ..schemas import ProductoResponseModel
from ..schemas import ProductoRequestPutModel

from ..middleware import get_current_user

from ..services import enviar_correo_de_notificacion

router = APIRouter(prefix='/productos')

@router.post('', response_model=ProductoResponseModel)
async def crear_producto(producto: ProductoRequestModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:
    
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

        enviar_correo_de_notificacion("alberto.ortiz.vargas@gmail.com",
                                    str(token.get("username")), 
                                    "creo",
                                    "productos",
                                    str(producto.id))

        return producto

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('', response_model=List[ProductoResponseModel])
async def obtener_productos(page: int = 1, limit : int = 10):
    
    productos = Producto.select().paginate(page, limit)

    return [producto for producto in productos]

@router.get('/{producto_id}', response_model=ProductoResponseModel)
async def obtener_producto_id(producto_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        producto_id = Producto.select().where(Producto.id == producto_id).first()

        if producto_id is None:
            raise HTTPException(status_code=404, detail='Producto no encontrado.')

        return producto_id

    if token.get("nivel") == 2:

        producto_id = Producto.select().where(Producto.id == producto_id).first()

        if producto_id is None:
            raise HTTPException(status_code=404, detail='Producto no encontrado.')

        usuario_id = Usuario.select().where(Usuario.username == token.get("username")).first()

        if usuario_id is None:
            raise HTTPException(status_code=404, detail='Usuario no encontrado.')

        """
        Cuando un usuario haga login y visite un producto en particualar,
        esta visita quedara guardada en el modelo SeguimientoUsuario.
        """
        SeguimientoUsuario.create(
            usuario_id=usuario_id.id,
            producto_id=producto_id
        )

        return producto_id

    raise HTTPException(status_code=404, detail="Este usuario no pertenece a ningun tipo de nivel de usuario valido.")

@router.put('/{producto_id}', response_model=ProductoResponseModel)
async def actualizar_producto(producto_id: int, review_request: ProductoRequestPutModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        producto_id = Producto.select().where(Producto.id == producto_id).first()

        if producto_id is None:
            raise HTTPException(status_code=404, detail='Producto no encontrado.')

        producto_id.marca_id = review_request.marca_id
        producto_id.sku = review_request.sku
        producto_id.nombre = review_request.nombre
        producto_id.precio = review_request.precio
        producto_id.estatus = review_request.estatus

        producto_id.save()

        enviar_correo_de_notificacion("alberto.ortiz.vargas@gmail.com",
                                    str(token.get("username")), 
                                    "actualizo",
                                    "productos",
                                    str(producto_id.id))

        return producto_id

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.delete('/{producto_id}', response_model=ProductoResponseModel)
async def eliminar_un_producto(producto_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        producto_id = Producto.select().where(Producto.id == producto_id).first()

        if producto_id is None:
            raise HTTPException(status_code=404, detail='Producto no encontrado.')
        
        producto_id.delete_instance()

        enviar_correo_de_notificacion("alberto.ortiz.vargas@gmail.com",
                                    str(token.get("username")), 
                                    "elimino",
                                    "productos",
                                    str(producto_id.id))

        return producto_id

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")