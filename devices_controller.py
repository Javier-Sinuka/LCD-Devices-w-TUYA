from datetime import datetime
from sqlalchemy.orm import Session
import numpy

from local_model import LocalModel, LocalConection
from model_db import TemporalPowerData, Devices, get_db

class DataBaseController:
    __local_model = LocalModel()
    db: Session = Session

    def __init__(self):
        self.db = next(get_db())
        self.save_devices()

    def save_devices(self):
        for i in self.__local_model.get_all_acces_data():
            existing_device = self.db.query(Devices).filter(Devices.name == i).first()
            if not existing_device:
                data = Devices(name=i)
                self.put_data(self.db, data)

    def put_data(self, db: Session, model):
        try:
            db.add(model)
            db.commit()
        except InterruptedError as e:
            db.rollback()
            print("Error adding data: ", e)
            return None

    def get_data(self, db:Session, model, id):
        return db.get(model, id)
        # return db.query(model).get(id)
    def get_all_data(self, db: Session, model):
        return db.query(model).all()

    def delete_data(self, db: Session, model, id):
        data_model = self.get_data(db, model, id)
        db.delete(data_model)
        db.commit()
        return data_model

# local_model = LocalModel()
temporal = TemporalPowerData()
db = DataBaseController()
