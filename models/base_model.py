#!/usr/bin/python3
"""Defines BaseModel class"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    BaseModel of AirBnB_clone
    Contains __init__, save, to_dict and __str__
    methods
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes new BaseModel.

        This piece of code handles the initialization of instance attributes
        based on provided keyword arguments (kwargs) and,
        if no arguments are provided,
        assumes the instance is new and performs some action
        related to storage management.

        Arguments:
            *args : Accepts any *args.
            **kwargs :This is the dict ==> Key/value pairs of attributes <==.
        """

        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for q, r in kwargs.items():
                if q == "created_at" or q == "updated_at":
                    self.__dict__[q] = datetime.strptime(r, tform)
                else:
                    self.__dict__[q] = r
        else:
            models.storage.new(self)

    def save(self):
        """
        Defines the save method within the BaseModel class
        Save the current instance or its changes to external storage
        Method depends on the implementation details of the storage system.
        """

        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Return the dictionary of the BaseModel instance.

        The to_dict method converts the BaseModel instance
        into a dictionary representation
        Finally, the method returns the updated dictionary rdict
        """

        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        rdict["__class__"] = self.__class__.__name__
        rdict["updated_at"] = self.updated_at.isoformat()

        return rdict

    def __str__(self):
        """
        This code defines the __str__ method
        Return the print/str representation of the BaseModel instance.
        """

        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
