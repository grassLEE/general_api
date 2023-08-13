from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

CAST_MEMBERS = {
    'cast1': {'cast': 'Sir Sam'},
    'cast2': {'cast': 'Nanny Ogg'},
    'cast3': {'cast': 'The Librarian'}
}

def abort_if_cast_doesnt_exist(cast_id):
    if cast_id not in CAST_MEMBERS:
        abort(404, message="Cast {} doesn't exist".format(cast_id))

parser = reqparse.RequestParser()
parser.add_argument('cast')

# Show a single Cast member with delete function
class Cast(Resource):
    def get(self, cast_id):
        abort_if_cast_doesnt_exist(cast_id)
        return CAST_MEMBERS[cast_id]

    def delete(self, cast_id):
        abort_if_cast_doesnt_exist(cast_id)
        del CAST_MEMBERS[cast_id]
        return '', 204
    
    def put(self, cast_id):
        args = parser.parse_args()
        cast = {'cast': args['cast']}
        CAST_MEMBERS[cast_id] = cast
        return cast, 201
    
# List of all Cast memeber w/ POST to add new cast members
class CastList(Resource):
    def get(self):
        return CAST_MEMBERS
    
    def post(self):
        args = parser.parse_args()
        cast_id = int(max(CAST_MEMBERS.keys()).lstrip('cast')) + 1
        cast_id = 'cast%i' % cast_id
        CAST_MEMBERS[cast_id] = {'cast': args['cast']}
        return CAST_MEMBERS[cast_id], 201
    
api.add_resource(Cast, '/cast/<cast_id>')
api.add_resource(CastList, '/cast')

if __name__ == '__main__':
    app.run(debug=True)

"""Curl Post Method:
curl -X POST -H "Content-Type: application/json" -d '{"cast": "Granny Weatherwax"}' http://localhost:5000/cast -v
"""