from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

NOVELS = {
    'novel1': {'novel': 'Thud!'},
    'novel2': {'novel': 'The Light Fantastic'},
    'novel3': {'novel': 'Witches Abroad'}
}

def abort_if_novel_doesnt_exist(novel_id):
    if novel_id not in NOVELS:
        abort(404, message="Novel {} doesn't exist".format(novel_id))

parser = reqparse.RequestParser()
parser.add_argument('novel')

class Novel_Single(Resource):
    def get(self, novel_id):
        abort_if_novel_doesnt_exist(novel_id)
        return NOVELS[novel_id]
    
    def delete(self, novel_id):
        abort_if_novel_doesnt_exist(novel_id)
        del NOVELS[novel_id]
        return '', 204
    
    def put(self, novel_id):
        args = parser.parse_args()
        novel = {'novel': args['novel']}
        NOVELS[novel_id] = novel
        return novel, 201
    
class Novel_List(Resource):
    def get(self):
        return NOVELS
    
    def post(self):
        args = parser.parse_args()
        novel_id = int(max(NOVELS.keys()).lstrip('novel')) + 1
        novel_id = 'novel%i' % novel_id
        NOVELS[novel_id] = {'novel': args['novel']}
        return NOVELS[novel_id], 201
    
api.add_resource(Novel_Single, '/novel/<novel_id>')
api.add_resource(Novel_List, '/novels')

if __name__ == '__main__':
    app.run(debug=True)