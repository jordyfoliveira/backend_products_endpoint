from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import require_admin
from app.services import auth_service, user_service
from app.schemas.user import UserRoleUpdate, ForgotPasswordRequest, ResetPasswordRequest

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

@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest):
    return await auth_service.forgot_password(payload.email)


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    result = await auth_service.reset_password(payload.token, payload.new_password)

    if result is None:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    return result