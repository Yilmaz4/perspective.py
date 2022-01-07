"""
Perspective API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~

An easy-to-use API wrapper for Perspective API written in Python.
"""

__title__ = "perspective.py"
__author__ = "Yilmaz04"
__license__ = "MIT"
__copyright__ = "Copyright 2021 Yilmaz Alpaslan"
__version__ = "0.2.0"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .main import Client
from .attributes import Attributes
from .utils import Utils as utils