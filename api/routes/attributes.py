from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.manager_db import UniqueConstraintViolation, NotFoundException, DatabaseOperationException
from api.model_db import SessionLocal
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

router = APIRouter(
    prefix="/attributes",
    tags=["attributes"],
    responses={404: {"description": "Not found in ATTRIBUTES"}},
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

attr = manager_db.AttributesOperations()

@router.get("/all", response_model=List[schemas.Attributes])
def get_all_attributes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Retrieve all attributes with pagination.

    Parameters:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        List[schemas.Attributes]: A list of attribute records.
    """
    try:
        return attr.get_all_attributes(db=db, skip=skip, limit=limit)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{id}", response_model=schemas.Attributes)
def get_attribute(id: int, db: Session = Depends(get_db)):
    """
    Retrieve an attribute by its ID.

    Parameters:
        id (int): The ID of the attribute to retrieve.

    Returns:
        schemas.Attributes: The attribute record.
    """
    try:
        return attr.get_attribute(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get_attribute/{name}", response_model=schemas.Attributes)
def get_attribute_by_name(name: str, db: Session = Depends(get_db)):
    """
    Retrieve an attribute by its name.

    Parameters:
        name (str): The name of the attribute to retrieve.

    Returns:
        schemas.Attributes: The attribute record.
    """
    try:
        return attr.get_attribute_by_name(db=db, name=name)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/create", response_model=schemas.Attributes)
def create_attribute(attribute: schemas.AttributesCreate, db: Session = Depends(get_db)):
    """
    Create a new attribute record.

    Parameters:
        attribute (schemas.AttributesCreate): The attribute data to create.

    Returns:
        schemas.Attributes: The created attribute record.
    """
    try:
        return attr.create_attribute(db=db, attribute=attribute)
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update/{id}", response_model=schemas.Attributes)
def update_attribute(id: int, attribute: schemas.Attributes, db: Session = Depends(get_db)):
    """
    Update an attribute by its ID.

    Parameters:
        id (int): The ID of the attribute to update.
        attribute (schemas.Attributes): The updated attribute data.

    Returns:
        schemas.Attributes: The updated attribute record.
    """
    try:
        return attr.update_attribute(db=db, id=id, attribute=attribute)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except UniqueConstraintViolation as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete/{id}", response_model=schemas.Attributes)
def delete_attribute(id: int, db: Session = Depends(get_db)):
    """
    Delete an attribute by its ID.

    Parameters:
        id (int): The ID of the attribute to delete.

    Returns:
        schemas.Attributes: The deleted attribute record.
    """
    try:
        return attr.delete_attribute(db=db, id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))