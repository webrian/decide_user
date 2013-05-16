#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "Adrian Weber, Centre for Development and Environment, University of Bern"
__date__ = "$May 16, 2013 1:24:52 PM$"

"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

__all__ = ['Base', 'UserSession']

# SQLAlchemy session manager. Updated by model.init_model()
UserSession = scoped_session(sessionmaker())

# The declarative Base
Base = declarative_base()