from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import require_admin
from app.services import audit_service

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("")
async def get_audit_logs(limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), entity: str | None = None, entity_id: int | None = None, current_user = Depends(require_admin)):
    return await audit_service.list_audit_logs(limit, offset, entity, entity_id)