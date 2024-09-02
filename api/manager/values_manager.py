from datetime import datetime
from typing import List, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import and_
from api import model_db, schemas
from api.exceptions import NotFoundException, DatabaseOperationException
from api.manager.manager import ModelManager
from api.schemas import Values

class ValuesOperations(ModelManager):
    def __init__(self):
        super().__init__()

    def get_value(self, db: Session, id: int):
        return self.get_element(db, model_db.Values, id)

    def get_all_values(self, db: Session, skip: int = 0, limit: int = 10):
        try:
            return db.query(model_db.Values).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving all values.") from e

    def get_device_ids_by_attribute(self, db: Session, attribute_id: int) -> List[int]:
        """
        Retrieve the IDs of devices associated with a specific attribute.

        Parameters:
            db (Session): The database session.
            attribute_id (int): The ID of the attribute.

        Returns:
            List[int]: A list of unique device IDs associated with the attribute.
        """
        try:
            device_ids = db.query(model_db.Values.device_id).filter(attribute_id == model_db.Values.attribute_id).distinct().all()
            return [device_id for (device_id,) in device_ids]
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving device IDs by attribute.") from e

    def get_attributes_by_device(self, db: Session, device_id: int) -> List[int]:
        """
        Retrieve the IDs of attributes associated with a specific device.

        Parameters:
            db (Session): The database session.
            device_id (int): The ID of the device.

        Returns:
            List[int]: A list of unique attribute IDs associated with the device.
        """
        try:
            attribute_ids = db.query(model_db.Values.attribute_id).filter(device_id == model_db.Values.device_id).distinct().all()

            return [attribute_id for (attribute_id,) in attribute_ids]
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving attribute IDs by device.") from e

    def get_values_by_device_and_attribute_within_dates(
            self, db: Session, device_id: int, attribute_id: int, start_date: datetime, end_date: datetime
    ) -> list[Type[Values]]:
        """
        Retrieve values associated with a specific Device ID and Attribute ID within a date range.

        Parameters:
            db (Session): The database session.
            device_id (int): The ID of the device.
            attribute_id (int): The ID of the attribute.
            start_date (datetime): The start date for filtering.
            end_date (datetime): The end date for filtering.

        Returns:
            List[model_db.Values]: A list of values within the date range.
        """
        try:
            values = db.query(model_db.Values).filter(
                and_(
                    model_db.Values.device_id == device_id,
                    model_db.Values.attribute_id == attribute_id,
                    model_db.Values.timestamp >= start_date,
                    model_db.Values.timestamp <= end_date
                )
            ).all()

            if not values:
                raise NotFoundException(
                    f"No values found for device_id {device_id} and attribute_id {attribute_id} within the specified dates.")
            return values

        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the values.") from e

    def create_value(self, db: Session, value: schemas.ValuesCreate):
        new_val = model_db.Values(**value.dict())
        return self.create_element(db, new_val)

    def update_value(self, db: Session, id: int, value: schemas.Values):
        val = self.get_value(db, id)
        return self.update_element(db, val, value.dict())

    def delete_value(self, db: Session, id: int):
        val = self.get_value(db, id)
        return self.delete_element(db, val)
