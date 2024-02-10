#!/usr/bin/python3
"""
Special/magic method used for initializing newly created objects within a class
"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
