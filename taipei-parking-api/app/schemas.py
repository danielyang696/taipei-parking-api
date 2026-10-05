from typing import Optional
from pydantic import BaseModel, Field

class ParkingLotBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    area: Optional[str] = None
    address: Optional[str] = None
    tel: Optional[str] = None
    summary: Optional[str] = None
    payex: Optional[str] = None
    tw97x: Optional[float] = None
    tw97y: Optional[float] = None
    totalcar: Optional[int] = None
    totalmotor: Optional[int] = None
    charging_station: Optional[int] = None

class ParkingLotCreate(ParkingLotBase):
    id: str = Field(..., min_length=1, max_length=100)

class ParkingLotUpdate(ParkingLotBase):
    pass

class ParkingLot(ParkingLotBase):
    id: str
