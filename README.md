# Expense Tracker Microservice

**CCS6440 Cloud Engineering Coursework**  
**Alex Tsirtiris - ATsirtiris/expense-tracker**

## Overview

Two-tier expense tracking application with Flask API and MariaDB database.

## Quick Start

```bash
# Clone repository
git clone https://github.com/ATsirtiris/expense-tracker.git
cd expense-tracker

# Start application
docker-compose up -d

# Test application
curl http://localhost:5001/health
```

## Architecture

- **API**: Flask REST API (Port 5001)
- **Database**: MariaDB with expense categories and user data
- **Containerization**: Docker Compose

## Key Endpoints

- `/health` - Health check
- `/metrics` - Prometheus metrics
- `/api/categories` - Get expense categories
- `/api/users` - User management
- `/api/expenses` - Expense CRUD operations

## Testing

```bash
python tests/test_api.py
```

All tests pass locally with running application.

## Requirements Met

✅ Microservices architecture  
✅ Git repository with branching  
✅ Database schema with relationships  
✅ Containerization with Docker  
✅ CI/CD pipeline (GitHub Actions)  
✅ Application monitoring  
✅ Comprehensive testing

## Files

- `app.py` - Main Flask application
- `docker-compose.yml` - Container orchestration
- `schema/init.sql` - Database schema
- `tests/test_api.py` - API tests
- `requirements.txt` - Python dependencies
