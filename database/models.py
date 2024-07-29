from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

user_properties = Table('user_properties', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('property_id', ForeignKey('properties.id'), primary_key=True)
)

user_businesses = Table('user_businesses', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('business_id', ForeignKey('businesses.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    money = Column(Integer, default=0)
    properties = relationship('Property', secondary=user_properties, back_populates='owners')
    businesses = relationship('Business', secondary=user_businesses, back_populates='owners')

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    owners = relationship('User', secondary=user_properties, back_populates='properties')

class Business(Base):
    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    owners = relationship('User', secondary=user_businesses, back_populates='businesses')
