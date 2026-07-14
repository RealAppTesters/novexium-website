# Novexium Production Deployment Guide

## Prerequisites

- Kubernetes cluster (v1.24+)
- PostgreSQL 15 with replication
- Redis 7
- Docker registry access
- Kubectl configured
- Helm v3

## Environment Variables

```bash
# Application
APP_NAME=Novexium
APP_ENV=production
DEBUG=false
SECRET_KEY=<secure-key>
ENCRYPTION_KEY=<secure-key>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/novexium
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis:6379/0

# Cache
CACHE_TTL=300

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=<sendgrid-api-key>

# Stripe
STRIPE_SECRET_KEY=<stripe-secret>
STRIPE_WEBHOOK_SECRET=<webhook-secret>

# Security
CORS_ORIGINS=https://app.novexium.com,https://novexium.com
SESSION_TIMEOUT=604800

# Rate Limiting
RATE_LIMIT=1000
RATE_LIMIT_WINDOW=3600

# Monitoring
SENTRY_DSN=<sentry-dsn>
