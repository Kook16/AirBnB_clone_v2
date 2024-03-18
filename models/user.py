#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """iherits from BaseModel and Base

    Args:
        BaseModel (clss): parent class
        Base (clss): engine
    """
    __tablename__ = 'users'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        email = Column(
            String(128),
            nullable=False)
        password = Column(
            String(128),
            nullable=False)
        first_name = Column(
            String(128),
            nullable=True)
        last_name = Column(
            String(128),
            nullable=True)
        places = relationship(
            'Place',
            backref='user',
            cascade="all, delete-orphan")
        reviews = relationship(
            'Review',
            backref='user',
            cascade="all, delete-orphan")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
