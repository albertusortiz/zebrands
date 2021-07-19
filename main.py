from fastapi import FastAPI
from fastapi import HTTPException

from database import Nivel
from database import Marca
from database import Usuario
from database import Producto
from database import UsuarioSeguimiento

from database import database as connection

from schemas import UsuarioRequestModel
from schemas import UsuarioResponseModel

app = FastAPI(title='Sistema de Catalogo para Administrar Productos',
            description='En este proyecto seremos capaces de gestionar usuarios y productos delimitando accesos con base al rol de cada usuario.',
            version='1')

@app.on_event('startup')
def startup():
    
    if connection.is_closed():
        connection.connect()

        print('Connecting...')

    connection.create_tables([Nivel, Marca, Usuario, Producto, UsuarioSeguimiento])

@app.on_event('shutdown')
def shutdown():
    
    if not connection.is_closed():
        connection.close()

        print('Closing...')

@app.get('/')
async def inicio():
    return 'Hola mundo, desde un servidor Flask'


@app.post('/usuarios', response_model=UsuarioResponseModel)
async def crear_usuario(usuario: UsuarioRequestModel):

    if Usuario.select().where(Usuario.username == usuario.username).exists():
        return HTTPException(409, 'El username ya se encuentra en uso.')

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

    return UsuarioResponseModel(id=usuario.id, username=usuario.username)