#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        # password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            # first time user creation hash password
            if not kwargs.get("id", None) and kwargs.get("password", None):
                self._password = hashlib.md5(kwargs["password"].encode()).hexdigest()
            if kwargs.get("id", None) and kwargs.get("password", None):
                self._password = kwargs["password"]

        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """get password"""
        return self._password

    @password.setter
    def password(self, passwd):
        """set password"""
        self._password = hashlib.md5(passwd.encode()).hexdigest()
