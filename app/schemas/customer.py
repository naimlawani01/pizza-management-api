from typing import Optional
from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    address: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True 