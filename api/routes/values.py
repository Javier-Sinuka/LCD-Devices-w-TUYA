from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import schemas
from api.exceptions import UniqueConstraintViolation, NotFoundException, DatabaseOperationException
from api.model_db import SessionLocal
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from api.manager import values_manager

router = APIRouter(
    prefix="/values",
    tags=["values"],
    responses={404: {"description": "Not found in VALUES"}},
)


def get_db():
    """
    Dependency function to get a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


val = values_manager.ValuesOperations()


@router.get("/all", response_model=List[schemas.Values])
def get_all_values(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all values with pagination.

    Parameters:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        List[schemas.Values]: A list of value records.
    """
    try:
        return val.get_all_values(db=db, skip=skip, limit=limit)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/devices/{device_id}/attributes", response_model=List[int])
def get_attributes_by_device_id(device_id: int, db: Session = Depends(get_db)):
    """
    Get the list of unique attribute IDs associated with a specific device ID.

    Parameters:
        device_id (int): The ID of the device.

    Returns:
        List[int]: A list of unique attribute IDs associated with the device.
    """
    try:
        return val.get_attributes_by_device(db, device_id)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attributes/{attribute_id}/devices", response_model=List[int])
def get_device_ids_by_attribute(attribute_id: int, db: Session = Depends(get_db)):
    """
    Get the unique IDs of devices associated with a specific attribute.

    Parameters:
        attribute_id (int): The ID of the attribute.

    Returns:
        List[int]: A list of unique device IDs associated with the attribute.
    """
    try:
        device_ids = val.get_device_ids_by_attribute(db=db, attribute_id=attribute_id)
        return device_ids
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/devices/{device_id}/attributes/{attribute_id}/values", response_model=List[schemas.ValuesValue])
def get_values_by_device_and_attribute(
    device_id: int,
    attribute_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """
    Get all values associated with a specific Device ID and Attribute ID within a date range.
    """
    try:
        values = val.get_values_by_device_and_attribute_within_dates(db, device_id, attribute_id, start_date, end_date)
        formatted_values = [{"value": value.value, "timestamp": value.timestamp} for value in values]
        return formatted_values
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=schemas.Values)
def get_value(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single value by its ID.

    Parameters:
        id (int): The ID of the value to retrieve.

    Returns:
        schemas.Values: The value record.
    """
    try:
        return val.get_value(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/create", response_model=schemas.Values)
def create_value(values: schemas.ValuesCreate, db: Session = Depends(get_db)):
    """
    Create a new value record.

    Parameters:
        values (schemas.ValuesCreate): The value data to create.

    Returns:
        schemas.Values: The created value record.
    """
    try:
        return val.create_value(db=db, value=values)
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete/{id}", response_model=schemas.Values)
def delete_value(id: int, db: Session = Depends(get_db)):
    """
    Delete a value by its ID.

    Parameters:
        id (int): The ID of the value to delete.

    Returns:
        schemas.Values: The deleted value record.
    """
    try:
        return val.delete_value(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/update/{id}", response_model=schemas.Values)
def update_value(id: int, values: schemas.Values, db: Session = Depends(get_db)):
    """
    Update a value by its ID.

    Parameters:
        id (int): The ID of the value to update.
        values (schemas.Values): The updated value data.

    Returns:
        schemas.Values: The updated value record.
    """
    try:
        return val.update_value(db=db, id=id, value=values)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))