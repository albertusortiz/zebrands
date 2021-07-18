from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index():
    return 'Hola mundo, desde un servidor Flask'