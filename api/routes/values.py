from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import manager_db, schemas
from api.model_db import SessionLocal

router = APIRouter(
    prefix="/values",
    tags=["values"],
    responses={404: {"description": "Not found in VALUES"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

val = manager_db.ValuesOperations()

@router.get("/all", response_model=List[schemas.Values])
def get_all_values(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    values = val.get_all_values(db=db, skip=skip, limit=limit)
    return values

@router.get("/{id}", response_model=schemas.Values)
def get_value(id: int, db: Session = Depends(get_db)):
    return val.get_value(db=db, id=id)

@router.post("/create", response_model=schemas.Values)
def create_value(values: schemas.Values, db: Session = Depends(get_db)):
    return val.create_value(db=db, value=values)

@router.delete("/delete/{id}", response_model=schemas.Values)
def delete_value(id: int, db: Session = Depends(get_db)):
    db_value = val.delete_value(db=db, id=id)
    if db_value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return db_value

@router.post("/update/{id}", response_model=schemas.Values)
def update_value(id: int, values: schemas.Values, db: Session = Depends(get_db)):
    db_value = val.update_value(db=db, id=id, value=values)
    if db_value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return db_value