from fastapi import FastAPI
from fastapi.routing import APIRouter

from .database import Nivel
from .database import Marca
from .database import Usuario
from .database import Producto
from .database import SeguimientoUsuario

from .routes import nivel_router
from .routes import usuario_router
from .routes import producto_router
from .routes import marca_router
from .routes import seguimiento_router

from .database import database as connection

app = FastAPI(title='Sistema de Catalogo para Administrar Productos',
            description='En este proyecto seremos capaces de gestionar usuarios y productos delimitando accesos con base al rol de cada usuario.',
            version='0.1')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(marca_router)
api_v1.include_router(nivel_router)
api_v1.include_router(producto_router)
api_v1.include_router(seguimiento_router)
api_v1.include_router(usuario_router)

app.include_router(api_v1)

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