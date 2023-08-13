from flask import Flask, request
from flask_restful import reqparse, Resource, Api, abort

app = Flask(__name__)
api = Api(app)

AUTHORS = {
    'author1': {'author': 'TP'},
    'author2': {'author': 'SK'},
    'author3': {'author': 'NG'}
}

def abort_if_author_doesnt_exist(author_id):
    if author_id not in AUTHORS:
        abort(404, message="Author {} doesn't exist".format(author_id))

parser = reqparse.RequestParser()
parser.add_argument('author', type=str, required=True)

class Author_Single(Resource):
    def get(self, author_id):
        abort_if_author_doesnt_exist(author_id)
        return AUTHORS[author_id], 201
    
    def delete(self, author_id):
        abort_if_author_doesnt_exist(author_id)
        del AUTHORS[author_id]
        return '', 204
    
    def put(self, author_id):
        args = parser.parse_args()
        author = {'author': args['author']}
        AUTHORS[author_id] = author
        return author, 201
    
class Author_All(Resource):
    def get(self):
        return AUTHORS
    
    def post(self):
        author_id = f'author{len(AUTHORS) + 1}'
        author = {'author': request.form.get('author')}
        AUTHORS[author_id] = author
        return AUTHORS[author_id], 201
    
api.add_resource(Author_Single, '/author/<author_id>')
api.add_resource(Author_All, '/authors')

if __name__ == '__main__':
    app.run(debug=True)