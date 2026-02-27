# 🔧 Integration Guide
## How to Use the New Professional Features

**Quick Start:** 5 Steps to Integrate

---

## STEP 1: Run Database Migration (5 minutes)

### Run the migration script:
```bash
cd backend
python migrate_enhancements.py
```

### What it does:
- ✅ Creates 5 new tables
- ✅ Initializes company settings
- ✅ Sets up system defaults
- ✅ Creates first audit log entry

### Verify:
```bash
# Check if tables were created
python -c "from database import engine; from sqlalchemy import inspect; print([t for t in inspect(engine).get_table_names() if t in ['audit_logs', 'notifications', 'user_sessions', 'system_settings', 'company_settings']])"
```

---

## STEP 2: Add Audit Logging (1-2 hours)

### Update `backend/crud.py`:

#### For CREATE operations:
```python
from audit_service import AuditService, get_client_ip, get_user_agent

def create_trip(db: Session, trip: schemas.TripCreate, current_user: models.User, request):
    # Existing code to create trip
    db_trip = models.Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    # NEW: Add audit logging
    audit = AuditService(db)
    audit.log_create(
        user_id=current_user.id,
        table_name="trips",
        record_id=db_trip.id,
        new_values=trip.dict(),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return db_trip
```

#### For UPDATE operations:
```python
def update_trip(db: Session, trip_id: int, trip_update: dict, current_user: models.User, request):
    # Get existing trip
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    
    # NEW: Store old values for audit
    old_values = {
        "client_freight": db_trip.client_freight,
        "vendor_freight": db_trip.vendor_freight,
        # ... other fields
    }
    
    # Update trip
    for key, value in trip_update.items():
        setattr(db_trip, key, value)
    db.commit()
    
    # NEW: Add audit logging
    audit = AuditService(db)
    audit.log_update(
        user_id=current_user.id,
        table_name="trips",
        record_id=trip_id,
        old_values=old_values,
        new_values=trip_update,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return db_trip
```

#### For DELETE operations:
```python
def delete_trip(db: Session, trip_id: int, current_user: models.User, request):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    
    # NEW: Store values before deletion
    old_values = {
        "reference_no": db_trip.reference_no,
        "client_freight": db_trip.client_freight,
        # ... other important fields
    }
    
    # Delete trip
    db.delete(db_trip)
    db.commit()
    
    # NEW: Add audit logging
    audit = AuditService(db)
    audit.log_delete(
        user_id=current_user.id,
        table_name="trips",
        record_id=trip_id,
        old_values=old_values,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return True
```

### Update `backend/main.py` endpoints:

Add `request: Request` parameter to all endpoints:

```python
from fastapi import Request

@app.post("/trips")
def create_trip(
    trip: schemas.TripCreate,
    request: Request,  # NEW: Add this
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_trip(db, trip, current_user, request)  # Pass request
```

---

## STEP 3: Add Data Validation (1-2 hours)

### Update API endpoints in `backend/main.py`:

```python
from validators import Validator, BusinessValidator, ValidationError
from fastapi import HTTPException

@app.post("/trips")
def create_trip(trip_data: dict, ...):
    try:
        # NEW: Validate data before processing
        validated_data = BusinessValidator.validate_trip_data(trip_data)
        
        # Create trip with validated data
        trip = crud.create_trip(db, validated_data, current_user, request)
        return trip
        
    except ValidationError as e:
        # NEW: Return user-friendly error
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Validation Error",
                "field": e.field,
                "message": e.message
            }
        )
    except ValueError as e:
        # Multiple validation errors
        raise HTTPException(status_code=400, detail=str(e))
```

### Add validation to all POST/PUT endpoints:
- `/trips` - Use `BusinessValidator.validate_trip_data()`
- `/payment-requests` - Use `BusinessValidator.validate_payment_request()`
- `/clients` - Validate email, phone
- `/vendors` - Validate email, phone
- `/users` - Use `Validator.validate_password()`

---

## STEP 4: Add Notifications (2-3 hours)

### Create notification endpoints in `backend/main.py`:

