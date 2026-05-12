from psycopg import AsyncConnection as pgsql
from app.core.config import settings


async def get_db_connection():
    connection = await pgsql.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )

    return connection