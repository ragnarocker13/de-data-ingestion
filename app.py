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
