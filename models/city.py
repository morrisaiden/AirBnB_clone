#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """
    Represent a city

    attributes:
        state_id(str)
        name(str)
    """

    state_id = ""
    name = ""
