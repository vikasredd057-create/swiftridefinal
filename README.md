# ⚡ SwiftRide - Quick Start Guide ⚡

## 🚀 SUPER SIMPLE START

### Just Double-Click This:
```
start.bat
```

That's it! **One window, all services running in background.**

## 🌐 Access the Application

After starting, open your browser and go to:

### For Users (Book a Ride)
**http://localhost:8000**

### For Drivers (Accept Rides)
- **Rajesh Kumar**: http://localhost:9001
- **Amit Singh**: http://localhost:9002
- **Priya Sharma**: http://localhost:9003
- **Vikram Patel**: http://localhost:9004
- **Sunita Reddy**: http://localhost:9005

## 🛑 Stop All Services

In the window that opened, press **Ctrl+C**

## 📋 What's Running?

When you start, these services run in the background:
- ✅ Backend Service (Port 8001)
- ✅ User Service (Port 8000)
- ✅ 5 Driver Instances (Ports 9001-9005)

**All in ONE window, no multiple PowerShell windows!**

## 🎯 How to Book a Ride

### Method 1: Search Mode (Fast)
1. Open http://localhost:8000
2. Type pickup location (e.g., "Connaught Place")
3. Select from suggestions
4. Type drop-off location (e.g., "India Gate")
5. Select from suggestions
6. See price → Click "REQUEST RIDE"

### Method 2: Map Mode (Visual)
1. Open http://localhost:8000
2. Click "🗺️ BOOK BY MAP" button
3. Click on map for pickup (green marker)
4. Click again for drop-off (red marker)
5. See price → Click "REQUEST RIDE"

## 🚗 How to Accept a Ride (Driver)

1. Open any driver dashboard (e.g., http://localhost:9001)
2. Wait for ride notification (auto-refreshes every 3 seconds)
3. See ride with price and addresses
4. Click "⚡ ACCEPT RIDE ⚡"
5. Complete when done

## 💰 Pricing

- **Base Fare**: ₹50
- **Per KM**: ₹15
- **Example**: 5 km ride = ₹50 + (5 × ₹15) = ₹130

## 🔧 Troubleshooting

### Services won't start
```bash
# Kill any existing Python processes
taskkill /F /IM python.exe

# Try again
start.bat
```

### Can't access URLs
- Wait 5-10 seconds after starting
- Check if services are running (look at the window)
- Try refreshing browser (F5)

### Database errors
```bash
# Recreate database
python recreate_db.py
# Type: yes

# Add drivers
python add_drivers.py
```

## 📊 Features

✅ **Dual Booking Modes** - Search or Map
✅ **Real-time Pricing** - See fare before booking
✅ **Broadcast System** - All drivers notified simultaneously
✅ **Atomic Acceptance** - No double-booking
✅ **Auto-refresh** - Driver dashboards update every 3 seconds
✅ **Flash Theme** - Lightning effects and animations
✅ **PostgreSQL** - All data persisted

## 🗄️ Database Info

- **Database**: swiftride_db
- **User**: postgres
- **Password**: vikas123
- **Tables**: drivers, ride_requests

## 📁 Project Structure

```
swiftfinal/
├── start.bat              ← DOUBLE-CLICK THIS!
├── start_services.py      ← Background launcher
├── backend_service/       ← API & Database
├── user_service/          ← User Interface
├── driver_instance/       ← Driver Dashboards
└── requirements.txt       ← Dependencies
```

## 🎓 Tips

1. **Keep the window open** - Closing it stops all services
2. **Use Search Mode** for speed
3. **Use Map Mode** for visual selection
4. **Open multiple driver dashboards** to see broadcast in action
5. **Check the window** for service status messages

## 🆘 Need Help?

Check these files:
- `SEARCH_MAP_MODES.md` - Detailed search/map guide
- `MAP_PRICING_UPDATE.md` - Pricing system details
- `BROADCAST_GUIDE.md` - Architecture overview

---

## ⚡ REMEMBER ⚡

**To Start**: Double-click `start.bat`
**To Stop**: Press Ctrl+C in the window
**User URL**: http://localhost:8000
**Driver URLs**: http://localhost:9001-9005

**That's all you need to know!** 🚀
