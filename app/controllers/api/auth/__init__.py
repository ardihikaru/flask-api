from flask_restplus import Namespace, fields

api = Namespace('/', description='Authentication related operations')

token_data = api.model('token_data', {
    'username': fields.String,
    'access_token': fields.String,
    'access_token_expired': fields.String,
    'refresh_token': fields.String,
    'refresh_token_expired': fields.String
})

login_results = api.model('login_results', {
    'response': fields.Boolean,
    'results': fields.Nested(token_data),
    'message': fields.String,
})

get_login_results = api.model('get_login_results', {
    'response': fields.Boolean,
})

login_model = api.model('login_model', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

# logout
get_logout_results = api.model('get_logout_results', {
    'response': fields.Boolean,
    'message': fields.String,
})

# refresh
refresh_model = api.model('refresh_model', {
    'access_token': fields.String,
    'access_token_expired': fields.String,
})

refresh_results = api.model('refresh_results', {
    'response': fields.Boolean,
    'results': fields.Nested(refresh_model),
    'message': fields.String,
})
