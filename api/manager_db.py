from sqlalchemy.orm import Session
from . import model_db, schemas

class BaseOperations:
    def __init__(self):
        pass
    def create_element(self, db: Session, element):
        db.add(element)
        db.commit()
        db.refresh(element)
        return element

    def delete_element(self, db: Session, element):
        if element is None:
            return None
        db.delete(element)
        db.commit()
        return element

class DevicesOperations(BaseOperations):
    def __init__(self):
        super().__init__()

    def get_device(self, db: Session, id: int):
        return db.query(model_db.Devices).filter(model_db.Devices.id == id).first()
    # id == model_db.Devices.id
    def get_all_devices(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(model_db.Devices).offset(skip).limit(limit).all()

    def create_device(self, db: Session, device: schemas.Device):
        dev = model_db.Devices(**device.dict())
        return self.create_element(db, dev)

    def update_device(self, db: Session, id: int, device: schemas.Device):
        dev = self.get_device(db, id)
        if dev is None:
            return None
        for key, value in device.dict().items():
            setattr(id, key, value)
        db.commit()
        db.refresh(dev)
        return dev

    def delete_device(self, db: Session, id: int):
        dev = self.get_device(db, id)
        return self.delete_element(db, dev)

class AttributesOperations(BaseOperations):
    def __init__(self):
        super().__init__()

    def get_attribute(self, db: Session, id: int):
        return db.query(model_db.Attributes).filter(model_db.Attributes.id == id).first()

    def get_all_attributes(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(model_db.Attributes).offset(skip).limit(limit).all()

    def create_attribute(self, db: Session, attribute: schemas.Attributes):
        new_attr = model_db.Attributes(**attribute.dict())
        return self.create_element(db, new_attr)

    def update_attribute(self, db: Session, id: int, attribute: schemas.Attributes):
        attr = self.get_attribute(db, id)
        if attr is None:
            return None
        for key, value in attribute.dict().items():
            setattr(attr, key, value)
        db.commit()
        db.refresh(attr)
        return attr

    def delete_attribute(self, db: Session, id: int):
        attr = self.get_attribute(db, id)
        return self.delete_element(db, attr)

class ValuesOperations(BaseOperations):
    def __init__(self):
        super().__init__()

    def get_value(self, db: Session, id: int):
        return db.query(model_db.Values).filter(model_db.Values.id == id).first()

    def get_all_values(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(model_db.Values).offset(skip).limit(limit).all()

    def create_value(self, db: Session, value: schemas.Values):
        new_val = model_db.Values(**value.dict())
        return self.create_element(db, new_val)

    def update_value(self, db: Session, id: int, value: schemas.Values):
        val = self.get_value(db, id)
        if val is None:
            return None
        for key, value in value.dict().items():
            setattr(val, key, value)
        db.commit()
        db.refresh(val)
        return val

    def delete_value(self, db: Session, id: int):
        val = self.get_value(db, id)
        return self.delete_element(db, val)
