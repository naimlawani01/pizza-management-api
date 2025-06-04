from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TimestampModel(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None 
