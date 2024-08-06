from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from api import model_db, schemas
from api.exceptions import UniqueConstraintViolation, NotFoundException, DatabaseOperationException

class BaseOperations:
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

class DevicesOperations(BaseOperations):
    def __init__(self):
        super().__init__()

    def get_device(self, db: Session, id: int):
        return self.get_element(db, model_db.Devices, id)

    def get_device_by_unique_id(self, db: Session, unique_id: str):
        try:
            device = db.query(model_db.Devices).filter(unique_id == model_db.Devices.unique_device_id).first()
            if device is None:
                raise NotFoundException(f"Device with unique_id {unique_id} not found.")
            return device
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the device.") from e

    def get_all_devices(self, db: Session, skip: int = 0, limit: int = 100):
        try:
            return db.query(model_db.Devices).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving all devices.") from e

    def create_device(self, db: Session, device: schemas.DeviceCreate):
        dev = model_db.Devices(**device.model_dump())
        return self.create_element(db, dev)

    def update_device(self, db: Session, id: int, device: schemas.Device):
        dev = self.get_device(db, id)
        return self.update_element(db, dev, device.dict())

    def delete_device(self, db: Session, id: int):
        dev = self.get_device(db, id)
        return self.delete_element(db, dev)

class AttributesOperations(BaseOperations):
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

    def create_attribute(self, db: Session, attribute: schemas.AttributesCreate):
        new_attr = model_db.Attributes(**attribute.dict())
        return self.create_element(db, new_attr)

    def update_attribute(self, db: Session, id: int, attribute: schemas.Attributes):
        attr = self.get_attribute(db, id)
        return self.update_element(db, attr, attribute.dict())

    def delete_attribute(self, db: Session, id: int):
        attr = self.get_attribute(db, id)
        return self.delete_element(db, attr)

class ValuesOperations(BaseOperations):
    def __init__(self):
        super().__init__()

    def get_value(self, db: Session, id: int):
        return self.get_element(db, model_db.Values, id)

    def get_all_values(self, db: Session, skip: int = 0, limit: int = 10):
        try:
            return db.query(model_db.Values).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving all values.") from e

    def create_value(self, db: Session, value: schemas.ValuesCreate):
        new_val = model_db.Values(**value.dict())
        return self.create_element(db, new_val)

    def update_value(self, db: Session, id: int, value: schemas.Values):
        val = self.get_value(db, id)
        return self.update_element(db, val, value.dict())

    def delete_value(self, db: Session, id: int):
        val = self.get_value(db, id)
        return self.delete_element(db, val)
