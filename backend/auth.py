from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Use a simpler password context to avoid bcrypt version issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_roles: list):
    def role_checker(current_user: models.User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

# ============================================
# DIRECTOR'S RULE #2: MANAGER IRON WALL (RBAC)
# ============================================

def get_visible_fields_for_role(user_role: models.UserRole, table_name: str) -> list:
    """
    Director's Iron Wall: Define exactly what each role can see
    Manager MUST NEVER see profit columns - only freight in/out
    """
    
    if table_name == "trips":
        if user_role == models.UserRole.ADMIN:
            # Director sees EVERYTHING
            return [
                'id', 'reference_no', 'date', 'vehicle_id', 'vehicle_number',
                'category_product', 'source_location', 'destination_location',
                'driver_operator', 'client_id', 'client_name', 'vendor_id', 'vendor_name',
                'freight_mode', 'total_tonnage', 'tonnage', 'rate_per_ton',
                'vendor_freight', 'client_freight', 'local_shifting_charges',
                'advance_paid', 'fuel_cost', 'munshiyana_bank_charges', 'other_expenses',
                'gross_profit', 'net_profit', 'profit_margin',  # ✅ PROFIT VISIBLE
                'status', 'notes', 'created_at'
            ]
        
        elif user_role == models.UserRole.MANAGER:
            # Manager sees operations ONLY - NO PROFIT
            return [
                'id', 'reference_no', 'date', 'vehicle_id', 'vehicle_number',
                'category_product', 'source_location', 'destination_location',
                'driver_operator', 'client_id', 'client_name', 'vendor_id', 'vendor_name',
                'freight_mode', 'total_tonnage', 'tonnage', 'rate_per_ton',
                'vendor_freight', 'client_freight', 'local_shifting_charges',
                'advance_paid', 'fuel_cost', 'munshiyana_bank_charges', 'other_expenses',
                # ❌ gross_profit HIDDEN
                # ❌ net_profit HIDDEN
                # ❌ profit_margin HIDDEN
                'status', 'notes', 'created_at'
            ]
        
        elif user_role == models.UserRole.SUPERVISOR:
            # Supervisor sees minimal data - NO PROFIT, NO FREIGHT DETAILS
            return [
                'id', 'reference_no', 'date', 'vehicle_id', 'vehicle_number',
                'category_product', 'source_location', 'destination_location',
                'driver_operator', 'client_name', 'vendor_name',
                'total_tonnage', 'status', 'notes', 'created_at'
                # ❌ client_freight HIDDEN
                # ❌ vendor_freight HIDDEN
                # ❌ ALL profit fields HIDDEN
            ]
    
    # Default: return all fields (for other tables)
    return []

def filter_trip_data_by_role(trip_data: dict, user_role: models.UserRole) -> dict:
    """
    Filter trip data based on user role
    Used to hide profit columns from Manager and Supervisor
    """
    visible_fields = get_visible_fields_for_role(user_role, "trips")
    
    if not visible_fields:
        return trip_data  # No filtering
    
    # Filter the data
    filtered_data = {}
    for field in visible_fields:
        if field in trip_data:
            filtered_data[field] = trip_data[field]
    
    return filtered_data