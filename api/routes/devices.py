from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.manager_db import UniqueConstraintViolation, NotFoundException, DatabaseOperationException
from api.model_db import SessionLocal
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    responses={404: {"description": "Not found in DEVICES"}},
)

def get_db():
    """
    Dependency function to provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dev = manager_db.DevicesOperations()

@router.get("/all", response_model=List[schemas.Device])
def get_all_devices(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Retrieve all devices with pagination.

    Parameters:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        List[schemas.Device]: A list of device records.
    """
    try:
        return dev.get_all_devices(db=db, skip=skip, limit=limit)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{id}", response_model=schemas.Device)
def get_device(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a device by its ID.

    Parameters:
        id (int): The ID of the device to retrieve.

    Returns:
        schemas.Device: The device record.
    """
    try:
        return dev.get_device(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get_id/{id}", response_model=schemas.Device)
def get_device_by_unique_id(id: str, db: Session = Depends(get_db)):
    """
    Retrieve a device by its unique device ID.

    Parameters:
        id (str): The unique device ID to retrieve.

    Returns:
        schemas.Device: The device record.
    """
    try:
        return dev.get_device_by_unique_id(db=db, unique_id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/create", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """
    Create a new device record.

    Parameters:
        device (schemas.DeviceCreate): The device data to create.

    Returns:
        schemas.Device: The created device record.
    """
    try:
        return dev.create_device(db=db, device=device)
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update/{id}", response_model=schemas.Device)
def update_device(id: int, device: schemas.Device, db: Session = Depends(get_db)):
    """
    Update a device by its ID.

    Parameters:
        id (int): The ID of the device to update.
        device (schemas.Device): The updated device data.

    Returns:
        schemas.Device: The updated device record.
    """
    try:
        return dev.update_device(db=db, id=id, device=device)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete/{id}", response_model=schemas.Device)
def delete_device(id: int, db: Session = Depends(get_db)):
    """
    Delete a device by its ID.

    Parameters:
        id (int): The ID of the device to delete.

    Returns:
        schemas.Device: The deleted device record.
    """
    try:
        return dev.delete_device(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))