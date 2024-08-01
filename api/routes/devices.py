from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.model_db import SessionLocal

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found in DEVICES"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dev = manager_db.DevicesOperations()

@router.get("/all", response_model=List[schemas.Device])
def get_all_devices(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    devices = dev.get_all_devices(db=db, skip=skip, limit=limit)
    return devices

@router.get("/{id}", response_model=schemas.Device)
def get_device(id: int, db: Session = Depends(get_db)):
    return dev.get_device(db=db, id=id)

@router.post("/create", response_model=schemas.Device)
def create_device(device: schemas.Device, db: Session = Depends(get_db)):
    return dev.create_device(db=db, device=device)

@router.put("/update/{id}", response_model=schemas.Device)
def update_device(id: int, device: schemas.Device, db: Session = Depends(get_db)):
    db_device = dev.update_device(db=db, id=id, device=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/delete/{id}", response_model=schemas.Device)
def delete_device(id: int, db: Session = Depends(get_db)):
    db_device = dev.delete_device(db=db, id=id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device