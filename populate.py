import csv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine("sqlite:///testdb.db")

# Create a base class for our class definitions
Base = declarative_base()


# Define our table as a class
class YourTable(Base):
    __tablename__ = "titanic"

    passenger = Column(Integer, primary_key=True)
    survived = Column(Integer)
    pclass = Column(Integer)
    pname = Column(String)
    sex = Column(String)
    age = Column(String)


# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Open the CSV file
with open("tested.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    # Skip the header row if it exists
    next(csv_reader, None)

    # Insert data into the table
    for row in csv_reader:
        new_row = YourTable(
            passenger=row[0],
            survived=bool(row[1]),
            pclass=int(row[2]),
            pname=row[3],
            sex=row[4],
            age=row[5],
        )
        session.add(new_row)

# Commit changes and close session
session.commit()
session.close()

print("Data imported successfully!")
