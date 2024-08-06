from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.manager_db import UniqueConstraintViolation, NotFoundException, DatabaseOperationException
from api.model_db import SessionLocal
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

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


val = manager_db.ValuesOperations()


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