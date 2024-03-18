#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import getenv

metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                          Column('place_id', ForeignKey('places.id'), primary_key=True, nullable=False),
                          Column('amenity_id', ForeignKey('amenities.id'), primary_key=True, nullable=False)
)



class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place', cascade='all, delete')
        amenities = relationship('Amenity', secondary=place_amenity, viewonly=False)
    else:
        @property
        def Review(self):
            '''returns the list of Review instances with place_id equals
            to the current Place.id
            '''
            from models import storage
            from models.review import Review
            filtered_reviews = []
            all_reviews = storage.all(Review)

            for key, review in all_reviews.items():
                id = key.split('.')[1]
                if self.id == id:
                    filtered_reviews.append(review)
            return filtered_reviews
        
        @property
        def amenities(self):
            '''getter method for amenities'''
            from models.__init__ import storage
            from models.amenity import Amenity
            list_amenities = []
            all_amenities = storage.all(Amenity)
            for amenity in all_amenities:
                if self.id == amenity.amenity_ids:
                    list_amenities.append(amenity)

            return list_amenities
        
        @amenities.setter
        def amenities(self, obj):
            '''Setter method for amenities'''
            from models.__init__ import storage
            from models.amenity import Amenity
            if isinstance(obj, storage.all(Amenity)):
                self.amenity_ids.append(obj.id)
    

