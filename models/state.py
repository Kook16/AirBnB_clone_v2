#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
 
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        @property
        def City(self):
            '''returns the list of City instances
                with state_id equals to the current State.id
            '''
            from models import storage
            from models.city import City
            filtered_cities = []
            all_cities = storage.all(City)
            for key, city in all_cities.items():
                class_name, id = key.split('.')
                if id == self.id:
                    filtered_cities.append(city)
            return filtered_cities

