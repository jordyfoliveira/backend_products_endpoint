from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from app.auth.jwt import SECRET_KEY, ALGORITHM


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return {
            "username": username,
            "role": role
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
        
async def require_admin(
    current_user = Depends(get_current_user)
):
    if current_user["role"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Permissão insuficiente"
        )

    return current_user


async def require_manager_or_admin(
    current_user = Depends(get_current_user)
):
    if current_user["role"] not in ["MANAGER", "ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Permissão insuficiente"
        )

    return current_user