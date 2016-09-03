from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
import datetime


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def allByName():
    for instance in session.query(Puppy).order_by(Puppy.name.asc()).all():
        print(instance.name)

def youngerThanSixMonths():
    six_months_ago = datetime.date.today() - datetime.timedelta(6*365/12)
    for instance in session.query(Puppy).order_by(Puppy.dateOfBirth.desc()).filter(Puppy.dateOfBirth >= six_months_ago):
        print(instance.name)
        print(instance.dateOfBirth)

def allByWeight():
    for instance in session.query(Puppy).order_by(Puppy.weight):
        s = ""
        seq = (instance.name, str(instance.weight))
        mytext = s.join (seq)
        print(mytext)

def allByShelter():
    for instance in session.query(Shelter).all():
        print(instance.name)

        for puppies in session.query(Puppy).filter(Puppy.shelter_id == instance.id):
            print (puppies.name)

        print("\n")

allByShelter()
#1. Query all of the puppies and return the results in ascending alphabetical order
#2. Query all of the puppies that are less than 6 months old organized by the youngest first
#3. Query all puppies by ascending weight
#4. Query all puppies grouped by the shelter in which they are staying