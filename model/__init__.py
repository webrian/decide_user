#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Adrian Weber, Centre for Development and Environment, University of Bern"
__date__ ="$May 16, 2013 1:22:43 PM$"

from decide_usermodel.meta import UserSession

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    UserSession.configure(bind=engine)