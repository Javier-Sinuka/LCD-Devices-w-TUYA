import json
from datetime import datetime
import time
import tinytuya
from sqlalchemy.orm import Session
import numpy

from local_model import LocalModel, LocalConnection
from model_db import Devices, get_db

class DataBaseController():
    __local_model = LocalModel()
    db: Session
    def __init__(self, db: Session):
        self.save_devices()
        self.db = db

    def save_devices(self):
        acces_data = self.__local_model.get_all_acces_data()
        for element in acces_data:
            existing_device_name = self.db.query(Devices).filter(Devices.name == element).first()
            existing_device_id = self.db.query(Devices).filter(Devices.device_id == acces_data[element]['id']).first()
            if not existing_device_name and not existing_device_id:
                data = Devices(name=element, device_id=acces_data[element]['id'])
                self.put_data(self.db, data)

    def put_data(self, db: Session, model):
        try:
            db.add(model)
            db.commit()
        except InterruptedError as e:
            db.rollback()
            print("Error adding data: ", e)
            return None

    def get_data(self, db: Session, model, id):
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

class DevicesController(DataBaseController):
    __local_connection = LocalConnection
    database = DataBaseController
    db: Session = Session

    def __init__(self):
        self.db = next(get_db())
        super().__init__(db=self.db)
        self.__local_connection = LocalConnection()

    def testeo_local(self):
        data = self.__local_connection.get_all_acces_data()
        for i in data:
            print(self.__local_connection.get_status_device(data[i].get('id')))
            time.sleep(4)
    # def test_almacenamiento(self):
    #     for i in self.get_all_data(db=self.db, model=Devices):
    #         d = self.__local_connection.get_status_device(device_id=i.device_id)
    #         data_device = json.dumps(d)
    #         data = EventTable(device_id=i.id,
    #                           date=datetime.now(),
    #                           event=data_device)
    #         self.put_data(self.db, data)
    #         time.sleep(2)

dev = DevicesController()
# dev.test_almacenamiento()
# dev.testeo_local()
