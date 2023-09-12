import uuid
import datetime


class Animal:
    def __init__(self, age: int, species_name: str, common_name: str):
        self.id: str = str(uuid.uuid4())
        self.age = age
        self.species_name = species_name
        self.common_name = common_name
        self.enclosure: str = ''
        self.caretaker: str = ''
        self.feeding_record: list[str] = []
        self.medical_record: list[str] = []
        
    def set_home(self):
        pass
    
    def set_caretaker(self):
        pass
        
    def feed(self):
        pass
        # self.feeding_record.append(datetime.datetime.now())
    
    def medical_checkup(self):
        pass
