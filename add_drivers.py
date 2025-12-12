"""
Script to add sample drivers to the database.
"""
from backend_service.database import SessionLocal
from backend_service.models import Driver

def add_sample_drivers():
    db = SessionLocal()
    
    # Sample drivers with individual ports
    drivers = [
        Driver(name="Rajesh Kumar", phone="9876543210", vehicle_number="DL-01-AB-1234", driver_port=9001, status="AVAILABLE"),
        Driver(name="Amit Singh", phone="9876543211", vehicle_number="DL-02-CD-5678", driver_port=9002, status="AVAILABLE"),
        Driver(name="Priya Sharma", phone="9876543212", vehicle_number="DL-03-EF-9012", driver_port=9003, status="AVAILABLE"),
        Driver(name="Vikram Patel", phone="9876543213", vehicle_number="DL-04-GH-3456", driver_port=9004, status="AVAILABLE"),
        Driver(name="Sunita Reddy", phone="9876543214", vehicle_number="DL-05-IJ-7890", driver_port=9005, status="AVAILABLE"),
    ]
    
    try:
        # Check if drivers already exist
        existing_count = db.query(Driver).count()
        if existing_count > 0:
            print(f"WARNING: Database already has {existing_count} drivers.")

        
        # Add drivers
        for driver in drivers:
            db.add(driver)
        
        db.commit()
        print(f"Successfully added {len(drivers)} drivers!")
        
        # Display added drivers
        print("\nDrivers in database:")
        all_drivers = db.query(Driver).all()
        for driver in all_drivers:
            print(f"  ID: {driver.id} | {driver.name} | {driver.vehicle_number} | {driver.status}")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_drivers()
