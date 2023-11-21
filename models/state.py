#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            '''getter attribute for cities that returns the list of cities'''
            from models import storage
            from models.city import City
            list_city = []
            all_cities = storage.all(City).values()
            for city in all_cities:
                if self.id == city.state_id:
                    list_city.append(city)
            return list_city
