from datetime import datetime
from typing import List, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from api import model_db, schemas
from api.exceptions import NotFoundException, DatabaseOperationException
from api.manager.manager import ModelManager

class AttributesOperations(ModelManager):
    def __init__(self):
        super().__init__()

    def get_attribute(self, db: Session, id: int):
        return self.get_element(db, model_db.Attributes, id)

    def get_attribute_by_name(self, db: Session, name: str):
        try:
            attribute = db.query(model_db.Attributes).filter(name == model_db.Attributes.name).first()
            if attribute is None:
                raise NotFoundException(f"Attribute with name {name} not found.")
            return attribute
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the attribute.") from e

    def get_all_attributes(self, db: Session, skip: int = 0, limit: int = 10):
        try:
            return db.query(model_db.Attributes).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving all attributes.") from e

    def get_all_attribute_names_and_ids(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve the names and IDs of all attributes.
        """
        try:
            attributes = db.query(model_db.Attributes.id, model_db.Attributes.name).offset(skip).limit(limit).all()
            if not attributes:
                raise NotFoundException("No attributes found.")

            return [{"id": attribute.id, "name": attribute.name} for attribute in attributes]
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving attribute names and IDs.") from e

    def get_attribute_id_by_name(self, db: Session, name: str) -> int:
        """
        Retrieve the ID of a device by its name.
        """
        try:
            attributes_id = db.query(model_db.Attributes.id).filter(name == model_db.Attributes.name).scalar()
            if attributes_id is None:
                raise NotFoundException(f"Attribute with name '{name}' not found.")
            return attributes_id
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the attribute ID.") from e


    def get_attribute_unit_by_id(self, db: Session, id: int) -> str:
        """
        Retrieve the unit of an attribute by its ID.
        """
        try:
            attribute = db.query(model_db.Attributes.unit).filter(id == model_db.Attributes.id).first()
            if attribute is None:
                raise NotFoundException(f"Attribute with id {id} not found.")
            return attribute.unit
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the attribute unit.") from e

    def get_attribute_name_by_id(self, db: Session, id: int) -> str:
        """
        Retrieve the name of an attribute by its ID.
        """
        try:
            attribute = db.query(model_db.Attributes.name).filter(id == model_db.Attributes.id).first()
            if attribute is None:
                raise NotFoundException(f"Attribute with id {id} not found.")
            return attribute.name
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the attribute name.") from e

    def get_attribute_data_type_by_id(self, db: Session, id: int) -> str:
        """
        Retrieve the data type of an attribute by its ID.
        """
        try:
            attribute = db.query(model_db.Attributes.data_type).filter(id == model_db.Attributes.id).first()
            if attribute is None:
                raise NotFoundException(f"Attribute with id {id} not found.")
            return attribute.data_type
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the attribute data type.") from e

    def create_attribute(self, db: Session, attribute: schemas.AttributesCreate):
        new_attr = model_db.Attributes(**attribute.dict())
        return self.create_element(db, new_attr)

    def update_attribute(self, db: Session, id: int, attribute: schemas.Attributes):
        attr = self.get_attribute(db, id)
        return self.update_element(db, attr, attribute.dict())

    def delete_attribute(self, db: Session, id: int):
        attr = self.get_attribute(db, id)
        return self.delete_element(db, attr)