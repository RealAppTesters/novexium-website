from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.audit_service import AuditService
from app.background.tasks.audit_tasks import run_audit_task

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("/{app_id}/run")
async def run_audit(
    app_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new audit for an app"""
    service = AuditService(db)
    
    # Run audit in background
    background_tasks.add_task(run_audit_task, app_id, str(current_user.id))
    
    return {
        "status": "started",
        "message": "Audit started in background",
        "app_id": app_id
    }

@router.get("/{audit_id}")
async def get_audit(
    audit_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific audit"""
    service = AuditService(db)
    audit = service.get_audit(audit_id)
    
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    return audit

@router.get("/{app_id}/history")
async def get_audit_history(
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get audit history for an app"""
    service = AuditService(db)
    return service.get_audit_history(app_id)

@router.get("/compare/{audit1_id}/{audit2_id}")
async def compare_audits(
    audit1_id: str,
    audit2_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two audits"""
    service = AuditService(db)
    comparison = service.compare_audits(audit1_id, audit2_id)
    
    if not comparison:
        raise HTTPException(status_code=404, detail="One or both audits not found")
    
    return comparison
