from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.app import App

router = APIRouter(prefix="/apps", tags=["Workspace"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{app_id}/workspace", response_class=HTMLResponse)
async def app_workspace(
    request: Request,
    app_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Render the app workspace"""
    
    # Get app (mock data for now)
    app = {
        "id": app_id,
        "app_name": "My Fitness App",
        "platform": "google_play",
        "developer": "FitTech Inc.",
        "category": "Health & Fitness",
        "country": "US",
        "version": "2.4.1",
        "rating": 4.8,
        "growth_score": 87,
        "growth_trend": 12.5,
        "visibility_score": 92,
        "visibility_trend": 8.3,
        "keyword_score": 78,
        "keyword_trend": 5.2,
        "creative_score": 71,
        "creative_trend": -2.1,
        "review_score": 94,
        "review_trend": 3.7,
        "competitor_score": 63,
        "competitor_trend": -4.2,
        "store_health": 82,
        "store_health_trend": 1.5,
        "conversion_potential": 2.4,
        "projected_growth": 94,
        "projected_visibility": 97,
        "projected_conversion": 3.8,
        "last_audit_date": (datetime.now() - timedelta(days=2)).strftime("%b %d, %Y"),
        "monitoring_status": "active"
    }
    
    # Next Win
    next_win = {
        "title": "Rewrite your app title",
        "description": "Your current title is missing primary keywords. Updating it could significantly improve your discoverability.",
        "impact": "+8% Visibility",
        "time": "10 minutes",
        "difficulty": "Easy",
        "difficulty_class": "easy",
        "reason": "Adding primary keywords to your title helps users find your app more easily in search results."
    }
    
    # Blueprint items
    blueprint_items = [
        {
            "priority": "Priority 1",
            "priority_class": "priority-1",
            "impact": "+8% Visibility",
            "title": "Rewrite app title",
            "description": "Add primary keywords to your title for better discoverability",
            "difficulty": "Easy",
            "difficulty_class": "easy",
            "time": "10 min",
            "completed": False
        },
        {
            "priority": "Priority 2",
            "priority_class": "priority-2",
            "impact": "+11% Conversion",
            "title": "Replace screenshot #1",
            "description": "Current screenshot isn't converting. Use a lifestyle shot showing your app in action.",
            "difficulty": "Medium",
            "difficulty_class": "medium",
            "time": "30 min",
            "completed": False
        },
        {
            "priority": "Priority 3",
            "priority_class": "priority-3",
            "impact": "+6% Visibility",
            "title": "Add 5 new keywords",
            "description": "Target high-volume keywords your competitors are missing",
            "difficulty": "Easy",
            "difficulty_class": "easy",
            "time": "15 min",
            "completed": False
        },
        {
            "priority": "Priority 4",
            "priority_class": "priority-4",
            "impact": "Rating Improvement",
            "title": "Reply to recent reviews",
            "description": "Respond to recent 1-star reviews to show you value user feedback",
            "difficulty": "Easy",
            "difficulty_class": "easy",
            "time": "5 min",
            "completed": True
        }
    ]
    
    # Opportunities
    opportunities = [
        {
            "id": "1",
            "badge": "Trending",
            "badge_class": "trending",
            "title": '"Fitness tracker" keyword',
            "description": "Search volume increased 340% in the last 30 days. Low competition.",
            "score": 92,
            "impact": "High Impact",
            "impact_class": "high"
        },
        {
            "id": "2",
            "badge": "Competitor",
            "badge_class": "competitor",
            "title": "Competitor dropped ranking",
            "description": "Your main competitor lost 12 positions for "photo editing". Quick win opportunity.",
            "score": 87,
            "impact": "High Impact",
            "impact_class": "high"
        },
        {
            "id": "3",
            "badge": "Review",
            "badge_class": "review",
            "title": "Users requesting dark mode",
            "description": "47 reviews mention dark mode. Could improve rating by 0.5 stars.",
            "score": 76,
            "impact": "Medium Impact",
            "impact_class": "medium"
        }
    ]
    
    # Health data
    health = {
        "visibility": 92,
        "visibility_trend": 8.3,
        "visibility_rec": "Maintain current strategy",
        "keywords": 78,
        "keywords_trend": 5.2,
        "keywords_rec": "Add 5 high-volume keywords",
        "creatives": 71,
        "creatives_trend": -2.1,
        "creatives_rec": "Replace screenshot #1",
        "reviews": 94,
        "reviews_trend": 3.7,
        "reviews_rec": "Reply to 3 recent reviews",
        "competitors": 63,
        "competitors_trend": -4.2,
        "competitors_rec": "Monitor top competitor",
        "metadata": 82,
        "metadata_trend": 1.5,
        "metadata_rec": "Update app description"
    }
    
    # Insights
    insights = [
        {"type": "positive", "text": "Your visibility improved 8.3% this week. Keep up the momentum!", "time": "2 hours ago"},
        {"type": "warning", "text": "A competitor updated their screenshots. Review your creative strategy.", "time": "4 hours ago"},
        {"type": "positive", "text": "Your average rating increased from 4.6 to 4.8. Great work!", "time": "1 day ago"},
        {"type": "info", "text": "A high-opportunity keyword was discovered: "fitness tracker"", "time": "2 days ago"}
    ]
    
    # Activity
    activities = [
        {"type": "audit", "text": "Audit completed with 87% overall score", "time": "2 hours ago"},
        {"type": "keyword", "text": "New keyword discovered: 'fitness tracker'", "time": "4 hours ago"},
        {"type": "competitor", "text": "Competitor 'FitApp Pro' updated their listing", "time": "6 hours ago"},
        {"type": "review", "text": "New 5-star review received", "time": "1 day ago"},
        {"type": "report", "text": "Weekly performance report generated", "time": "2 days ago"},
        {"type": "monitoring", "text": "Daily monitoring completed: 3 changes detected", "time": "2 days ago"}
    ]
    
    return templates.TemplateResponse(
        "apps/workspace.html",
        {
            "request": request,
            "user": current_user,
            "app": app,
            "next_win": next_win,
            "blueprint_items": blueprint_items,
            "opportunities": opportunities,
            "health": health,
            "insights": insights,
            "activities": activities
        }
    )
