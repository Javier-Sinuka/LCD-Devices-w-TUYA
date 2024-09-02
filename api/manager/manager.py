from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from api.exceptions import UniqueConstraintViolation, NotFoundException, DatabaseOperationException


class ModelManager:
    def __init__(self):
        pass

    def create_element(self, db: Session, element):
        try:
            db.add(element)
            db.commit()
            db.refresh(element)
            return element
        except IntegrityError as e:
            raise UniqueConstraintViolation("Unique constraint violated.") from e
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while creating the element.") from e

    def get_element(self, db: Session, model, id: int):
        try:
            element = db.query(model).filter(model.id == id).first()
            if element is None:
                raise NotFoundException(f"Element with id {id} not found.")
            return element
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the element.") from e

    def update_element(self, db: Session, element, update_data: dict):
        try:
            for key, value in update_data.items():
                setattr(element, key, value)
            db.commit()
            db.refresh(element)
            return element
        except IntegrityError as e:
            raise UniqueConstraintViolation("Unique constraint violated.") from e
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while updating the element.") from e

    def delete_element(self, db: Session, element):
        try:
            if element is None:
                raise NotFoundException("Element not found.")
            db.delete(element)
            db.commit()
            return element
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while deleting the element.") from e