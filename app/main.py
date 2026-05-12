from fastapi import FastAPI
from app.db.connection import get_db_connection
from app.routers.product_router import router as product_router

app = FastAPI(
    title="Products Async API",
    version="0.1.0",
    description="Async FastAPI project using PostgreSQL and psycopg.",
)

app.include_router(product_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/db-health", tags=["Health"])
async def db_health_check():
    try:
        connection = await get_db_connection()
        async with connection.cursor() as cur:
            await cur.execute("SELECT 1;")
            result = await cur.fetchone()

        await connection.close()
        return {"db_status": "ok", "result": result[0]}
    except Exception as e:
        return {"db_status": "error", "details": str(e)}