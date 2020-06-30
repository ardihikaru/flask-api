from flask_restplus import Namespace, fields

# api = Namespace('user', description='User related operations')
api = Namespace('users', description='User related operations')

register_data = api.model('register_data', {
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'password_confirm': fields.String,
})

register_data_resp = api.model('register_data_resp', {
    'id': fields.String,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
})

register_results = api.model('register_results', {
    'response': fields.Boolean,
    'results': fields.Nested(register_data_resp),
    'message': fields.String,
})

all_user_data = api.model('all_user_data', {
    'response': fields.Boolean,
    'results': fields.List(fields.Nested(register_data_resp)),
    'message': fields.String,
    'total': fields.Integer,
})

editable_data = api.model('editable_data', {
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
})