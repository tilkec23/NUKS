from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    command = data['command']
    conn = sqlite3.connect('v3_final_data.db')
    cursor = conn.cursor()
    cursor.execute(command)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = []
    for row in rows:
        row_dict = {}
        for i in range(len(columns)):
            row_dict[columns[i]] = row[i]
        result.append(row_dict)
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(port = 8001)
