from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import require_admin
from app.services import user_service
from app.schemas.user import UserRoleUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def list_users(current_user = Depends(require_admin)):
    return await user_service.list_users()

@router.patch("/{user_id}/role")
async def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    current_user = Depends(require_admin)
):
    result = await user_service.update_role(
        user_id,
        payload.role
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Utilizador não encontrado"
        )

    return result