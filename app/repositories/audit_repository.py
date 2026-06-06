from app.db.connection import get_db_connection as get_conn

columns = ["id", "ts", "action", "entity", "entity_id", "details"]


async def list_audit_logs( limit: int = 50, offset: int = 0, entity: str | None = None, entity_id: int | None = None):
    query = """
    SELECT id, ts, action, entity, entity_id, details
    FROM audit_logs
    """

    conditions = []
    params = []

    if entity is not None:
        conditions.append("entity = %s")
        params.append(entity)

    if entity_id is not None:
        conditions.append("entity_id = %s")
        params.append(entity_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY ts DESC LIMIT %s OFFSET %s;"
    params.extend([limit, offset])

    async with await get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            rows = await cur.fetchall()

            return [dict(zip(columns, row)) for row in rows]