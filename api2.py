from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

NOVELS = {
    'novel1': {'novel': 'Thud!'},
    'novel2': {'novel': 'Mort'},
    'novel3': {'novel': 'Witches Abroad'}
}

def abort_if_novel_doesnt_exist(novel_id):
    if novel_id not in NOVELS:
        abort(404, message="Novel {} doesn't exist".format(novel_id))

parser = reqparse.RequestParser()
parser.add_argument('novel')

# Show a single novel item and allows for Delete method in novel item
"""Retrieve details of a specific novel (GET /novel/<novel_id>):
curl http://localhost:5000/novel/novel1

Delete a specific novel (DELETE /novel/<novel_id>):
curl -X DELETE http://localhost:5000/novel/novel1

Update the details of a specific novel (PUT /novel/<novel_id>):
curl -X PUT -H "Content-Type: application/json" -d '{"novel": "Updated Novel Title"}' http://localhost:5000/novel/novel1
"""
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
    
# Show a list of all novels and allows a POST method for adding new novels
"""Retrieve the list of all novels (GET /allnovels):
curl http://localhost:5000/allnovels

Add a new novel to the collection (POST /allnovels):
curl -X POST -H "Content-Type: application/json" -d '{"novel": "New Novel Title"}' http://localhost:5000/allnovels
"""
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
api.add_resource(Novel_List, '/allnovels')

if __name__ == '__main__':
    app.run(debug=True)