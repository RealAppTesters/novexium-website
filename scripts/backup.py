#!/usr/bin/env python3
"""
Database Backup Script
Run daily via cron or Kubernetes CronJob
"""

import os
import subprocess
import boto3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKUP_DIR = "/tmp/backups"
RETENTION_DAYS = 30
S3_BUCKET = os.getenv("BACKUP_BUCKET", "novexium-backups")


def create_backup():
    """Create a PostgreSQL backup"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"novexium_{timestamp}.backup"
    filepath = os.path.join(BACKUP_DIR, filename)
    
    # Create backup
    cmd = [
        "pg_dump",
        "-h", os.getenv("DB_HOST"),
        "-U", os.getenv("DB_USER"),
        "-d", os.getenv("DB_NAME"),
        "--format=custom",
        "--compress=9",
        "--file", filepath
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        logger.error(f"Backup failed: {result.stderr}")
        return None
    
    logger.info(f"Backup created: {filename}")
    return filepath


def upload_to_s3(filepath):
    """Upload backup to S3"""
    s3 = boto3.client('s3')
    
    try:
        s3.upload_file(
            filepath,
            S3_BUCKET,
            os.path.basename(filepath)
        )
        logger.info(f"Backup uploaded to S3: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return False


def cleanup_old_backups():
    """Remove old local backups"""
    os.system(f"find {BACKUP_DIR} -name '*.backup' -mtime +{RETENTION_DAYS} -delete")
    logger.info(f"Cleaned up backups older than {RETENTION_DAYS} days")


def cleanup_s3_backups():
    """Remove old S3 backups"""
    s3 = boto3.client('s3')
    
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    response = s3.list_objects_v2(Bucket=S3_BUCKET)
    
    for obj in response.get('Contents', []):
        if obj['LastModified'] < cutoff:
            s3.delete_object(Bucket=S3_BUCKET, Key=obj['Key'])
            logger.info(f"Deleted old backup from S3: {obj['Key']}")


def main():
    """Main backup routine"""
    logger.info("Starting backup process...")
    
    # Create backup
    filepath = create_backup()
    if not filepath:
        logger.error("Backup creation failed")
        return 1
    
    # Upload to S3
    if not upload_to_s3(filepath):
        logger.warning("S3 upload failed, backup saved locally")
    
    # Cleanup
    cleanup_old_backups()
    cleanup_s3_backups()
    
    logger.info("Backup process complete")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
