from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

@app.route('/query', methods=['POST'])
@limiter.limit("10 per minute")
def query():
    # Only allow requests from authorized client with valid secret key.
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != 'VQs8e7mHBuWozlPug0Z08ZfNbwm3LMyb':
        return jsonify({'message': 'Unauthorized'}), 401
    else:
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