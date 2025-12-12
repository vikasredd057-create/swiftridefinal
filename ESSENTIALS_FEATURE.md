# Swift Essentials Feature Guide 🛍️

This document outlines the architecture and usage of the "Swift Essentials" monetization feature for SwiftRide.

## 🌟 Overview
Swift Essentials allows riders to add small items (snacks, drinks, meds, etc.) to their ride booking. Drivers can fulfill these in two ways:
1.  **Driver Carry**: Items the driver already has in stock (e.g., Water, Chips).
2.  **Driver Pickup**: Items the driver buys from a partner store on the way (e.g., Meds from Apollo Pharmacy).

## 🏗️ Architecture

### 1. Database Schema
New tables were added to support this feature:
-   `partner_stores`: Locations for item pickup.
-   `product_categories`: Categorization (Snacks, Drinks, Tech, etc.).
-   `products`: Item catalog with price, stock, and linkage to stores.
-   `essentials_orders`: Links a `RideRequest` to a set of items.
-   `essentials_order_items`: Line items for each order.

### 2. Backend Service (`backend_service`)
-   **Endpoints**:
    -   `GET /api/essentials/products`: Fetch catalog.
    -   `POST /api/rides`: Logic updated to process `essentials` field in payload, creating linkage.
    -   `Broadcast`: Logic updated to send essentials details to drivers via WebSocket/HTTP push.
-   **Logic**:
    -   Calculates total price (Ride Fare + Essentials Total).
    -   Determines execution method (`DRIVER_CARRY` or `DRIVER_PICKUP`) based on item source.

### 3. User Service (`user_service`)
-   **UI**:
    -   Added "Swift Essentials" section in the booking interface.
    -   Product Grid with "Add to Cart" functionality.
    -   Cart summary and total price calculation (Fare + Items).
-   **Proxy**:
    -   `GET /api/essentials/products` proxies the request to the backend to avoid CORS issues if typically separated.

### 4. Driver Service (`driver_service` / `driver_instance`)
-   **Dashboard**:
    -   Displays "🛍️ Swift Essentials Included" badge on ride cards.
    -   Lists items and quantities.
    -   Highlights "PICKUP REQUIRED" if items are from a store, showing Store ID/Name.

## 🚀 Usage

### For Users
1.  Open the SwiftRide app.
2.  Enter pickup/dropoff.
3.  Click "Show Catalog" to view essentials.
4.  Add items (e.g., Water, Chips).
5.  Request Ride. The fare includes the item cost.

### For Drivers
1.  Receive a ride request.
2.  Check if it has the "Swift Essentials" badge.
    -   **Green Badge**: You have the stock (Driver Stock). Hand it over.
    -   **Red Badge**: Pickup required. Stop at the indicated store.
3.  Accept and Complete ride as normal.

## 🛠️ Maintenance
-   **Seeding Data**: Run `python seed_essentials.py` to reset the catalog.
-   **Adding Drivers**: Run `python add_drivers.py`.
-   **Reset DB**: Run `python recreate_db.py` (Deletes all data!).
