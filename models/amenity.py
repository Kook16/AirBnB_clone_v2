#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base

import os
from sqlalchemy import Column, String
from models.place import place_amenity
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """amenity class"""
    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(
            String(128),
            nullable=False)
        place_amenities = relationship(
            "Place",
            secondary=place_amenity,
            back_populates="amenities")
    else:
        name = ""
