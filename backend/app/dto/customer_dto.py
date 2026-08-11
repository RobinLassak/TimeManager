from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CustomerDTO:
    first_name: str
    last_name: str
    ico: str
    dic: str
    street: str
    city: str
    zip: str
    country: str
    email: str
    phone: str
    website: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None