from flask import Flask, abort, jsonify, make_response
from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_httpauth import HTTPBasicAuth
import gh_user

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'eric':
        return 'ghuc_proj'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

users = gh_user.Users()
user_fields = {
    'username': fields.String,
    'contributions': fields.String,
    'uri': fields.Url('user')
}


class UserListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No user provided', location='json')
        super(UserListAPI, self).__init__()

    # Get user list
    @staticmethod
    def get():
        ulist = users.get_user_list()
        return {'users': [marshal(user, user_fields) for user in ulist]}

    # Add user
    def post(self):
        args = self.reqparse.parse_args()
        if not users.add_new_user(args['username']):
            abort(400)
        return {'user': marshal([user for user in users.get_user_list()
                                 if user['username'] == args['username']], user_fields)}, 201


class UserAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        super(UserAPI, self).__init__()

    # Get user contributions for the year
    @staticmethod
    def get(username):
        ulist = users.get_user_list()
        if len(ulist) == 0:
            abort(404)
        user = [user for user in ulist if user['username'] == username]
        if len(user) == 0:
            abort(404)
        return {'user': marshal(user[0], user_fields)}

    # Update user's contributions
    @staticmethod
    def put(username):
        user = [user for user in users.get_user_list() if user['username'] == username]
        if len(user) == 0:
            abort(404)
        users.get_contributions(username, None, None, True)
        return {'user': marshal(user, user_fields)}

    # Delete a user
    @staticmethod
    def delete(username):
        user = [user for user in users.get_user_list() if user['username'] == username]
        if len(user) == 0:
            abort(404)
        return {'result': users.remove_user(username)}


class UserDateAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        super(UserDateAPI, self).__init__()

    # Get user's contributions from start to end date
    @staticmethod
    def get(username, start, end):
        user = [user for user in users.get_user_list() if user['username'] == username]
        if len(user) == 0:
            abort(404)
        return {'contributions': users.get_contributions(username, start, end)}


api.add_resource(UserListAPI, '/ghuc/api/v1.0/users', endpoint='users')
api.add_resource(UserAPI, '/ghuc/api/v1.0/users/<username>', endpoint='user')
api.add_resource(UserDateAPI, '/ghuc/api/v1.0/users/<username>/<start>:<end>', endpoint='date')


if __name__ == '__main__':
    app.run(debug=False)
