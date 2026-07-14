from celery import Task
from app.background.celery_app import celery_app
from app.database.session import SessionLocal
from app.services.audit_service import AuditService
from app.models.notification import Notification


@celery_app.task(name="audit.run_audit_task")
def run_audit_task(app_id: str, user_id: str):
    """Run audit in background"""
    db = SessionLocal()
    try:
        service = AuditService(db)
        result = service.run_audit(app_id, user_id)
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            notification=f"Audit completed for your app. Score: {result['overall_score']}",
            type="audit",
            read_status=False
        )
        db.add(notification)
        db.commit()
        
        return result
    finally:
        db.close()
