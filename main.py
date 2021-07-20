from typing import List

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic.errors import NotNoneError

from database import Nivel
from database import Marca
from database import Usuario
from database import Producto
from database import SeguimientoUsuario

from database import database as connection

from schemas import NivelRequestModel, ProductoRequestPutModel
from schemas import NivelResponseModel

from schemas import MarcaRequestModel
from schemas import MarcaResponseModel

from schemas import UsuarioRequestModel
from schemas import UsuarioResponseModel
from schemas import UsuarioRequestPutModel

from schemas import ProductoRequestModel
from schemas import ProductoResponseModel
from schemas import ProductoValidator

from schemas import SeguimientoUsuariosRequestModel
from schemas import SeguimientoUsuariosResponseModel

app = FastAPI(title='Sistema de Catalogo para Administrar Productos',
            description='En este proyecto seremos capaces de gestionar usuarios y productos delimitando accesos con base al rol de cada usuario.',
            version='1')

@app.on_event('startup')
def startup():
    
    if connection.is_closed():
        connection.connect()

        print('Connecting...')

    connection.create_tables([Nivel, Marca, Usuario, Producto, SeguimientoUsuario])

@app.on_event('shutdown')
def shutdown():
    
    if not connection.is_closed():
        connection.close()

        print('Closing...')

@app.get('/')
async def inicio():
    return 'Hola mundo, desde un servidor FastAPI'

@app.post('/niveles', response_model=NivelResponseModel)
async def crear_nivel_de_usuario(nivel: NivelRequestModel):

    if Nivel.select().where(Nivel.tipo == nivel.tipo).exists():
        raise HTTPException(status_code=409, detail='El tipo de nivel de usuario ya se encuentra en uso.')

    nivel = Nivel.create(
        nombre=nivel.nombre,
        tipo=nivel.tipo
    )

    return nivel

@app.post('/marcas', response_model=MarcaResponseModel)
async def crear_marca(marca: MarcaRequestModel):

    marca = Marca.create(
        nombre=marca.nombre
    )

    return marca

@app.post('/usuarios', response_model=UsuarioResponseModel)
async def crear_usuario(usuario: UsuarioRequestModel):

    if Usuario.select().where(Usuario.username == usuario.username).exists():
        raise HTTPException(status_code=409, detail='El username ya se encuentra en uso.')

    if Nivel.select().where(Nivel.id == usuario.nivel_id).first() is None:
        raise HTTPException(status_code=404, detail="Nivel de usuario no encontrado")

    hash_password = Usuario.create_password(usuario.password)
    
    usuario = Usuario.create(
        nivel_id=usuario.nivel_id,
        username=usuario.username,
        password=hash_password,
        nombre_completo=usuario.nombre_completo,
        fecha_nacimiento=usuario.fecha_nacimiento,
        email=usuario.email,
        telefono=usuario.telefono,
        direccion=usuario.direccion
    )

    return usuario

@app.post('/productos', response_model=ProductoResponseModel)
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

@app.post('/seguimiento', response_model=SeguimientoUsuariosResponseModel)
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

@app.get('/niveles', response_model=List[NivelResponseModel])
async def obtener_nivel_de_usuarios():
    
    niveles = Nivel.select()

    return [nivel for nivel in niveles]

@app.get('/niveles/{nivel_id}', response_model=NivelResponseModel)
async def obtener_nivel_id(nivel_id: int):

    nivel_id = Nivel.select().where(Nivel.id == nivel_id).first()

    if nivel_id is None:
        raise HTTPException(status_code=404, detail='Nivel ID no encontrado.')

    return nivel_id

@app.get('/marcas', response_model=List[MarcaResponseModel])
async def obtener_marcas():
    
    marcas = Marca.select()

    return [marca for marca in marcas]

@app.get('/marcas/{marca_id}', response_model=MarcaResponseModel)
async def obtener_marca_id(marca_id: int):

    marca_id = Marca.select().where(Marca.id == marca_id).first()

    if marca_id is None:
        raise HTTPException(status_code=404, detail='ID de marca no encontrada.')

    return marca_id

@app.get('/usuarios', response_model=List[UsuarioResponseModel])
async def obtener_usuarios(page: int = 1, limit : int = 10):
    
    usuarios = Usuario.select().paginate(page, limit)

    return [usuario for usuario in usuarios]

@app.get('/usuarios/{usuario_id}', response_model=UsuarioResponseModel)
async def obtener_usuario_id(usuario_id: int):

    usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

    if usuario_id is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrada.')

    return usuario_id

@app.get('/productos', response_model=List[ProductoResponseModel])
async def obtener_productos(page: int = 1, limit : int = 10):
    
    productos = Producto.select().paginate(page, limit)

    return [producto for producto in productos]

@app.get('/productos/{producto_id}', response_model=ProductoResponseModel)
async def obtener_producto_id(producto_id: int):

    producto_id = Producto.select().where(Producto.id == producto_id).first()

    if producto_id is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado.')

    return producto_id

@app.get('/seguimiento', response_model=List[SeguimientoUsuariosResponseModel])
async def obtener_seguimiento_de_usuarios():
    
    seguimientos = SeguimientoUsuario.select()

    return [seguimiento for seguimiento in seguimientos]

@app.get('/seguimiento/{seguimiento_id}', response_model=SeguimientoUsuariosResponseModel)
async def obtener_seguimiento_id(seguimiento_id: int):

    seguimiento_id = SeguimientoUsuario.select().where(SeguimientoUsuario.id == seguimiento_id).first()

    if seguimiento_id is None:
        raise HTTPException(status_code=404, detail='Seguimiento de usuario no encontrado.')

    return seguimiento_id

@app.put('/usuarios/{usuario_id}', response_model=UsuarioResponseModel)
async def actualizar_usuario(usuario_id: int, review_request: UsuarioRequestPutModel):
    
    usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

    if usuario_id is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado.')

    usuario_id.username = review_request.username
    usuario_id.password = review_request.password
    usuario_id.nombre_completo = review_request.nombre_completo
    usuario_id.fecha_nacimiento = review_request.fecha_nacimiento
    usuario_id.email = review_request.email
    usuario_id.telefono = review_request.telefono
    usuario_id.direccion = review_request.direccion

    usuario_id.save()

    return usuario_id

@app.put('/productos/{producto_id}', response_model=ProductoResponseModel)
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

@app.delete('/usuarios/{usuario_id}', response_model=UsuarioResponseModel)
async def eliminar_un_usuario(usuario_id: int):
    
    usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

    if usuario_id is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado.')

    usuario_id.delete_instance()

    return usuario_id

@app.delete('/productos/{producto_id}', response_model=ProductoResponseModel)
async def eliminar_un_producto(producto_id: int):

    producto_id = Producto.select().where(Producto.id == producto_id).first()

    if producto_id is None:
        raise HTTPException(status_code=404, detail='Producto no encontrado.')
    
    producto_id.delete_instance()

    return producto_id