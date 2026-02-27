"""
Data Validation Utilities
Comprehensive validation for all user inputs
"""

import re
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class Validator:
    """Comprehensive data validator"""
    
    # Regex patterns
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN_PK = r'^\+?92-?3[0-9]{2}-?[0-9]{7}$'  # Pakistan mobile
    PHONE_PATTERN_GENERAL = r'^\+?[0-9]{10,15}$'  # General international
    
    @staticmethod
    def validate_required(value: Any, field_name: str) -> Any:
        """Validate that a field is not empty"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValidationError(field_name, "This field is required")
        return value
    
    @staticmethod
    def validate_email(email: Optional[str], field_name: str = "email", required: bool = True) -> Optional[str]:
        """Validate email format"""
        if not email or email.strip() == "":
            if required:
                raise ValidationError(field_name, "Email is required")
            return None
        
        email = email.strip().lower()
        if not re.match(Validator.EMAIL_PATTERN, email):
            raise ValidationError(field_name, "Invalid email format")
        
        return email
    
    @staticmethod
    def validate_phone(phone: Optional[str], field_name: str = "phone", required: bool = False) -> Optional[str]:
        """Validate phone number format"""
        if not phone or phone.strip() == "":
            if required:
                raise ValidationError(field_name, "Phone number is required")
            return None
        
        phone = phone.strip()
        # Remove spaces and dashes for validation
        phone_clean = phone.replace(" ", "").replace("-", "")
        
        # Try Pakistan format first, then general
        if not (re.match(Validator.PHONE_PATTERN_PK, phone_clean) or 
                re.match(Validator.PHONE_PATTERN_GENERAL, phone_clean)):
            raise ValidationError(
                field_name, 
                "Invalid phone format. Use: +92-3XX-XXXXXXX or +XX-XXXXXXXXXX"
            )
        
        return phone
    
    @staticmethod
    def validate_positive_number(
        value: Any, 
        field_name: str, 
        allow_zero: bool = False,
        required: bool = True
    ) -> Optional[float]:
        """Validate positive number"""
        if value is None or value == "":
            if required:
                raise ValidationError(field_name, "This field is required")
            return None
        
        try:
            num = float(value)
        except (ValueError, TypeError):
            raise ValidationError(field_name, "Must be a valid number")
        
        if allow_zero:
            if num < 0:
                raise ValidationError(field_name, "Must be zero or positive")
        else:
            if num <= 0:
                raise ValidationError(field_name, "Must be greater than zero")
        
        return num
    
    @staticmethod
    def validate_amount(
        value: Any,
        field_name: str,
        min_amount: float = 0,
        max_amount: Optional[float] = None,
        required: bool = True
    ) -> Optional[float]:
        """Validate monetary amount"""
        if value is None or value == "":
            if required:
                raise ValidationError(field_name, "Amount is required")
            return None
        
        try:
            amount = float(value)
        except (ValueError, TypeError):
            raise ValidationError(field_name, "Invalid amount format")
        
        if amount < min_amount:
            raise ValidationError(field_name, f"Amount must be at least {min_amount}")
        
        if max_amount and amount > max_amount:
            raise ValidationError(field_name, f"Amount cannot exceed {max_amount}")
        
        # Check for reasonable decimal places (2 for currency)
        if round(amount, 2) != amount:
            raise ValidationError(field_name, "Amount can have maximum 2 decimal places")
        
        return amount
    
    @staticmethod
    def validate_date(
        value: Any,
        field_name: str,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
        required: bool = True
    ) -> Optional[date]:
        """Validate date"""
        if value is None:
            if required:
                raise ValidationError(field_name, "Date is required")
            return None
        
        # Convert string to date if needed
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(field_name, "Invalid date format. Use YYYY-MM-DD")
        
        if isinstance(value, datetime):
            value = value.date()
        
        if not isinstance(value, date):
            raise ValidationError(field_name, "Invalid date")
        
        if min_date and value < min_date:
            raise ValidationError(field_name, f"Date cannot be before {min_date}")
        
        if max_date and value > max_date:
            raise ValidationError(field_name, f"Date cannot be after {max_date}")
        
        return value
    
    @staticmethod
    def validate_date_range(
        start_date: Any,
        end_date: Any,
        start_field: str = "start_date",
        end_field: str = "end_date"
    ) -> tuple:
        """Validate date range (start must be before end)"""
        start = Validator.validate_date(start_date, start_field)
        end = Validator.validate_date(end_date, end_field)
        
        if start and end and start > end:
            raise ValidationError(end_field, "End date must be after start date")
        
        return start, end
    
    @staticmethod
    def validate_string_length(
        value: Optional[str],
        field_name: str,
        min_length: int = 0,
        max_length: Optional[int] = None,
        required: bool = True
    ) -> Optional[str]:
        """Validate string length"""
        if not value or value.strip() == "":
            if required:
                raise ValidationError(field_name, "This field is required")
            return None
        
        value = value.strip()
        length = len(value)
        
        if length < min_length:
            raise ValidationError(field_name, f"Must be at least {min_length} characters")
        
        if max_length and length > max_length:
            raise ValidationError(field_name, f"Cannot exceed {max_length} characters")
        
        return value
    
    @staticmethod
    def validate_choice(
        value: Any,
        field_name: str,
        choices: List[Any],
        required: bool = True
    ) -> Optional[Any]:
        """Validate value is in allowed choices"""
        if value is None or value == "":
            if required:
                raise ValidationError(field_name, "This field is required")
            return None
        
        if value not in choices:
            raise ValidationError(
                field_name,
                f"Invalid choice. Must be one of: {', '.join(map(str, choices))}"
            )
        
        return value
    
    @staticmethod
    def validate_percentage(
        value: Any,
        field_name: str,
        required: bool = True
    ) -> Optional[float]:
        """Validate percentage (0-100)"""
        if value is None or value == "":
            if required:
                raise ValidationError(field_name, "Percentage is required")
            return None
        
        try:
            pct = float(value)
        except (ValueError, TypeError):
            raise ValidationError(field_name, "Invalid percentage format")
        
        if pct < 0 or pct > 100:
            raise ValidationError(field_name, "Percentage must be between 0 and 100")
        
        return pct
    
    @staticmethod
    def validate_password(
        password: str,
        field_name: str = "password",
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True
    ) -> str:
        """Validate password strength"""
        if not password:
            raise ValidationError(field_name, "Password is required")
        
        if len(password) < min_length:
            raise ValidationError(field_name, f"Password must be at least {min_length} characters")
        
        errors = []
        
        if require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("one uppercase letter")
        
        if require_lowercase and not re.search(r'[a-z]', password):
            errors.append("one lowercase letter")
        
        if require_digit and not re.search(r'\d', password):
            errors.append("one number")
        
        if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("one special character (!@#$%^&*)")
        
        if errors:
            raise ValidationError(
                field_name,
                f"Password must contain at least: {', '.join(errors)}"
            )
        
        return password
    
    @staticmethod
    def validate_unique_reference(
        db,
        model,
        field_name: str,
        value: str,
        exclude_id: Optional[int] = None
    ) -> str:
        """Validate that a reference number is unique"""
        query = db.query(model).filter(getattr(model, field_name) == value)
        
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        
        if query.first():
            raise ValidationError(field_name, f"This {field_name} already exists")
        
        return value

# Business Logic Validators
class BusinessValidator:
    """Business-specific validation rules"""
    
    @staticmethod
    def validate_trip_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trip creation/update data"""
        errors = []
        
        try:
            # Required fields
            Validator.validate_required(data.get('date'), 'date')
            Validator.validate_required(data.get('reference_no'), 'reference_no')
            Validator.validate_required(data.get('vehicle_id'), 'vehicle_id')
            Validator.validate_required(data.get('client_id'), 'client_id')
            Validator.validate_required(data.get('vendor_id'), 'vendor_id')
            
            # Financial validation
            client_freight = Validator.validate_amount(
                data.get('client_freight'),
                'client_freight',
                min_amount=0
            )
            
            vendor_freight = Validator.validate_amount(
                data.get('vendor_freight'),
                'vendor_freight',
                min_amount=0
            )
            
            # Business rule: Client freight should be >= vendor freight
            if client_freight and vendor_freight and client_freight < vendor_freight:
                errors.append(ValidationError(
                    'client_freight',
                    'Client freight should not be less than vendor freight (negative profit)'
                ))
            
            # Validate tonnage based on freight mode
            freight_mode = data.get('freight_mode', 'total')
            if freight_mode == 'per_ton':
                Validator.validate_positive_number(
                    data.get('tonnage'),
                    'tonnage',
                    required=True
                )
                Validator.validate_positive_number(
                    data.get('rate_per_ton'),
                    'rate_per_ton',
                    required=True
                )
            
            # Validate total tonnage
            Validator.validate_positive_number(
                data.get('total_tonnage'),
                'total_tonnage',
                required=True
            )
            
        except ValidationError as e:
            errors.append(e)
        
        if errors:
            raise ValueError({
                "validation_errors": [
                    {"field": e.field, "message": e.message}
                    for e in errors
                ]
            })
        
        return data
    
    @staticmethod
    def validate_payment_request(data: Dict[str, Any], payable_outstanding: float) -> Dict[str, Any]:
        """Validate payment request data"""
        errors = []
        
        try:
            # Validate amount
            requested_amount = Validator.validate_amount(
                data.get('requested_amount'),
                'requested_amount',
                min_amount=0.01
            )
            
            # Business rule: Cannot request more than outstanding
            if requested_amount > payable_outstanding:
                errors.append(ValidationError(
                    'requested_amount',
                    f'Cannot request more than outstanding amount ({payable_outstanding})'
                ))
            
            # Validate payment type
            payment_type = Validator.validate_choice(
                data.get('payment_type'),
                'payment_type',
                choices=['full', 'partial']
            )
            
            # Business rule: Full payment must equal outstanding
            if payment_type == 'full' and requested_amount != payable_outstanding:
                errors.append(ValidationError(
                    'requested_amount',
                    f'Full payment must equal outstanding amount ({payable_outstanding})'
                ))
            
        except ValidationError as e:
            errors.append(e)
        
        if errors:
            raise ValueError({
                "validation_errors": [
                    {"field": e.field, "message": e.message}
                    for e in errors
                ]
            })
        
        return data
