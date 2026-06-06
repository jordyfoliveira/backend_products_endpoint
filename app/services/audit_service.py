from app.repositories import audit_repository


async def list_audit_logs(limit: int = 50, offset: int = 0, entity: str | None = None, entity_id: int | None = None):
    return await audit_repository.list_audit_logs(limit, offset, entity, entity_id)