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
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return result

@router.patch("/{user_id}/activate")
async def activate_user(user_id: int, current_user = Depends(require_admin)):
    result = await user_service.update_user_status(user_id, True)

    if result is None:
        raise HTTPException(status_code=404,detail="Utilizador não encontrado")

    return {"id": result["id"], "username": result["username"], "is_active": result["is_active"], "performed_by": current_user["username"], "message": "Utilizador ativado com sucesso!"}


@router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: int, current_user = Depends(require_admin)):
    result = await user_service.update_user_status(user_id, False)

    if result is None:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return {"id": result["id"], "username": result["username"], "is_active": result["is_active"], "performed_by": current_user["username"], "message": "Utilizador desativado com sucesso!"}