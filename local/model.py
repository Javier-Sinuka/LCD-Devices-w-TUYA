from abc import ABC, abstractmethod

class ModelDevices(ABC):

    @abstractmethod
    def save_content_devices(self):
        pass

    @abstractmethod
    def save_devices_info(self):
        pass

    @abstractmethod
    def save_attributes_local_device(self):
        pass