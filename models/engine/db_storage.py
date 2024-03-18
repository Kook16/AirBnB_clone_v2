#!/usr/bin/python3
"""The New storage engine DBStorage"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """orm storage class
    """
    __engine = None
    __session = None
    all_classes = {"State", "City", "User", "Amenity", "Place", "Review"}

    def __init__(self):
        """create engine and link to the MySQL database and user created
        before
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query current db session depending on class name argument

        Args:
            cls : class name.

        Returns:
        dictionary: key = <class-name>.<object-id>
                    value = object
        """
        new_dict = {}
        if cls:
            if type(cls) == str:
                cls = self.all_classes[cls]

            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj
        else:
            for clas in self.all_classes.values():
                objs = self.__session.query(clas).all()

                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """add the object to the current database session (self.__session)
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)
        # self.save()

    def reload(self):
        """create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        sc_session = scoped_session(Session)
        self.__session = sc_session()

    def close(self):
        """close the transactional resources
        """
        self.__session.close()
        # self.Session.close()
        # self.__session.remove()
