from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class TimestampModel(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_active: bool = True

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool = True 