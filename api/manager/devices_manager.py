from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from api import model_db, schemas
from api.exceptions import NotFoundException, DatabaseOperationException
from api.manager.manager import ModelManager


class DevicesOperations(ModelManager):
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

    def get_devices_by_manufacturer(self, db: Session, manufacturer: str, skip: int = 0, limit: int = 100):
        """
        Retrieve devices by manufacturer.
        """
        try:
            devices = (
                db.query(model_db.Devices.id, model_db.Devices.name)
                .filter(manufacturer == model_db.Devices.manufacturer)
                .offset(skip)
                .limit(limit)
                .all()
            )
            if not devices:
                raise NotFoundException(f"No devices found for manufacturer: {manufacturer}")
            return devices
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving devices by manufacturer.") from e

    def get_device_name_by_id(self, db: Session, id: int) -> str:
        """
        Retrieve the name of a device by its ID.
        """
        try:
            device_name = db.query(model_db.Devices.name).filter(id == model_db.Devices.id).first()
            if device_name is None:
                raise NotFoundException(f"Device with id {id} not found.")
            return device_name[0]  # `device_name` es una tupla, extraemos el primer valor
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving the device name.") from e

    def get_all_device_names_and_ids(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve the names and IDs of all devices.
        """
        try:
            devices = db.query(model_db.Devices.id, model_db.Devices.name).offset(skip).limit(limit).all()
            if not devices:
                raise NotFoundException("No devices found.")

            return [{"id": device.id, "name": device.name} for device in devices]
        except SQLAlchemyError as e:
            raise DatabaseOperationException("An error occurred while retrieving device names and IDs.") from e

    def create_device(self, db: Session, device: schemas.DeviceCreate):
        dev = model_db.Devices(**device.model_dump())
        return self.create_element(db, dev)

    def update_device(self, db: Session, id: int, device: schemas.Device):
        dev = self.get_device(db, id)
        return self.update_element(db, dev, device.dict())

    def delete_device(self, db: Session, id: int):
        dev = self.get_device(db, id)
        return self.delete_element(db, dev)