-- create the table
CREATE TABLE IF NOT EXISTS titanic(
    passenger INT PRIMARY KEY,
    survived BOOLEAN,
    pclass INTEGER,
    pname VARCHAR,
    sex VARCHAR,
    age FLOAT
);