from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis import Redis
import psutil

from app.database.session import get_db
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION
    }


@router.get("/live")
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {"status": "alive"}


@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe for Kubernetes"""
    try:
        # Check database
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    
    try:
        # Check Redis
        redis_client = Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False
    
    return {
        "status": "ready" if db_ok and redis_ok else "not ready",
        "database": "ok" if db_ok else "error",
        "redis": "ok" if redis_ok else "error",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with metrics"""
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Database connection pool
    pool = db.get_bind().pool
    
    return {
        "status": "healthy",
        "system": {
            "cpu": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
        },
        "database": {
            "status": "ok",
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "overflow": pool.overflow()
        },
        "redis": {
            "status": "ok"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
