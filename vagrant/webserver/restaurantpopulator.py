# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from restaurants import Base, Restaurant
# from flask.ext.sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Add Restaurants
rest1 = Restaurant(name="McDonalds")

session.add(rest1)

rest2 = Restaurant(name="Moevenpick")

session.add(rest2)

rest3 = Restaurant(name="Mauldasch")

session.add(rest3)

rest4 = Restaurant(name="Absteige")

session.add(rest4)

session.commit()