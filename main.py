from fastapi import FastAPI

app = FastAPI(title='Sistema de Catalogo para Administrar Productos',
            description='En este proyecto seremos capaces de gestionar usuarios y productos delimitando accesos con base al rol de cada usuario.',
            version='1')

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor Flask'