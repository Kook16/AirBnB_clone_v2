#!/usr/bin/python3
'''DBStorage module
'''
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker


user = getenv('HBNB_MYSQL_USER')
pwd = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db = getenv('HBNB_MYSQL_DB')
env = getenv('HBNB_ENV')


class DBStorage:
    '''A db Storage class'''
    __engine = None
    __session = None
    __classes = [State,
                 City,
                 User,
                 Place,
                 Review,
                 Amenity
                 ]
    def __init__(self):
        '''Initializer for the dbstorage class'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        
        if env == 'test':
            Base.metaData.drop_all(self.__engine)

    def all(self, cls=None):
        '''Return a dict of objs'''
        my_dict = {}
        if cls:
            if cls in self.__classes:
                cls_r = DBStorage.__session.query(cls)
                for row in cls_r:
                    key = '{}.{}'.format(row.__class__.__name__, row.id)
                    my_dict[key] = row
        else:
            for clas in self.__classes:
                cls_r = DBStorage.__session.query(clas)
                for row in cls_r:
                    key = '{}.{}'.format(row.__class__.__name__.row.id)
                    my_dict[key] = row
        return my_dict
    
    def new(self, obj):
        '''Adds obj to current session'''
        self.__session.add(obj)

    def save(self):
        '''Commit all changes to the current dd'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Deletes the current db session'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''Creates wll tables in the db'''
        Base.metadata.create_all(self.__engine)
        local_session = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        session = scoped_session(local_session)
        DBStorage.__session = session()

    def close(self):
        '''close sessions'''
        DBStorage.__session.close()

