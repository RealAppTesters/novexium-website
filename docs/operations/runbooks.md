# Novexium Operational Runbooks

## Runbook: Database Connection Issues

### Symptoms
- Application returns 500 errors
- "Too many connections" errors in logs
- Health check shows database as unhealthy

### Immediate Actions
1. Check current connections:
```sql
SELECT count(*) FROM pg_stat_activity;
