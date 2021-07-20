from fastapi import FastAPI
from fastapi import HTTPException

from database import Nivel
from database import Marca
from database import Usuario
from database import Producto
from database import SeguimientoUsuario

from database import database as connection

from schemas import NivelRequestModel
from schemas import NivelResponseModel
from schemas import MarcaRequestModel
from schemas import MarcaResponseModel
from schemas import UsuarioRequestModel
from schemas import UsuarioResponseModel
from schemas import ProductoRequestModel
from schemas import ProductoResponseModel
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
        raise HTTPException(409, 'El tipo de nivel de usuario ya se encuentra en uso.')

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
        raise HTTPException(409, 'El username ya se encuentra en uso.')

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
        raise HTTPException(409, 'Este SKU ya existe en el catálogo')

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

    seguimiento = SeguimientoUsuario.create(
        usuario_id = seguimiento.usuario_id,
        producto_id = seguimiento.producto_id
    )

    return seguimiento