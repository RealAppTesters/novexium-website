from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.report import Report
from app.report.sections.summary import SummarySection
from app.report.sections.score import ScoreSection
from app.report.sections.blueprint import BlueprintSection
from app.report.sections.visibility import VisibilitySection
from app.report.sections.keywords import KeywordSection
from app.report.sections.ranking import RankingSection
from app.report.sections.listing import ListingSection
from app.report.sections.creative import CreativeSection
from app.report.sections.competitors import CompetitorSection
from app.report.sections.reviews import ReviewSection
from app.report.sections.recommendations import RecommendationSection


class ReportBuilder:
    def __init__(self, db: Session):
        self.db = db
        self.sections = {
            'summary': SummarySection(),
            'score': ScoreSection(),
            'blueprint': BlueprintSection(),
            'visibility': VisibilitySection(),
            'keywords': KeywordSection(),
            'ranking': RankingSection(),
            'listing': ListingSection(),
            'creative': CreativeSection(),
            'competitors': CompetitorSection(),
            'reviews': ReviewSection(),
            'recommendations': RecommendationSection()
        }
    
    def build(self, report: Report) -> Dict[str, Any]:
        """Build report data"""
        report_data = {
            'title': report.title,
            'description': report.description,
            'sections': [],
            'data': {}
        }
        
        for section_name in report.sections:
            if section_name in self.sections:
                section = self.sections[section_name]
                section_data = section.build(report.app_id, report.settings)
                report_data['sections'].append({
                    'name': section_name,
                    'title': section.title,
                    'data': section_data
                })
        
        return report_data
