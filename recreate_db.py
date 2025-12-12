"""
Script to recreate the database from scratch.
This will drop all tables and recreate them.
"""
import sys
from backend_service.database import engine, Base
from backend_service.models import *

def recreate_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database recreated successfully!")
    print("\nTables created:")
    print("  - drivers")
    print("  - ride_requests")
    print("\nNext step: Run add_drivers.py to add sample drivers")

if __name__ == "__main__":
    recreate_database()
