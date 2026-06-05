from app.repositories import user_repository
from app.auth.password import hash_password
from app.auth.password import verify_password
from app.auth.jwt import create_access_token

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