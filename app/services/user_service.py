from app.repositories import user_repository

async def list_users():
    return await user_repository.list_users()

async def update_role(user_id: int, role: str):
    return await user_repository.update_role(user_id, role)

async def update_user_status(user_id: int, is_active: bool):
    return await user_repository.update_user_status(user_id, is_active)