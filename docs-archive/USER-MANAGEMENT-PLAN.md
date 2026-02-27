# User Management & Role-Based Access Control Plan

## Overview
Comprehensive plan for user management with role-based access control (RBAC) for PGT TMS.

## Current System

### Existing Roles
1. **ADMIN** - Full system access
2. **MANAGER** - Financial reports and staff management
3. **SUPERVISOR** - Trip entry and basic operations

### Current User Model
```python
class User:
    - id
    - username
    - email
    - hashed_password
    - full_name
    - role (ADMIN/MANAGER/SUPERVISOR)
    - is_active
    - created_at
```

## Proposed Role-Based Access Control

### Role Hierarchy

```
ADMIN (CEO/Owner)
├─ Full system access
├─ User management
├─ Financial reports with profit
├─ System configuration
└─ All permissions

MANAGER (Operations Manager/Accountant)
├─ Financial reports (no profit details)
├─ Approve payments
├─ View all ledgers
├─ Manage receivables/payables
├─ Generate reports
└─ Cannot: Create users, see profit margins

SUPERVISOR (Operations Supervisor)
├─ Create/edit trips
├─ View fleet operations
├─ Basic reports
├─ Cannot: Approve payments, see financials, manage users

OPERATOR (Data Entry)
├─ Create trips only
├─ View assigned trips
├─ Cannot: Edit, delete, see reports
└─ Limited access
```

## Detailed Permissions Matrix

### Module: User Management
| Action | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|--------|-------|---------|------------|----------|
| Create User | ✅ | ❌ | ❌ | ❌ |
| Edit User | ✅ | ❌ | ❌ | ❌ |
| Delete User | ✅ | ❌ | ❌ | ❌ |
| View Users | ✅ | ❌ | ❌ | ❌ |
| Change Roles | ✅ | ❌ | ❌ | ❌ |

### Module: Fleet Operations
| Action | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|--------|-------|---------|------------|----------|
| Create Trip | ✅ | ✅ | ✅ | ✅ |
| Edit Trip | ✅ | ✅ | ✅ | ❌ |
| Delete Trip | ✅ | ❌ | ❌ | ❌ |
| Cancel Trip | ✅ | ✅ | ❌ | ❌ |
| View All Trips | ✅ | ✅ | ✅ | Own only |
| Complete Trip | ✅ | ✅ | ✅ | ❌ |

### Module: Financial Management
| Action | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|--------|-------|---------|------------|----------|
| View Profit | ✅ | ❌ | ❌ | ❌ |
| View Revenue | ✅ | ✅ | ❌ | ❌ |
| View Costs | ✅ | ✅ | ❌ | ❌ |
| Approve Payments | ✅ | ✅ | ❌ | ❌ |
| Record Collections | ✅ | ✅ | ❌ | ❌ |
| View Ledgers | ✅ | ✅ | ❌ | ❌ |

### Module: Reports
| Action | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|--------|-------|---------|------------|----------|
| Vendor Reports | ✅ | ✅ | ❌ | ❌ |
| Client Reports | ✅ | ✅ | ❌ | ❌ |
| Financial Ledgers | ✅ | ✅ | ❌ | ❌ |
| Profit Reports | ✅ | ❌ | ❌ | ❌ |
| Trip Reports | ✅ | ✅ | ✅ | Own only |
| Export Excel | ✅ | ✅ | ❌ | ❌ |

### Module: Master Data
| Action | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|--------|-------|---------|------------|----------|
| Add Vehicle | ✅ | ✅ | ❌ | ❌ |
| Add Client | ✅ | ✅ | ✅ | ❌ |
| Add Vendor | ✅ | ✅ | ✅ | ❌ |
| Edit Master Data | ✅ | ✅ | ❌ | ❌ |
| Delete Master Data | ✅ | ❌ | ❌ | ❌ |

### Module: Dashboard
| View | ADMIN | MANAGER | SUPERVISOR | OPERATOR |
|------|-------|---------|------------|----------|
| Revenue Metrics | ✅ | ✅ | ❌ | ❌ |
| Profit Metrics | ✅ | ❌ | ❌ | ❌ |
| Trip Count | ✅ | ✅ | ✅ | ✅ |
| Outstanding | ✅ | ✅ | ❌ | ❌ |
| Fleet Status | ✅ | ✅ | ✅ | ❌ |

## Implementation Plan

### Phase 1: Backend Enhancement (Priority: HIGH)

#### 1.1 Add OPERATOR Role
```python
class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    OPERATOR = "operator"  # NEW
```

#### 1.2 Create Permission Decorator
```python
def require_permission(permission: str):
    """Decorator to check user permissions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not has_permission(current_user, permission):
                raise HTTPException(403, "Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

#### 1.3 Permission Checking Function
```python
def has_permission(user: User, permission: str) -> bool:
    """Check if user has specific permission"""
    permissions = {
        UserRole.ADMIN: ["*"],  # All permissions
        UserRole.MANAGER: [
            "view_financials",
            "approve_payments",
            "manage_trips",
            "view_reports",
            "manage_master_data"
        ],
        UserRole.SUPERVISOR: [
            "create_trip",
            "edit_trip",
            "view_trips",
            "add_client",
            "add_vendor"
        ],
        UserRole.OPERATOR: [
            "create_trip",
            "view_own_trips"
        ]
    }
    
    user_perms = permissions.get(user.role, [])
    return "*" in user_perms or permission in user_perms
