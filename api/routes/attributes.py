from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.model_db import SessionLocal

router = APIRouter(
    prefix="/attributes",
    tags=["attributes"],
    responses={404: {"description": "Not found in ATTRIBUTES"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

attr = manager_db.AttributesOperations()

@router.get("/all", response_model=List[schemas.Attributes])
def get_all_attributes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    attributes = attr.get_all_attributes(db=db, skip=skip, limit=limit)
    return attributes

@router.get("/{id}", response_model=schemas.Attributes)
def get_attribute(id: int, db: Session = Depends(get_db)):
    return attr.get_attribute(db=db, id=id)

@router.post("/create", response_model=schemas.Attributes)
def create_attribute(attribute: schemas.Attributes, db: Session = Depends(get_db)):
    return attr.create_attribute(db=db, attribute=attribute)

@router.delete("/delete/{id}", response_model=schemas.Attributes)
def delete_attribute(id: int, db: Session = Depends(get_db)):
    db_attribute = attr.delete_attribute(db=db, id=id)
    if db_attribute is None:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return db_attribute

@router.post("/update/{id}", response_model=schemas.Attributes)
def update_attribute(id: int, attribute: schemas.Attributes, db: Session = Depends(get_db)):
    db_attribute = attr.update_attribute(db=db, id=id, attribute=attribute)
    if db_attribute is None:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return db_attribute