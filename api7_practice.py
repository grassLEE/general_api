from flask import Flask
from flask_restful import reqparse, Api, Resource
import os
import sqlite3

app = Flask(__name__)
api = Api(app)

if not os.path.exists('mydatabase3.db'):
    open('mydatabase3.db', 'w').closed()

    conn = sqlite3.connect('mydatabase3.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL)''')
    conn.commit()

class UserResource(Resource):
    def get(self, user_id):
        conn = sqlite3.connect('mydatabase3.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id=?", 
                       (user_id,))
        
        user = cursor.fetchone()
        if user:
            return {'id': user[0], 'name': user[1], 'email': user[2]}
        else: 
            return {'message': 'User not found'}, 404
        
    def post(self, user_id):
        conn = sqlite3.connect('mydatabase3.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                       (args['name'], args['email']))
        
        conn.commit()
        return {'message': 'User created successfully'}, 201
    
    def put(self, user_id):
        conn = sqlite3.connect('mydatabase3.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", 
                       (args['name'], args['email'], user_id,))
        
        conn.commit()
        return {'message': 'User updated successfully'}, 200
    
    def delete(self, user_id):
        conn = sqlite3.connect('mydatabase3.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id=?", 
                       (user_id,))

        conn.commit()
        return {'message': 'User deleted successfully'}, 200
    
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)