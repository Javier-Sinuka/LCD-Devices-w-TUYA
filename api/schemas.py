from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    name: str
    unique_device_id: str
    manufacturer: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    class Config:
        from_attributes = True

class AttributesBase(BaseModel):
    name: str
    unit: Optional[str] = None
    data_type: str
class AttributesCreate(AttributesBase):
    pass

class Attributes(AttributesBase):
    id: int
    class Config:
        from_attributes = True

class ValuesBase(BaseModel):
    value: str

class ValuesCreate(ValuesBase):
    device_id: int
    attribute_id: int

class Values(ValuesBase):
    id: Optional[int]
    device_id: int
    attribute_id: int
    timestamp: datetime
    class Config:
        from_attributes = True