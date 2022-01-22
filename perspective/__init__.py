"""
Perspective API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~

An easy-to-use API wrapper for Perspective API written in Python.
"""

__title__ = "perspective.py"
__author__ = "Yilmaz04"
__license__ = "MIT"
__copyright__ = "Copyright 2021-2022 Yilmaz Alpaslan"
__version__ = "0.3.4"

from .main import Client
from .attributes import Attributes, all_attr_grps, all_attrs, all_expr_attrs, all_newy_attrs, all_prod_attrs
from .utils import Utils as utils