```python
from notification_service import NotificationService

@app.get("/notifications")
def get_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user notifications"""
    notif = NotificationService(db)
    notifications = notif.get_user_notifications(
        user_id=current_user.id,
        unread_only=unread_only
    )
    return notifications

@app.get("/notifications/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get count of unread notifications"""
    notif = NotificationService(db)
    count = notif.get_unread_count(user_id=current_user.id)
    return {"count": count}

@app.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Mark notification as read"""
    notif = NotificationService(db)
    success = notif.mark_as_read(notification_id, current_user.id)
    return {"success": success}

@app.put("/notifications/mark-all-read")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Mark all notifications as read"""
    notif = NotificationService(db)
    count = notif.mark_all_as_read(current_user.id)
    return {"marked_read": count}
```

### Add notifications to business logic:

```python
from notification_service import NotificationService, get_admin_user_ids

# When payment request is created
@app.post("/payment-requests")
def create_payment_request(data: dict, ...):
    # Create payment request
    payment_request = crud.create_payment_request(db, data)
    
    # NEW: Notify admins
    notif = NotificationService(db)
    admin_ids = get_admin_user_ids(db)
    notif.notify_payment_request_submitted(
        admin_user_ids=admin_ids,
        vendor_name=payment_request.vendor.name,
        amount=payment_request.requested_amount,
        payment_request_id=payment_request.id
    )
    
    return payment_request

# When payment is approved
@app.put("/payment-requests/{id}/approve")
def approve_payment(id: int, ...):
    # Approve payment
    payment_request = crud.approve_payment_request(db, id)
    
    # NEW: Notify requester
    notif = NotificationService(db)
    notif.notify_payment_approved(
        requester_id=payment_request.requested_by,
        vendor_name=payment_request.vendor.name,
        amount=payment_request.requested_amount
    )
    
    return payment_request
```

---

## STEP 5: Update Frontend (3-4 hours)

### Add Notification Bell to Header:

Create `frontend/src/components/NotificationBell.js`:

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bell } from 'lucide-react';

