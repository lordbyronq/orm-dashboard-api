#!/usr/bin/env python3
"""
Database initialization script for ORM Dashboard API
Creates sample data for development and testing
"""

import os
import sys
import uuid
from datetime import datetime, timedelta

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Base, Flight, Unit, User, UserRole, SeverityLevel

def create_tables():
    """Create all database tables"""
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

def create_sample_data():
    """Create sample data for development"""
    print("📊 Creating sample data...")

    db = SessionLocal()
    try:
        # Sample units
        units = [
            Unit(
                id="ea37b_55ecg",
                name="55th Electronic Combat Group (EA-37B)",
                patch_image_url="https://example.com/55ecg_patch.png",
                checklist_url="https://raw.githubusercontent.com/lordbyronq/Worksheet_hub/refs/heads/main/EA-37B-Worksheet.json",
                orm_matrix={"version": "1.1", "platform": "EA-37B"}
            ),
            Unit(
                id="ec130h_41ecs",
                name="41st Expeditionary Combat Squadron (EC-130H)",
                patch_image_url="https://example.com/41ecs_patch.png",
                checklist_url="https://raw.githubusercontent.com/lordbyronq/Worksheet_hub/refs/heads/main/EC-130H-Worksheet.json",
                orm_matrix={"version": "2.0", "platform": "EC-130H"}
            ),
            Unit(
                id="f16_388fw",
                name="388th Fighter Wing (F-16C)",
                patch_image_url="https://example.com/388fw_patch.png",
                checklist_url="https://example.com/f16_worksheet.json",
                orm_matrix={"version": "1.3", "platform": "F-16C"}
            )
        ]

        for unit in units:
            existing = db.query(Unit).filter(Unit.id == unit.id).first()
            if not existing:
                db.add(unit)

        # Sample admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            name="Admin User",
            email="admin@military.mil",
            role=UserRole.ADMIN,
            unit_access=["ea37b_55ecg", "ec130h_41ecs", "f16_388fw"],
            can_export=True,
            can_view_historical=True,
            can_view_pii=True,
            is_active=True
        )

        existing_admin = db.query(User).filter(User.email == admin_user.email).first()
        if not existing_admin:
            db.add(admin_user)

        # Sample flights with various risk levels
        base_date = datetime.utcnow()
        sample_flights = [
            Flight(
                id=str(uuid.uuid4()),
                unit_id="ea37b_55ecg",
                callsign="SHADOW01",
                aircraft_type="EA-37B",
                tail_number="87-0001",
                mission_type="Electronic Warfare",
                aircraft_commander="Maj Smith",
                flight_date=base_date - timedelta(hours=2),
                total_risk_score=15,
                risk_tier=SeverityLevel.MEDIUM,
                approval_by="Squadron Commander",
                is_briefed=True,
                is_approved=True,
                crew_count=4
            ),
            Flight(
                id=str(uuid.uuid4()),
                unit_id="ec130h_41ecs",
                callsign="COMMANDO99",
                aircraft_type="EC-130H",
                tail_number="73-1234",
                mission_type="Command & Control",
                aircraft_commander="Lt Col Jones",
                flight_date=base_date - timedelta(hours=1),
                total_risk_score=8,
                risk_tier=SeverityLevel.LOW,
                approval_by="Operations Officer",
                is_briefed=True,
                is_approved=True,
                crew_count=6
            ),
            Flight(
                id=str(uuid.uuid4()),
                unit_id="f16_388fw",
                callsign="VIPER03",
                aircraft_type="F-16C",
                tail_number="88-0567",
                mission_type="Combat Air Patrol",
                aircraft_commander="Capt Davis",
                flight_date=base_date - timedelta(minutes=30),
                total_risk_score=22,
                risk_tier=SeverityLevel.HIGH,
                approval_by="Wing Commander",
                is_briefed=True,
                is_approved=True,
                crew_count=1
            ),
            # Historical flights (older than 24 hours - will be sanitized)
            Flight(
                id=str(uuid.uuid4()),
                unit_id="ea37b_55ecg",
                callsign="[REDACTED]",
                aircraft_type="EA-37B",
                tail_number="[REDACTED]",
                mission_type="Electronic Warfare",
                aircraft_commander="[REDACTED]",
                flight_date=base_date - timedelta(days=3),
                total_risk_score=12,
                risk_tier=SeverityLevel.MEDIUM,
                approval_by="Squadron Commander",
                is_briefed=True,
                is_approved=True,
                crew_count=4,
                is_pii_scrubbed=True
            ),
            Flight(
                id=str(uuid.uuid4()),
                unit_id="ec130h_41ecs",
                callsign="[REDACTED]",
                aircraft_type="EC-130H",
                tail_number="[REDACTED]",
                mission_type="Command & Control",
                aircraft_commander="[REDACTED]",
                flight_date=base_date - timedelta(days=7),
                total_risk_score=6,
                risk_tier=SeverityLevel.LOW,
                approval_by="Operations Officer",
                is_briefed=True,
                is_approved=True,
                crew_count=6,
                is_pii_scrubbed=True
            )
        ]

        for flight in sample_flights:
            existing = db.query(Flight).filter(Flight.id == flight.id).first()
            if not existing:
                db.add(flight)

        db.commit()
        print("✅ Sample data created successfully")
        print(f"📊 Created {len(units)} units, 1 admin user, and {len(sample_flights)} sample flights")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
        raise
    finally:
        db.close()

def main():
    print("🚀 Initializing ORM Dashboard Database...")
    create_tables()
    create_sample_data()
    print("✅ Database initialization complete!")
    print("\n🌐 Ready to start the API server:")
    print("   Development: uvicorn app.main:app --reload --port 8000")
    print("   Production:  uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("\n📖 API Documentation available at:")
    print("   http://localhost:8000/docs (development only)")

if __name__ == "__main__":
    main()