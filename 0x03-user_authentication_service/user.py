#!/usr/bin/env python3
'''
Module user.py: SQLAlchemy model named User for db table named users
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer


Base = declarative_base()


class User(Base):
    ''' User model that inherits from Base '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
