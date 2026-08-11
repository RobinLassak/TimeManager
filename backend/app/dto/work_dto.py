from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class WorkDTO:
    name: str
    project_id: int
    start_date: date
    end_date: date
    description: str = ""
    status: str = "active"
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None