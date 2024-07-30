from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    balance = Column(Float, default=200000.0)
    businesses = Column(Text, default='')

engine = create_engine('sqlite:///game_bot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_user(username):
    return session.query(User).filter_by(username=username).first()

def create_user(username):
    user = User(username=username)
    session.add(user)
    session.commit()

def update_balance(username, amount):
    user = get_user(username)
    if user:
        user.balance += amount
        session.commit()

def update_businesses(username, business, level=1):
    user = get_user(username)
    if user:
        businesses = {}
        if user.businesses:
            businesses = dict(item.split(':') for item in user.businesses.split(','))
        if business in businesses:
            businesses[business] = str(int(businesses[business]) + level)
        else:
            businesses[business] = str(level)
        user.businesses = ','.join(f'{k}:{v}' for k, v in businesses.items())
        session.commit()

def get_business_levels(username):
    user = get_user(username)
    if user and user.businesses:
        return dict(item.split(':') for item in user.businesses.split(','))
    return {}
