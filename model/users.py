#! /usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "Adrian Weber, Centre for Development and Environment, University of Bern"
__date__ = "$May 16, 2013 1:24:16 PM$"

from decide_user.model.meta import Base
import hashlib
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
                      CheckConstraint('(users.is_active = FALSE) = (users.activation_uuid IS NOT NULL)', name="users_activation_uuid_not_null"),
                      {"schema": 'public'}
                      )
    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    firstname = Column(String(128), nullable=True)
    lastname = Column(String(128), nullable=True)
    fk_usergroup = Column(Integer, ForeignKey('public.usergroups.id'), nullable=False)
    registration_timestamp = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    activation_uuid = Column(UUID, nullable=True)
    position = Column(String(128))
    organization = Column(String(512))
    purpose = Column(String(512))
    fk_requested_usergroup = Column(Integer, ForeignKey('public.usergroups.id'), nullable=False)

    def __repr__(self):
        return (
                '<Anr_Users> id [ %s ] | email [ %s ] | firstname [ %s ] | lastname [ %s ]' %
                (self.id, self.email, self.firstname, self.lastname)
                )

    def validate_password(self, password):
        """
        Validates the password for repoze.who SQLAlchemy plugin
        """

        pw = hashlib.md5(password).hexdigest()
        return self.password == pw

class UserGroup(Base):
    __tablename__ = 'usergroups'
    __table_args__ = {
        "schema": 'public'
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(String(128))
    mapviewer = Column(String)
    decidegis = Column(String)
    variables = Column(String)
    metadata_column = Column('metadata', String)
    users = relationship(User, backref="group", primaryjoin="User.fk_usergroup == UserGroup.id")
    users_requests = relationship(User, backref="requested_group", primaryjoin="User.fk_requested_usergroup == UserGroup.id")