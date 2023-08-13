from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import sqlite3
import os
import json

app = Flask(__name__)
api = Api(app)

if not os.path.exists('mydatabase.db'):
    open('mydatabase.db', 'w').close()

# Create a connection to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL)''')
conn.commit()

class UserResource(Resource):
    # curl http://localhost:5000/users/1
    def get(self, user_id):
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'name': user[1], 'email': user[2]}
        else:
            return {'message': 'User not found'}, 404

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        # Check if the request data is JSON
        if request.is_json:
            data = request.get_json()
            args['name'] = data.get('name')
            args['email'] = data.get('email')

        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                       (args['name'], args['email']))
        conn.commit()

        return {'message': 'User created successfully'}, 201

api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
