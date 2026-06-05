from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate, UserLogin
from app.services import auth_service
from fastapi import Depends
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(user: UserCreate):

    result = await auth_service.register_user(user)

    if result == "USER_EXISTS":
        raise HTTPException(
            status_code=409,
            detail="Utilizador já existe"
        )

    return result


@router.post("/login")
async def login(user: UserLogin):

    result = await auth_service.login_user(user)

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )

    return result

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user