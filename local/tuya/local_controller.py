from datetime import datetime
import time
from sqlalchemy.orm import Session

from local_model import LocalModel, LocalConnection
from api.model_database import Devices, Attributes, Values, get_db

class DataBaseController():
    __local_model = LocalModel()
    db: Session
    def __init__(self, db: Session):
        self.save_devices_data()
        self.db = db

    def save_devices_data(self):
        acces_data = self.__local_model.get_all_acces_data()
        # mapping_data = self.__local_model.get_all_mapping_data()
        for element in acces_data:
            existing_device_name = self.db.query(Devices).filter(Devices.name == element).first()
            existing_device_id = self.db.query(Devices).filter(Devices.unique_device_id == acces_data[element]['id']).first()
            if not existing_device_name and not existing_device_id:
                data_device = Devices(name=element, unique_device_id=acces_data[element]['id'], manufacturer="TUYA")

                # mapping = mapping_data[acces_data[element]['id']]['mapping']
                # self.save_attributes(mapping)

                self.put_data(self.db, data_device)

    def save_attributes(self, mapping: dict):
        for data in mapping:
            existing_attribute_ref = self.db.query(Attributes).filter(Attributes.ref_attr_device == data).first()
            if not existing_attribute_ref:
                unit = ''
                try:
                    unit = mapping[data]['values']['unit']
                except Exception:
                    unit = 'none'
                data_attribute = Attributes(ref_attr_device=data,
                                            name=mapping[data]['code'],
                                            unit=unit,
                                            data_type=mapping[data]['type'])
                self.put_data(self.db, data_attribute)

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
    db: Session = Session

    def __init__(self):
        self.db = next(get_db())
        super().__init__(db=self.db)
        self.__local_connection = LocalConnection()

    def test_almacenamiento(self):
        data = self.__local_connection.get_all_acces_data()
        for i in data:
            data_local = self.__local_connection.get_status_device_tuya(data[i].get('id'))
            print(data_local)
            device_id = data[i].get('id')
            try:
                for j in data_local:
                    id_dev = self.db.query(Devices).filter_by(device_id=device_id).first().id
                    try:  # Existe un valor que no lo registra el dispositivo de medidor de aire
                        id_attr = self.db.query(Attributes).filter_by(ref_attr_device=j).first().id
                    except Exception:
                        id_attr = 'unregistered_attribute'
                    value = Values(device_id=id_dev,
                                   attribute_id=id_attr,
                                   value=data_local[j],
                                   timestamp=datetime.now())
                    self.put_data(self.db, value)
            except Exception:
                print("Elemento no iterable")
            time.sleep(2)