const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    fetchUnreadCount();
    // Poll every 30 seconds
    const interval = setInterval(fetchUnreadCount, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchUnreadCount = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/notifications/unread-count', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUnreadCount(response.data.count);
    } catch (error) {
      console.error('Error fetching unread count:', error);
    }
  };

  const fetchNotifications = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/notifications?unread_only=true', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`/notifications/${notificationId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchUnreadCount();
      fetchNotifications();
    } catch (error) {
      console.error('Error marking as read:', error);
    }
  };

  const handleBellClick = () => {
    setShowDropdown(!showDropdown);
    if (!showDropdown) {
      fetchNotifications();
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={handleBellClick}
        style={{
          position: 'relative',
          padding: '0.5rem',
          backgroundColor: 'transparent',
          border: 'none',
          cursor: 'pointer'
        }}
      >
        <Bell style={{ height: '1.5rem', width: '1.5rem', color: '#374151' }} />
        {unreadCount > 0 && (
          <span style={{
            position: 'absolute',
            top: '0',
            right: '0',
            backgroundColor: '#dc2626',
            color: 'white',
            borderRadius: '50%',
            padding: '0.125rem 0.375rem',
            fontSize: '0.75rem',
            fontWeight: 'bold'
          }}>
            {unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <div style={{
          position: 'absolute',
          right: '0',
          top: '100%',
          marginTop: '0.5rem',
          width: '20rem',
          maxHeight: '24rem',
          overflow: 'auto',
          backgroundColor: 'white',
          borderRadius: '0.5rem',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          zIndex: 1000
        }}>
          <div style={{
            padding: '1rem',
            borderBottom: '1px solid #e5e7eb',
            fontWeight: '600'
          }}>
            Notifications
          </div>

          {notifications.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>
              No new notifications
            </div>
          ) : (
            notifications.map(notif => (
              <div
                key={notif.id}
                onClick={() => markAsRead(notif.id)}
                style={{
                  padding: '1rem',
                  borderBottom: '1px solid #e5e7eb',
                  cursor: 'pointer',
                  backgroundColor: notif.is_read ? 'white' : '#eff6ff'
                }}
              >
                <div style={{ fontWeight: '500', marginBottom: '0.25rem' }}>
                  {notif.title}
                </div>
                <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                  {notif.message}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '0.25rem' }}>
                  {new Date(notif.created_at).toLocaleString()}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
```

### Add to Layout:

Update `frontend/src/components/Layout.js`:

```javascript
import NotificationBell from './NotificationBell';

// In the header section, add:
<div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
  <NotificationBell />  {/* NEW */}
  <button onClick={handleLogout}>Logout</button>
</div>
```

### Update Error Handling:

Update all forms to show validation errors:

```javascript
const [errors, setErrors] = useState({});

const handleSubmit = async (e) => {
  e.preventDefault();
  setErrors({});  // Clear previous errors
  
  try {
    await axios.post('/trips', tripData);
    toast.success('Trip created successfully!');
  } catch (error) {
    if (error.response?.data?.field) {
      // Validation error
      setErrors({
        [error.response.data.field]: error.response.data.message
      });
      toast.error(error.response.data.message);
    } else {
      toast.error('Failed to create trip');
    }
  }
};

// In form fields:
<input
  name="client_freight"
  value={tripData.client_freight}
  onChange={handleChange}
  style={{
    borderColor: errors.client_freight ? '#dc2626' : '#d1d5db'
  }}
/>
{errors.client_freight && (
  <div style={{ color: '#dc2626', fontSize: '0.875rem', marginTop: '0.25rem' }}>
    {errors.client_freight}
  </div>
)}
```

---

## TESTING CHECKLIST

### ✅ Audit Trail:
- [ ] Create a trip - Check audit_logs table
- [ ] Update a trip - Verify old/new values logged
- [ ] Delete a trip - Confirm deletion logged
- [ ] Login - Check login audit entry
- [ ] View audit trail for a specific record

### ✅ Validation:
- [ ] Try invalid email - Should show error
- [ ] Try invalid phone - Should show error
- [ ] Try negative amount - Should show error
- [ ] Try client_freight < vendor_freight - Should warn
- [ ] Try weak password - Should show requirements

### ✅ Notifications:
- [ ] Create payment request - Admins should be notified
- [ ] Approve payment - Requester should be notified
- [ ] Check notification bell - Should show count
- [ ] Click notification - Should mark as read
- [ ] Mark all as read - Count should go to zero

### ✅ Company Settings:
- [ ] Query company_settings table
- [ ] Update company name
- [ ] Verify changes appear in reports

---

## TROUBLESHOOTING

### Migration fails:
```bash
# Drop and recreate database (CAUTION: Loses data!)
rm backend/pgt_tms.db
python backend/init_database.py
python backend/migrate_enhancements.py
```

### Audit logging not working:
- Check if `request` parameter is passed to CRUD functions
- Verify `audit_logs` table exists
- Check for errors in console

### Notifications not showing:
- Verify `/notifications` endpoint works
- Check browser console for errors
- Ensure NotificationBell component is imported

### Validation errors not displaying:
- Check error response format
- Verify error state is set correctly
- Check console for error details

---

## QUICK REFERENCE

### Import Statements:
```python
# Backend
from audit_service import AuditService, get_client_ip, get_user_agent
from validators import Validator, BusinessValidator, ValidationError
from notification_service import NotificationService, get_admin_user_ids
```

### Common Patterns:
```python
# Audit logging
audit = AuditService(db)
audit.log_create(user_id, "trips", trip.id, trip_data, ip, user_agent)

# Validation
validated = BusinessValidator.validate_trip_data(data)

# Notifications
notif = NotificationService(db)
notif.create_notification(user_id, "Title", "Message", "info")
```

---

## NEXT STEPS

After integration:
1. ✅ Test all features thoroughly
2. ✅ Update user documentation
3. ✅ Train staff on new features
4. ✅ Monitor audit logs
5. ✅ Gather user feedback

---

**You're ready to integrate! Follow these steps and your system will be professional-grade!** 🚀

