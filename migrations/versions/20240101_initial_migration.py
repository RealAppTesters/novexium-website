"""initial migration with all tables

Revision ID: 20240101_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid

# revision identifiers, used by Alembic.
revision = '20240101_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # ============================================
    # 1. CREATE ENUM TYPES
    # ============================================
    op.execute("CREATE TYPE subscription_plan AS ENUM ('free', 'pro', 'business', 'enterprise')")
    op.execute("CREATE TYPE subscription_status AS ENUM ('active', 'expired', 'cancelled', 'trial')")
    op.execute("CREATE TYPE platform AS ENUM ('google_play', 'app_store')")
    op.execute("CREATE TYPE sentiment AS ENUM ('positive', 'neutral', 'negative')")
    op.execute("CREATE TYPE reply_status AS ENUM ('pending', 'replied', 'skipped')")
    op.execute("CREATE TYPE asset_type AS ENUM ('screenshot', 'feature_graphic', 'app_icon', 'promo_video')")
    op.execute("CREATE TYPE report_type AS ENUM ('aso_audit', 'keyword_tracking', 'competitor_analysis', 'performance_report')")
    op.execute("CREATE TYPE report_status AS ENUM ('pending', 'processing', 'completed', 'failed')")
    op.execute("CREATE TYPE notification_type AS ENUM ('system', 'audit', 'subscription', 'report', 'keyword', 'review')")
    op.execute("CREATE TYPE payment_status AS ENUM ('paid', 'unpaid', 'pending', 'failed', 'refunded')")
    
    # ============================================
    # 2. CREATE TABLES
    # ============================================
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('avatar', sa.String(500), nullable=True),
        sa.Column('email_verified', sa.Boolean, default=False),
        sa.Column('subscription_plan', sa.Enum('free', 'pro', 'business', 'enterprise', name='subscription_plan'), default='free'),
        sa.Column('subscription_status', sa.Enum('active', 'expired', 'cancelled', 'trial', name='subscription_status'), default='trial'),
        sa.Column('trial_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trial_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    
    # Apps table
    op.create_table(
        'apps',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.Enum('google_play', 'app_store', name='platform'), nullable=False),
        sa.Column('package_name', sa.String(255), nullable=False),
        sa.Column('store_url', sa.String(500), nullable=False),
        sa.Column('app_name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('country', sa.String(2), nullable=True),
        sa.Column('aso_score', sa.Float, default=0.0),
        sa.Column('visibility_score', sa.Float, default=0.0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
    )
    
    # Audits table
    op.create_table(
        'audits',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('overall_score', sa.Float, nullable=False),
        sa.Column('keyword_score', sa.Float, nullable=False),
        sa.Column('metadata_score', sa.Float, nullable=False),
        sa.Column('creative_score', sa.Float, nullable=False),
        sa.Column('review_score', sa.Float, nullable=False),
        sa.Column('recommendations', JSON, nullable=True),
        sa.Column('audit_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
    )
    
    # Keywords table
    op.create_table(
        'keywords',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('keyword', sa.String(255), nullable=False),
        sa.Column('search_volume', sa.Integer, nullable=True),
        sa.Column('difficulty', sa.Integer, nullable=True),
        sa.Column('opportunity_score', sa.Float, nullable=True),
        sa.Column('ranking', sa.Integer, nullable=True),
        sa.Column('estimated_traffic', sa.Integer, nullable=True),
        sa.Column('country', sa.String(2), nullable=True),
        sa.Column('language', sa.String(2), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )
    
    # App Keywords (junction table)
    op.create_table(
        'app_keywords',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('keyword_id', UUID(as_uuid=True), nullable=False),
        sa.Column('current_ranking', sa.Integer, nullable=True),
        sa.Column('previous_ranking', sa.Integer, nullable=True),
        sa.Column('ranking_change', sa.Integer, nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['keyword_id'], ['keywords.id'], ondelete='RESTRICT'),
    )
    
    # Competitors table
    op.create_table(
        'competitors',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('competitor_app', sa.String(255), nullable=False),
        sa.Column('store_url', sa.String(500), nullable=False),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('reviews', sa.Integer, nullable=True),
        sa.Column('estimated_downloads', sa.Integer, nullable=True),
        sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True),
        sa.Column('country', sa.String(2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
    )
    
    # Competitor Monitoring table
    op.create_table(
        'competitor_monitoring',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('competitor_id', UUID(as_uuid=True), nullable=False),
        sa.Column('keywords', JSON, nullable=True),
        sa.Column('ratings', JSON, nullable=True),
        sa.Column('screenshots', JSON, nullable=True),
        sa.Column('store_listing', JSON, nullable=True),
        sa.Column('visibility', JSON, nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['competitor_id'], ['competitors.id'], ondelete='CASCADE'),
    )
    
    # Reviews table
    op.create_table(
        'reviews',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('reviewer', sa.String(255), nullable=True),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('review', sa.Text, nullable=True),
        sa.Column('sentiment', sa.Enum('positive', 'neutral', 'negative', name='sentiment'), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('language', sa.String(2), nullable=True),
        sa.Column('reply_status', sa.Enum('pending', 'replied', 'skipped', name='reply_status'), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
    )
    
    # Store Listings table
    op.create_table(
        'store_listings',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('short_description', sa.String(255), nullable=True),
        sa.Column('long_description', sa.Text, nullable=True),
        sa.Column('release_notes', sa.Text, nullable=True),
        sa.Column('character_count', sa.Integer, nullable=True),
        sa.Column('optimization_score', sa.Float, nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
    )
    
    # Creative Assets table
    op.create_table(
        'creative_assets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('asset_type', sa.Enum('screenshot', 'feature_graphic', 'app_icon', 'promo_video', name='asset_type'), nullable=False),
        sa.Column('asset_url', sa.String(500), nullable=False),
        sa.Column('analysis_results', JSON, nullable=True),
        sa.Column('upload_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='CASCADE'),
    )
    
    # Reports table
    op.create_table(
        'reports',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('app_id', UUID(as_uuid=True), nullable=True),
        sa.Column('pdf_file', sa.String(500), nullable=True),
        sa.Column('report_type', sa.Enum('aso_audit', 'keyword_tracking', 'competitor_analysis', 'performance_report', name='report_type'), nullable=False),
        sa.Column('generated_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', name='report_status'), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['app_id'], ['apps.id'], ondelete='SET NULL'),
    )
    
    # Notifications table
    op.create_table(
        'notifications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('notification', sa.Text, nullable=False),
        sa.Column('type', sa.Enum('system', 'audit', 'subscription', 'report', 'keyword', 'review', name='notification_type'), nullable=False),
        sa.Column('read_status', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Billing table
    op.create_table(
        'billing',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('stripe_customer_id', sa.String(255), nullable=False),
        sa.Column('plan', sa.String(50), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('currency', sa.String(3), default='USD'),
        sa.Column('invoice', sa.String(255), nullable=True),
        sa.Column('renewal_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payment_status', sa.Enum('paid', 'unpaid', 'pending', 'failed', 'refunded', name='payment_status'), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
    )
    
    # Sessions table
    op.create_table(
        'sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('token', sa.Text, nullable=False, unique=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text, nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # API Keys table
    op.create_table(
        'api_keys',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('api_key', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('permissions', JSON, nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expiry', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Activity Logs table
    op.create_table(
        'activity_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('details', JSON, nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # ============================================
    # 3. CREATE INDEXES
    # ============================================
    
    # Users indexes
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_email_verified', 'users', ['email', 'email_verified'])
    op.create_index('idx_user_subscription', 'users', ['subscription_plan', 'subscription_status'])
    
    # Apps indexes
    op.create_index('idx_app_user_package', 'apps', ['user_id', 'package_name'], unique=True)
    op.create_index('idx_app_aso_score', 'apps', ['aso_score'])
    op.create_index('idx_app_visibility', 'apps', ['visibility_score'])
    
    # Audits indexes
    op.create_index('idx_audit_app_date', 'audits', ['app_id', 'audit_date'])
    op.create_index('idx_audit_overall_score', 'audits', ['overall_score'])
    
    # Keywords indexes
    op.create_index('idx_keyword_search', 'keywords', ['keyword'])
    op.create_index('idx_keyword_country_lang', 'keywords', ['keyword', 'country', 'language'])
    op.create_index('idx_keyword_search_volume', 'keywords', ['search_volume'])
    op.create_index('idx_keyword_opportunity', 'keywords', ['opportunity_score'])
    
    # App Keywords indexes
    op.create_index('idx_app_keyword_date', 'app_keywords', ['app_id', 'keyword_id', 'date'])
    op.create_index('idx_app_keyword_ranking', 'app_keywords', ['current_ranking'])
    
    # Competitors indexes
    op.create_index('idx_competitor_app_url', 'competitors', ['app_id', 'store_url'])
    op.create_index('idx_competitor_last_checked', 'competitors', ['last_checked'])
    
    # Competitor Monitoring indexes
    op.create_index('idx_monitoring_competitor_date', 'competitor_monitoring', ['competitor_id', 'date'])
    
    # Reviews indexes
    op.create_index('idx_review_app_rating', 'reviews', ['app_id', 'rating'])
    op.create_index('idx_review_sentiment', 'reviews', ['sentiment'])
    op.create_index('idx_review_created', 'reviews', ['created_at'])
    op.create_index('idx_review_reply_status', 'reviews', ['reply_status'])
    
    # Store Listings indexes
    op.create_index('idx_store_listing_app', 'store_listings', ['app_id'], unique=True)
    
    # Creative Assets indexes
    op.create_index('idx_asset_app_type', 'creative_assets', ['app_id', 'asset_type'])
    
    # Reports indexes
    op.create_index('idx_report_user_date', 'reports', ['user_id', 'generated_date'])
    op.create_index('idx_report_status', 'reports', ['status'])
    
    # Notifications indexes
    op.create_index('idx_notification_user_read', 'notifications', ['user_id', 'read_status'])
    op.create_index('idx_notification_created', 'notifications', ['created_at'])
    
    # Billing indexes
    op.create_index('idx_billing_stripe_customer', 'billing', ['stripe_customer_id'])
    op.create_index('idx_billing_renewal_date', 'billing', ['renewal_date'])
    op.create_index('idx_billing_payment_status', 'billing', ['payment_status'])
    
    # Sessions indexes
    op.create_index('idx_session_token', 'sessions', ['token'])
    op.create_index('idx_session_token_expiry', 'sessions', ['token', 'expires_at'])
    op.create_index('idx_session_user_expiry', 'sessions', ['user_id', 'expires_at'])
    
    # API Keys indexes
    op.create_index('idx_apikey_key', 'api_keys', ['api_key'], unique=True)
    op.create_index('idx_apikey_user_expiry', 'api_keys', ['user_id', 'expiry'])
    op.create_index('idx_apikey_last_used', 'api_keys', ['last_used'])
    
    # Activity Logs indexes
    op.create_index('idx_activity_user_action', 'activity_logs', ['user_id', 'action'])
    op.create_index('idx_activity_created', 'activity_logs', ['created_at'])
    op.create_index('idx_activity_action_date', 'activity_logs', ['action', 'created_at'])

def downgrade():
    # Drop all tables in reverse order
    op.drop_table('activity_logs')
    op.drop_table('api_keys')
    op.drop_table('sessions')
    op.drop_table('billing')
    op.drop_table('notifications')
    op.drop_table('reports')
    op.drop_table('creative_assets')
    op.drop_table('store_listings')
    op.drop_table('reviews')
    op.drop_table('competitor_monitoring')
    op.drop_table('competitors')
    op.drop_table('app_keywords')
    op.drop_table('keywords')
    op.drop_table('audits')
    op.drop_table('apps')
    op.drop_table('users')
    
    # Drop all enum types
    op.execute('DROP TYPE IF EXISTS payment_status')
    op.execute('DROP TYPE IF EXISTS notification_type')
    op.execute('DROP TYPE IF EXISTS report_status')
    op.execute('DROP TYPE IF EXISTS report_type')
    op.execute('DROP TYPE IF EXISTS asset_type')
    op.execute('DROP TYPE IF EXISTS reply_status')
    op.execute('DROP TYPE IF EXISTS sentiment')
    op.execute('DROP TYPE IF EXISTS platform')
    op.execute('DROP TYPE IF EXISTS subscription_status')
    op.execute('DROP TYPE IF EXISTS subscription_plan')
