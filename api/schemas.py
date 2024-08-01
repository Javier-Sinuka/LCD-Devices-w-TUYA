from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Device(BaseModel):
    name: str
    unique_device_id: str
    manufacturer: str

    class Config:
        from_attributes = True

class Attributes(BaseModel):
    name: str
    unit: Optional[str] = None
    data_type: str

    class Config:
        from_attributes = True

class Values(BaseModel):
    device_id: int
    attribute_id: int
    value: str
    timestamp: datetime

    class Config:
        from_attributes = True