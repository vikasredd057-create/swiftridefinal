from backend_service import models, database
from sqlalchemy.orm import Session

def seed_data():
    db = database.SessionLocal()
    
    try:
        # Check if data exists
        if db.query(models.ProductCategory).first():
            print("Data already seeded.")
            return

        print("Seeding essentials data...")

        # Categories
        cat_snacks = models.ProductCategory(name="Snacks", description="Chips, chocolates, and bites")
        cat_drinks = models.ProductCategory(name="Drinks", description="Water, juices, and sodas")
        cat_meds = models.ProductCategory(name="OTC Meds", description="Over-the-counter essentials")
        cat_tech = models.ProductCategory(name="Tech", description="Chargers and cables")
        
        db.add_all([cat_snacks, cat_drinks, cat_meds, cat_tech])
        db.commit()

        # Stores
        store_711 = models.PartnerStore(
            name="7-Eleven", 
            address="Downtown Market", 
            lat="12.9716", 
            lng="77.5946", 
            contact_info="555-0101"
        )
        store_apollo = models.PartnerStore(
            name="Apollo Pharmacy", 
            address="Indiranagar", 
            lat="12.9784", 
            lng="77.6408", 
            contact_info="555-0102"
        )
        
        db.add_all([store_711, store_apollo])
        db.commit()

        # Products (Driver Carry - No Store ID)
        p_water = models.Product(
            category_id=cat_drinks.id, 
            name="Mineral Water (500ml)", 
            description="Chilled water bottle", 
            price=20, 
            stock_quantity=10
        )
        p_coke = models.Product(
            category_id=cat_drinks.id, 
            name="Coca Cola (330ml)", 
            description="Chilled can", 
            price=40, 
            stock_quantity=5
        )
        p_chips = models.Product(
            category_id=cat_snacks.id, 
            name="Lays Classic", 
            description="Salted chips", 
            price=20, 
            stock_quantity=10
        )
        
        # Products (Store Pickup)
        p_crocin = models.Product(
            category_id=cat_meds.id, 
            name="Crocin Advance", 
            description="For pain relief", 
            price=30, 
            store_id=store_apollo.id,
            is_age_restricted=False
        )
        p_charger = models.Product(
            category_id=cat_tech.id, 
            name="iPhone Cable", 
            description="Lightning to USB", 
            price=200, 
            store_id=store_711.id
        )
        p_usb_c = models.Product(
            category_id=cat_tech.id, 
            name="USB-C Cable", 
            description="Fast charging cable", 
            price=250, 
            store_id=store_711.id
        )
        p_powerbank = models.Product(
            category_id=cat_tech.id, 
            name="Power Bank 10000mAh", 
            description="Portable charger", 
            price=800, 
            store_id=store_711.id
        )
        p_earphones = models.Product(
            category_id=cat_tech.id, 
            name="Wired Earphones", 
            description="3.5mm jack", 
            price=300, 
            store_id=store_711.id
        )
        p_pepsi = models.Product(
            category_id=cat_drinks.id, 
            name="Pepsi (Can)", 
            description="Chilled soda", 
            price=40, 
            stock_quantity=10
        )

        db.add_all([p_water, p_coke, p_pepsi, p_chips, p_crocin, p_charger, p_usb_c, p_powerbank, p_earphones])
        db.commit()
        
        print("Seeding complete!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
