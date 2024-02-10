#!/usr/bin/python3
"""Defines the User class."""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Represent a User.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str), last_name (str)
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
