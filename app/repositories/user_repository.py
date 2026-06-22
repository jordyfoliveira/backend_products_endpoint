from app.db.connection import get_db_connection as get_conn
from psycopg.types.json import Jsonb


async def get_user_by_username(username: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, username, email, hashed_password, role, is_active
                FROM users
                WHERE username = %s;
                """,
                (username,)
            )

            row = await cur.fetchone()

            if row is None:
                return None

            return {"id": row[0], "username": row[1], "email": row[2], "hashed_password": row[3], "role": row[4], "is_active": row[5]}


async def create_user(username: str, email: str, hashed_password: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:

            await cur.execute(
                """
                INSERT INTO users
                (username, email, hashed_password)
                VALUES
                (%s, %s, %s)
                RETURNING id;
                """,
                (username, email, hashed_password)
            )

            row = await cur.fetchone()

            return row[0]
        
async def list_users():
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, username, email, role, is_active, created_at
                FROM users
                ORDER BY id;
                """
            )

            rows = await cur.fetchall()

            return [{"id": row[0], "username": row[1], "email": row[2], "role": row[3], "is_active": row[4], "created_at": row[5],} for row in rows]
            
async def update_role(user_id: int, role: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:

            await cur.execute(
                """
                UPDATE users
                SET role = %s
                WHERE id = %s
                RETURNING id, username, role;
                """,
                (role, user_id)
            )

            row = await cur.fetchone()

            if row is None:
                return None

            return {"id": row[0], "username": row[1], "role": row[2]}
        
async def update_user_status(user_id: int, is_active: bool):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, username, is_active
                FROM users
                WHERE id = %s;
                """,
                (user_id,)
            )

            old_row = await cur.fetchone()

            if old_row is None:
                return None

            old_status = old_row[2]

            await cur.execute(
                """
                UPDATE users
                SET is_active = %s
                WHERE id = %s
                RETURNING id, username, email, role, is_active, created_at;
                """,
                (is_active, user_id)
            )

            row = await cur.fetchone()

            return {"id": row[0], "username": row[1], "email": row[2], "role": row[3], "is_active": row[4], "created_at": row[5], "old_status": old_status, "new_status": is_active}
        
async def get_user_by_email(email: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, username, email, hashed_password, role, is_active
                FROM users
                WHERE email = %s;
                """,
                (email,)
            )

            row = await cur.fetchone()

            if row is None:
                return None

            return {"id": row[0], "username": row[1], "email": row[2], "hashed_password": row[3], "role": row[4], "is_active": row[5]}

async def create_password_reset_token(user_id: int, token: str, expires_at):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO password_reset_tokens
                (user_id, token, expires_at)
                VALUES
                (%s, %s, %s)
                RETURNING id;
                """,
                (user_id, token, expires_at)
            )

            row = await cur.fetchone()

            return None if row is None else row[0]

async def get_password_reset_token(token: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, user_id, token, expires_at, used
                FROM password_reset_tokens
                WHERE token = %s;
                """,
                (token,)
            )

            row = await cur.fetchone()

            if row is None:
                return None

            return {"id": row[0], "user_id": row[1], "token": row[2], "expires_at": row[3], "used": row[4]}

async def mark_password_reset_token_used(token: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE password_reset_tokens
                SET used = TRUE
                WHERE token = %s
                RETURNING id;
                """,
                (token,)
            )

            row = await cur.fetchone()

            return None if row is None else row[0]

async def update_user_password(user_id: int, hashed_password: str):
    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE users
                SET hashed_password = %s
                WHERE id = %s
                RETURNING id;
                """,
                (hashed_password, user_id)
            )

            row = await cur.fetchone()

            return None if row is None else row[0]