from flask_restful import Resource, reqparse, request
import sqlite3


class DiscWorld(Resource):
    def get(self, disc_id):
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM disc WHERE id=?", 
                       (disc_id,))
        disc = cursor.fetchone()
        if disc:
            return {'id': disc[0], 'char': disc[1], 'type': disc[2], 'fav': disc[3]}
        else:
            return {'message': 'Character not found'}, 404
        
    def post(self):
        data = request.get_json(force=True)
        if not data:
            return {'message': "Invalid request format. Expected 'application/json'."}, 400

        char = data.get('char')
        type = data.get('type')

        if not char or not type:
            return {'message': 'Missing required data'}, 400
        
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('char', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('fav', type=str)
        args = parser.parse_args()

        cursor.execute("INSERT INTO disc (char, type, fav) VALUES (?, ?, ?)", 
                       (args['char'], args['type'], args['fav']))
        
        conn.commit()
        return {'message': 'Character added'}
    
    def put(self, disc_id):
        data = request.get_json(force=True)
        if not data:
            return {'message': "Invalid request format. Expected 'application/json'."}, 400

        char = data.get('char')
        type = data.get('type')

        if not char or not type:
            return {'message': 'Missing required data'}, 400
        
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('char', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('fav', type=str)
        args = parser.parse_args()

        cursor.execute("UPDATE disc SET char=?, type=?, fav=? WHERE id=?", 
                       (args['char'], args['type'], args['fav'], disc_id,))

        conn.commit()
        return {'message': 'Character updated'}, 201
    

