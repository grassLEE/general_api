from flask_restful import request, reqparse, Resource
import sqlite3


class AllNovels(Resource):
    def get(self, novel_id=None):
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()

        if novel_id:
            cursor.execute("SELECT * FROM novels WHERE id=?", 
                           (novel_id,))
        else:
            cursor.execute("SELECT * FROM novels")

        novels = cursor.fetchall()
        novel_list = []
        for novel in novels:
            novel_list.append({
                'title': novel[1],
                'pages': novel[2],
                'focus': novel[3]
            })
        
        conn.close()
        return {'novels': novel_list}

    def post(self):
        data = request.get_json(force=True)
        if not data:
            return {'message': "Invalid request format. Expected 'application/json'."}, 400

        title = data.get('title')
        focus = data.get('focus')

        if not title or not focus:
            return {'message': 'Missing required data'}, 401
        
        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('pages', type=int, required=True)
        parser.add_argument('focus', type=str, required=True)
        args = parser.parse_args()

        cursor.execute("INSERT INTO novels (title, pages, focus) VALUES (?, ?, ?)", 
                       (args['title'], args['pages'], args['focus']))
        
        conn.commit()
        conn.close()
        return {'message': 'Novel added'}
    
    def put(self, novel_id):
        data = request.get_json(force=True)
        if not data:
            return {'message': "Invalid request format. Expected 'application/json'."}, 400
        
        title = data.get('title')
        focus = data.get('focus')

        if not title or not focus:
            return {'message': 'Missing required data'}, 400

        conn = sqlite3.connect('dsworld.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('pages', type=int, required=True)
        parser.add_argument('focus', type=str, required=True)
        args = parser.parse_args()

        cursor.execute("UPDATE novels SET title=?, pages=?, focus=? WHERE id=?", 
                       (args['title'], args['pages'], args['focus'], novel_id,))
        
        conn.commit()
        conn.close()
        return {'message': '{} updated'.format(novel_id,)}
    