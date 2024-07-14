# Data Engineering Simple ETL Process

This guide explains three key steps in data ingestion and loading:

1. Creating a simple SQLite database.
2. Populating it with data imported from a CSV file and then cleaning up the database.
3. Creating an API to output the data in JSON format.

Before starting make sure to install all dependencies declared inside the requirements.txt file

```bash
pip install -r requirements.txt
```

## Step 1: Creating a Simple SQLite Database

First, let's create an SQLite database, assigning the respective datatypes for each column (testdb.sql file).

### SQL Code (testdb.sql)

```sql
-- create the table
CREATE TABLE IF NOT EXISTS titanic(
    passenger INT PRIMARY KEY,
    survived BOOLEAN,
    pclass INTEGER,
    pname VARCHAR,
    sex VARCHAR,
    age FLOAT
);
```

## Step 2: Populating the Database with Data from a CSV File and Cleaning Up the Database

Next, we'll populate the SQLite database with data from a CSV file (tested.csv), and then clean up the database by removing duplicates.

### Python Code (populate.py)

```python
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

```

After the table has been populated, we perform a simple cleanup by removing rows with null values.

### SQL Code (cleanup.sql)

```SQL
-- cleanup the table removing null values
DELETE FROM titanic
WHERE age = "";

-- check if rows with null values exists
SELECT COUNT(*) FROM titanic
where age = "";

```

## Step 3: Creating an API to Output the Data in JSON Format

As a final step, we'll create a simple API using Flask to output the data from the SQLite database in JSON format.

### Python Code (app.py)

```python
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/data", methods=["GET"])
def get_table_contents():

    # Connect to the SQLite database
    conn = sqlite3.connect("testdb.db")
    cursor = conn.cursor()

    # Execute a SELECT query to fetch all rows from the table
    cursor.execute("SELECT * FROM titanic")

    # Retrieve all the rows
    rows = cursor.fetchall()

    # Retrive column names
    column_names = [description[0] for description in cursor.description]

    # Terminate the connection
    conn.close()

    # Create the list of dictionaries
    result = []
    for row in rows:
        result.append(dict(zip(column_names, row)))

    # Finally, output as json
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
```

### Running the Flask App

To run the Flask app, save the above code in a file (e.g., app.py) and execute the following command in your terminal:

```bash
python app.py

```

Visit http://127.0.0.1:5000/data in your web browser to see the JSON output of the data.
