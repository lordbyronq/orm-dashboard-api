"""
FastAPI main application for ORM Dashboard API
Secure backend for Commander's Dashboard - companion to iORM mobile app
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime

from .database import get_db, engine
from .models import Base, Flight, Unit, User, SeverityLevel
from .config import settings

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="ORM Dashboard API",
    description="Secure API for Commander's ORM Dashboard - companion to iORM mobile app",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API information and health check"""
    return {
        "message": "ORM Dashboard API",
        "version": "1.0.0",
        "description": "Secure backend for Commander's ORM Dashboard",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/health")
async def health_check(db: Session = Depends(get_db)):
    """Detailed health check with database connectivity"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/v1/flights")
async def get_flights(
    limit: int = 50,
    unit_id: str = None,
    db: Session = Depends(get_db)
):
    """Get flights for dashboard with optional filtering"""
    query = db.query(Flight)

    if unit_id:
        query = query.filter(Flight.unit_id == unit_id)

    flights = query.order_by(Flight.flight_date.desc()).limit(limit).all()

    return {
        "data": [
            {
                "id": flight.id,
                "unit_id": flight.unit_id,
                "callsign": flight.callsign,
                "aircraft_type": flight.aircraft_type,
                "mission_type": flight.mission_type,
                "flight_date": flight.flight_date.isoformat(),
                "total_risk_score": flight.total_risk_score,
                "risk_tier": flight.risk_tier.value,
                "is_approved": flight.is_approved,
                "is_briefed": flight.is_briefed,
                "crew_count": flight.crew_count,
                "aircraft_commander": flight.aircraft_commander if not flight.is_pii_scrubbed else "[REDACTED]"
            }
            for flight in flights
        ],
        "total": len(flights),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/units")
async def get_units(db: Session = Depends(get_db)):
    """Get available units for dashboard"""
    units = db.query(Unit).all()

    return {
        "data": [
            {
                "id": unit.id,
                "name": unit.name,
                "patch_image_url": unit.patch_image_url,
                "last_updated": unit.last_updated.isoformat() if unit.last_updated else None
            }
            for unit in units
        ],
        "total": len(units),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/metrics/summary")
async def get_metrics_summary(
    unit_id: str = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get risk metrics summary for dashboard"""
    from datetime import timedelta

    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Base query
    query = db.query(Flight).filter(
        Flight.flight_date >= start_date,
        Flight.flight_date <= end_date
    )

    if unit_id:
        query = query.filter(Flight.unit_id == unit_id)

    flights = query.all()

    # Calculate metrics
    total_flights = len(flights)
    if total_flights == 0:
        return {
            "data": {
                "total_flights": 0,
                "risk_distribution": {"low": 0, "medium": 0, "high": 0, "extreme": 0},
                "average_risk_score": 0,
                "approval_rate": 0
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    risk_distribution = {"low": 0, "medium": 0, "high": 0, "extreme": 0}
    total_risk_score = 0
    approved_count = 0

    for flight in flights:
        risk_distribution[flight.risk_tier.value] += 1
        total_risk_score += flight.total_risk_score
        if flight.is_approved:
            approved_count += 1

    return {
        "data": {
            "total_flights": total_flights,
            "risk_distribution": risk_distribution,
            "average_risk_score": round(total_risk_score / total_flights, 2),
            "approval_rate": round((approved_count / total_flights) * 100, 2),
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/orm/submit")
async def submit_orm(
    orm_data: dict,
    db: Session = Depends(get_db)
):
    """
    Submit ORM data from mobile app
    This is a simplified version - will be enhanced with authentication and validation
    """
    return {
        "message": "ORM submission received",
        "status": "success",
        "data": orm_data,
        "timestamp": datetime.utcnow().isoformat()
    }

# Include additional routers
# from .api import auth, flights, metrics
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
# app.include_router(flights.router, prefix="/api/v1/flights", tags=["flights"])
# app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])