from datetime import datetime

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from ..database import Usuario
from ..database import Nivel

from ..schemas import UsuarioRequestModel
from ..schemas import UsuarioResponseModel
from ..schemas import UsuarioRequestPutModel

from ..middleware import create_token
from ..middleware import get_current_user

router = APIRouter(prefix='/usuarios')

@router.post('', response_model=UsuarioResponseModel)
async def crear_usuario(usuario: UsuarioRequestModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

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
    
    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('', response_model=List[UsuarioResponseModel])
async def obtener_usuarios(page: int = 1, limit : int = 10, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:
        usuarios = Usuario.select().paginate(page, limit)

        return [usuario for usuario in usuarios]

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.get('/{usuario_id}', response_model=UsuarioResponseModel)
async def obtener_usuario_id(usuario_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

        if usuario_id is None:
            raise HTTPException(status_code=404, detail='Usuario no encontrado.')

        return usuario_id
    
    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.put('/{usuario_id}', response_model=UsuarioResponseModel)
async def actualizar_usuario(usuario_id: int, review_request: UsuarioRequestPutModel, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:

        usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

        if usuario_id is None:
            raise HTTPException(status_code=404, detail='Usuario no encontrado.')

        hash_password = Usuario.create_password(review_request.password)

        usuario_id.username = review_request.username
        usuario_id.password = hash_password
        usuario_id.nombre_completo = review_request.nombre_completo
        usuario_id.fecha_nacimiento = review_request.fecha_nacimiento
        usuario_id.email = review_request.email
        usuario_id.telefono = review_request.telefono
        usuario_id.direccion = review_request.direccion

        usuario_id.save()

        return usuario_id
    
    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.delete('/{usuario_id}', response_model=UsuarioResponseModel)
async def eliminar_un_usuario(usuario_id: int, token: str = Depends(get_current_user)):

    if token.get("nivel") == 1:
    
        usuario_id = Usuario.select().where(Usuario.id == usuario_id).first()

        if usuario_id is None:
            raise HTTPException(status_code=404, detail='Usuario no encontrado.')

        usuario_id.delete_instance()

        return usuario_id

    raise HTTPException(status_code=404, detail="Este usuario no tiene permisos para la petición.")

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    hash_password = Usuario.create_password(form_data.password)

    username = Usuario.select().where(Usuario.username == form_data.username).first()
    password = Usuario.select().where(Usuario.password == hash_password).first()

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        'access_token': create_token(form_data.username, username.nivel_id),
        'token_type': 'bearer'
    }