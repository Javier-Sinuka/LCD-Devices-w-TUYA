from typing import List, Tuple
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import schemas
from api.exceptions import UniqueConstraintViolation, NotFoundException, DatabaseOperationException
from api.model_db import SessionLocal
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from api.manager import devices_manager

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

dev = devices_manager.DevicesOperations()

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

@router.get("/manufacturer/{manufacturer}", response_model=List[schemas.DeviceSummary])
def get_devices_by_manufacturer(manufacturer: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Retrieve all devices by manufacturer with pagination.

    Parameters:
        manufacturer (str): The manufacturer to filter devices by.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        List[schemas.DeviceSummary]: A list of devices' ID and name.
    """
    try:
        return dev.get_devices_by_manufacturer(db=db, manufacturer=manufacturer, skip=skip, limit=limit)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/name/{id}", response_model=str)
def get_device_name_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve the name of a device by its ID.

    Parameters:
        id (int): The ID of the device to retrieve the name.

    Returns:
        str: The name of the device.
    """
    try:
        return dev.get_device_name_by_id(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/names_ids", response_model=List[schemas.DeviceNameID])
def get_all_device_names_and_ids(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Retrieve the names and IDs of all devices with pagination.

    Parameters:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        List[schemas.DeviceNameID]: A list of device records containing IDs and names.
    """
    try:
        return dev.get_all_device_names_and_ids(db=db, skip=skip, limit=limit)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
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