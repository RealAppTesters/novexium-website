from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.models.notification import Notification
from app.models.activity_item import ActivityItem
from app.models.daily_summary import DailySummary
from app.notifications.generators.audit import AuditNotificationGenerator
from app.notifications.generators.rank import RankNotificationGenerator
from app.notifications.generators.competitor import CompetitorNotificationGenerator
from app.notifications.generators.review import ReviewNotificationGenerator
from app.notifications.generators.report import ReportNotificationGenerator
from app.notifications.generators.billing import BillingNotificationGenerator
from app.notifications.services.priority import PriorityService


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.generators = {
            'audit': AuditNotificationGenerator(),
            'rank': RankNotificationGenerator(),
            'competitor': CompetitorNotificationGenerator(),
            'review': ReviewNotificationGenerator(),
            'report': ReportNotificationGenerator(),
            'billing': BillingNotificationGenerator()
        }
        self.priority_service = PriorityService()
    
    def create_notification(self, user_id: str, data: Dict) -> Dict:
        """Create a new notification"""
        notification = Notification(
            id=uuid.uuid4(),
            user_id=user_id,
            app_id=data.get('app_id'),
            notification_type=data.get('type', 'info'),
            priority=self.priority_service.calculate_priority(data),
            title=data['title'],
            description=data.get('description'),
            source_module=data.get('source_module'),
            source_id=data.get('source_id'),
            action_label=data.get('action_label'),
            action_url=data.get('action_url'),
            notification_date=datetime.utcnow(),
            metadata=data.get('metadata')
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return self._notification_to_dict(notification)
    
    def create_activity(self, user_id: str, data: Dict) -> Dict:
        """Create an activity item"""
        activity = ActivityItem(
            id=uuid.uuid4(),
            user_id=user_id,
            app_id=data.get('app_id'),
            activity_type=data['activity_type'],
            title=data['title'],
            description=data.get('description'),
            source_module=data.get('source_module'),
            source_id=data.get('source_id'),
            activity_date=datetime.utcnow(),
            metadata=data.get('metadata')
        )
        
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        
        return self._activity_to_dict(activity)
    
    def get_notifications(self, user_id: str, filters: Dict = None, 
                          limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's notifications"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if filters:
            if filters.get('type'):
                query = query.filter(Notification.notification_type == filters['type'])
            if filters.get('priority'):
                query = query.filter(Notification.priority == filters['priority'])
            if filters.get('app_id'):
                query = query.filter(Notification.app_id == filters['app_id'])
            if filters.get('read') is not None:
                query = query.filter(Notification.is_read == filters['read'])
        
        notifications = query.order_by(
            Notification.notification_date.desc()
        ).offset(offset).limit(limit).all()
        
        return [self._notification_to_dict(n) for n in notifications]
    
    def get_activity(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's activity timeline"""
        activities = self.db.query(ActivityItem).filter(
            ActivityItem.user_id == user_id
        ).order_by(
            ActivityItem.activity_date.desc()
        ).offset(offset).limit(limit).all()
        
        return [self._activity_to_dict(a) for a in activities]
    
    def mark_read(self, notification_id: str) -> Dict:
        """Mark a notification as read"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.db.commit()
            return {'read': True}
        
        return {'error': 'Notification not found'}
    
    def mark_all_read(self, user_id: str) -> Dict:
        """Mark all notifications as read"""
        self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({'is_read': True, 'read_at': datetime.utcnow()})
        
        self.db.commit()
        return {'count': self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).count()}
    
    def bookmark_notification(self, notification_id: str) -> Dict:
        """Bookmark a notification"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if notification:
            notification.is_bookmarked = not notification.is_bookmarked
            self.db.commit()
            return {'bookmarked': notification.is_bookmarked}
        
        return {'error': 'Notification not found'}
    
    def dismiss_notification(self, notification_id: str) -> Dict:
        """Dismiss a notification"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if notification:
            notification.dismissed_at = datetime.utcnow()
            self.db.commit()
            return {'dismissed': True}
        
        return {'error': 'Notification not found'}
    
    def get_unread_count(self, user_id: str) -> int:
        """Get unread notification count"""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
    
    def generate_summary(self, user_id: str, period: str = 'daily') -> Dict:
        """Generate a daily or weekly summary"""
        if period == 'daily':
            return self._generate_daily_summary(user_id)
        else:
            return self._generate_weekly_summary(user_id)
    
    def _generate_daily_summary(self, user_id: str) -> Dict:
        """Generate daily summary"""
        cutoff = datetime.utcnow() - timedelta(days=1)
        
        # Get recent activity
        activities = self.db.query(ActivityItem).filter(
            ActivityItem.user_id == user_id,
            ActivityItem.activity_date >= cutoff
        ).order_by(ActivityItem.activity_date.desc()).limit(20).all()
        
        # Get top recommendations
        notifications = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.notification_date >= cutoff,
            Notification.priority.in_(['critical', 'high'])
        ).order_by(Notification.notification_date.desc()).limit(5).all()
        
        return {
            'period': 'daily',
            'date': datetime.utcnow().isoformat(),
            'activity_count': len(activities),
            'recent_activities': [self._activity_to_dict(a) for a in activities[:5]],
            'top_notifications': [self._notification_to_dict(n) for n in notifications],
            'recommendation_count': len(notifications)
        }
    
    def _generate_weekly_summary(self, user_id: str) -> Dict:
        """Generate weekly summary"""
        cutoff = datetime.utcnow() - timedelta(days=7)
        
        activities = self.db.query(ActivityItem).filter(
            ActivityItem.user_id == user_id,
            ActivityItem.activity_date >= cutoff
        ).all()
        
        return {
            'period': 'weekly',
            'date': datetime.utcnow().isoformat(),
            'total_activities': len(activities),
            'activity_types': self._group_activities_by_type(activities)
        }
    
    def _group_activities_by_type(self, activities: List[ActivityItem]) -> Dict:
        """Group activities by type"""
        groups = {}
        for activity in activities:
            if activity.activity_type not in groups:
                groups[activity.activity_type] = 0
            groups[activity.activity_type] += 1
        return groups
    
    def _notification_to_dict(self, notification: Notification) -> Dict:
        return {
            'id': str(notification.id),
            'type': notification.notification_type,
            'priority': notification.priority,
            'title': notification.title,
            'description': notification.description,
            'source_module': notification.source_module,
            'action_label': notification.action_label,
            'action_url': notification.action_url,
            'is_read': notification.is_read,
            'is_bookmarked': notification.is_bookmarked,
            'notification_date': notification.notification_date.isoformat()
        }
    
    def _activity_to_dict(self, activity: ActivityItem) -> Dict:
        return {
            'id': str(activity.id),
            'type': activity.activity_type,
            'title': activity.title,
            'description': activity.description,
            'source_module': activity.source_module,
            'activity_date': activity.activity_date.isoformat()
        }
