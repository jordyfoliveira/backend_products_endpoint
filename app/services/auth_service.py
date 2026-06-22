from app.repositories import user_repository
from app.auth.password import hash_password
from app.auth.password import verify_password
from app.auth.jwt import create_access_token
import secrets
from datetime import datetime, timedelta

token = secrets.token_urlsafe(32)
expires_at = datetime.now() + timedelta(minutes=30)

async def register_user(user):

    existing_user = await user_repository.get_user_by_username(
        user.username
    )

    if existing_user is not None:
        return "USER_EXISTS"

    hashed = hash_password(user.password)

    user_id = await user_repository.create_user(
        user.username,
        user.email,
        hashed
    )

    return {
        "id": user_id,
        "message": "Utilizador criado com sucesso!"
    }
    
async def login_user(user):
    db_user = await user_repository.get_user_by_username(user.username)

    if db_user is None:
        return None

    if not db_user["is_active"]:
        return None

    password_valid = verify_password(
        user.password,
        db_user["hashed_password"]
    )

    if not password_valid:
        return None

    token = create_access_token(
        {
            "sub": db_user["username"],
            "role": db_user["role"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
async def forgot_password(email: str):
    user = await user_repository.get_user_by_email(email)

    if user is None:
        return {"message": "Se o email existir, será enviado um link de recuperação."}

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(minutes=30)

    await user_repository.create_password_reset_token(user["id"], token, expires_at)

    return {"message": "Token de redefinição de senha criado com sucesso!", "token": token}

async def reset_password(token: str, new_password: str):
    token_data = await user_repository.get_password_reset_token(token)

    if token_data is None or token_data["used"]:
        return None

    if token_data["expires_at"] < datetime.now():
        return None

    hashed_password = hash_password(new_password)

    await user_repository.update_user_password(token_data["user_id"], hashed_password)
    await user_repository.mark_password_reset_token_used(token)

    return {"message": "Password atualizada com sucesso!"}