```

### Phase 2: Frontend User Management UI (Priority: HIGH)

#### 2.1 Settings Page - User Management Tab
Add new tab in Settings page with:
- User list table
- Add user button
- Edit/Delete actions
- Role assignment dropdown
- Active/Inactive toggle

#### 2.2 User Management Features
```javascript
Features:
- Create new user
- Edit user details
- Change user role
- Activate/Deactivate user
- Delete user (with confirmation)
- Reset password
- View user activity log
```

### Phase 3: UI Permission Control (Priority: MEDIUM)

#### 3.1 Hide/Show Based on Role
```javascript
// Example: Hide profit for non-admin
{user.role === 'ADMIN' && (
  <div>Profit: {formatCurrency(profit)}</div>
)}

// Example: Disable edit for operator
<button 
  disabled={user.role === 'OPERATOR'}
  onClick={handleEdit}
>
  Edit Trip
</button>
```

#### 3.2 Route Protection
```javascript
// Protect routes based on role
<ProtectedRoute 
  path="/user-management" 
  requiredRole="ADMIN"
>
  <UserManagement />
</ProtectedRoute>
```

### Phase 4: Audit Trail (Priority: LOW)

#### 4.1 User Activity Logging
```python
class UserActivity(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String)  # "created_trip", "approved_payment"
    module = Column(String)  # "fleet_operations", "payables"
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=func.now())
```

## User Management UI Design

### User List View
```
┌─────────────────────────────────────────────────────────┐
│ User Management                          [+ Add User]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Username    │ Full Name  │ Role       │ Status    │ │
│ ├────────────────────────────────────────────────────┤ │
│ │ admin       │ Admin      │ ADMIN      │ Active  ✓ │ │
│ │ waqar       │ Waqar Sajid│ MANAGER    │ Active  ✓ │ │
│ │ muhammad    │ Muhammad   │ SUPERVISOR │ Active  ✓ │ │
│ │ operator1   │ Ali Khan   │ OPERATOR   │ Active  ✓ │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ Actions: [Edit] [Delete] [Reset Password]               │
└─────────────────────────────────────────────────────────┘
```

### Add/Edit User Form
```
┌─────────────────────────────────────────┐
│ Add New User                      [X]   │
├─────────────────────────────────────────┤
│                                          │
│ Username: [________________]            │
│ Full Name: [________________]           │
│ Email: [________________]               │
│ Password: [________________]            │
│ Confirm Password: [________________]    │
│                                          │
│ Role: [▼ Select Role]                   │
│   - Administrator (Full Access)         │
│   - Manager (Financial & Reports)       │
│   - Supervisor (Operations)             │
│   - Operator (Data Entry Only)          │
│                                          │
│ Status: [✓] Active                      │
│                                          │
│ [Cancel]              [Create User]     │
└─────────────────────────────────────────┘
```

## Security Considerations

### Password Policy
- Minimum 8 characters
- Must include: uppercase, lowercase, number
- Password hashing with bcrypt
- Password expiry (optional): 90 days
- Cannot reuse last 3 passwords

### Session Management
- JWT token with expiration
- Auto-logout after 8 hours
- Refresh token mechanism
- Single session per user (optional)

### Access Control
- Check permissions on every API call
- Frontend hiding is not security
- Backend must enforce all permissions
- Log all permission denials

## Recommended Role Assignment

### For PGT International

#### CEO/Owner
- **Role**: ADMIN
- **Access**: Everything
- **Purpose**: Full control, profit visibility

#### Operations Manager
- **Role**: MANAGER
- **Access**: Operations + Financial (no profit)
- **Purpose**: Day-to-day management

#### Accountant
- **Role**: MANAGER
- **Access**: Financial reports, payments
- **Purpose**: Financial management

#### Operations Supervisor
- **Role**: SUPERVISOR
- **Access**: Trip creation, basic operations
- **Purpose**: Field operations

#### Data Entry Staff
- **Role**: OPERATOR
- **Access**: Create trips only
- **Purpose**: Data entry

## Implementation Steps

### Step 1: Backend (Week 1)
1. Add OPERATOR role to UserRole enum
2. Create permission checking functions
3. Add permission decorators to API endpoints
4. Test all endpoints with different roles

### Step 2: User Management UI (Week 1)
1. Add User Management tab in Settings
2. Create user list component
3. Create add/edit user form
4. Implement delete user functionality
5. Add role assignment dropdown

### Step 3: Permission Enforcement (Week 2)
1. Hide/show UI elements based on role
2. Disable actions based on permissions
3. Add route protection
4. Test all scenarios

### Step 4: Testing & Documentation (Week 2)
1. Test each role thoroughly
2. Document permissions
3. Create user guide
4. Train staff on roles

## Benefits

### Security
- ✅ Controlled access to sensitive data
- ✅ Profit information protected
- ✅ Prevent unauthorized actions
- ✅ Audit trail for accountability

### Operational
- ✅ Clear role definitions
- ✅ Appropriate access levels
- ✅ Reduced errors
- ✅ Better workflow

### Management
- ✅ Easy user management
- ✅ Flexible role assignment
- ✅ Activity monitoring
- ✅ Compliance ready

## Next Steps

1. **Review & Approve**: Review this plan and approve
2. **Prioritize**: Decide which features are most important
3. **Implement**: Start with Phase 1 (Backend)
4. **Test**: Thoroughly test each role
5. **Deploy**: Roll out to production
6. **Train**: Train staff on new system

## Questions to Consider

1. **Do you need OPERATOR role?** Or is SUPERVISOR enough?
2. **Should MANAGER see profit?** Or only ADMIN?
3. **Password policy?** How strict should it be?
4. **Session timeout?** How long should users stay logged in?
5. **Audit trail?** Do you need detailed activity logs?

---

**Recommendation**: Start with 3 roles (ADMIN, MANAGER, SUPERVISOR) and add OPERATOR later if needed. Keep it simple initially.
