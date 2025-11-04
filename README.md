# ORM Dashboard API

Secure FastAPI backend for the Commander's Dashboard - companion to the iORM mobile application.

## Features

- **REST API**: Complete CRUD operations for ORM flights and dashboard data
- **PostgreSQL**: Production-ready database with relationships and indexes
- **Authentication**: JWT-based auth with role-based access control (RBAC)
- **Data Sanitization**: Automatic PII removal for historical data
- **Military Compliance**: Designed for IL4/IL5 security requirements
- **Export APIs**: CSV and PDF report generation

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/orm_dashboard"
export SECRET_KEY="your-secret-key"

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)

1. Click "Deploy on Railway"
2. Connect your GitHub repository
3. Add environment variables:
   - `DATABASE_URL` (auto-provided by Railway PostgreSQL)
   - `SECRET_KEY` (generate secure key)
4. Deploy!

### Deploy to Render

1. Connect GitHub repository to Render
2. Create PostgreSQL database
3. Create Web Service with:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

### Health & Info
- `GET /` - API info
- `GET /api/v1/health` - Health check

### ORM Data
- `POST /api/v1/orm/submit` - Submit ORM from mobile app
- `GET /api/v1/flights` - List flights for dashboard
- `GET /api/v1/flights/{id}` - Get flight details

### Dashboard Metrics
- `GET /api/v1/metrics/summary` - Risk summary by unit
- `GET /api/v1/metrics/top-hazards` - Top 10 hazards analysis
- `GET /api/v1/units` - Available units

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Current user info

## Data Flow

```
iORM Mobile App → POST /api/v1/orm/submit → PostgreSQL → Dashboard API → Next.js Frontend
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (development)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Optional
SQL_DEBUG=false
ENVIRONMENT=development
```

## Database Schema

### Core Tables
- `units` - Military units and their ORM matrices
- `flights` - Individual flight records
- `flight_hazards` - Assessed hazards per flight
- `crew_members` - Crew risk assessments
- `users` - Dashboard users with RBAC
- `audit_events` - Complete audit trail

### Data Sanitization
- **Current Day**: Full data access for authorized users
- **Historical**: Automatic PII removal (crew names, callsigns, tail numbers)
- **Audit Trail**: All data access logged

## Security Features

- **JWT Authentication**: Secure token-based auth
- **RBAC**: Role-based access (Unit Lead, Safety Officer, Group Lead, Wing Lead, Admin)
- **Data Sanitization**: Automatic PII scrubbing for historical data
- **Audit Logging**: Complete access trail
- **CORS Protection**: Configured for production

## Development

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing

```bash
pytest
```

## Architecture

Built with:
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM with relationship management
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **PostgreSQL**: Production database
- **JWT**: Secure authentication

## Integration

### Mobile App Integration
The iORM mobile app submits completed, approved ORM sheets via `POST /api/v1/orm/submit` with:
- Unit authentication
- Approved ORM data only
- Automatic data validation

### Dashboard Integration
The Next.js dashboard consumes data via REST APIs with:
- Real-time metrics
- Historical trend analysis
- Export capabilities
- Role-based data access

---

**Security Notice**: This system is designed for military operational risk management. All data handling follows DoD security guidelines and data sanitization requirements.