#!/usr/bin/python3
"""Defines FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Represent an abstracted storage engine.

    Attributes:
        __file_path : Must be a str, the name of the file where objects are saved.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return the dictionary __objects.
        """

        return FileStorage.__objects

    def new(self, obj):
        """
        Responsible for adding a new object to the storage system,
        indexing it by a combination of its class name and unique identifier
        """

        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """
        This code defines a method named save() which is responsible
        for serializing the objects stored in the __objects attribute
        of the FileStorage class into a JSON file specified by the __file_path
        """

        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """
        Defines a method named reload() within a class FileStorage of a file storage system.
        This method is responsible for deserializing the JSON data from the file specified by
        the __file_path attribute and reconstructing objects stored in the __objects attribute.
        """

        try:
            with open(FileStorage.__file_path) as m:
                objdict = json.load(m)
                for t in objdict.values():
                    cls_name = t["__class__"]
                    del t["__class__"]
                    self.new(eval(cls_name)(**t))
        except FileNotFoundError:
            return
