from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Property, Business
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def get_user(user_id):
    return session.query(User).filter(User.telegram_id == user_id).first()

def create_user(user_id):
    new_user = User(telegram_id=user_id, money=1000)
    session.add(new_user)
    session.commit()

def get_properties():
    return session.query(Property).all()

def purchase_property(user, prop_id):
    property = session.query(Property).filter(Property.id == prop_id).first()
    if user.money >= property.price:
        user.money -= property.price
        user.properties.append(property)
        session.commit()
        return True
    return False

def purchase_business(user, business_id):
    business = session.query(Business).filter(Business.id == business_id).first()
    if user.money >= business.price:
        user.money -= business.price
        user.businesses.append(business)
        session.commit()
        return True
    return False
