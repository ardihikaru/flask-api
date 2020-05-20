from flask_restplus import  Resource, abort
from flask import request
from app.addons.database_blacklist.blacklist_helpers import is_token_valid
from app.addons.utils import get_json_template, masked_json_template
from app.models.user.user import User
from . import *
from flask_jwt_extended import (
    jwt_refresh_token_required
)

@api.route('/auth/login')
# @api.hide
@api.response(400, 'Json Input should be provided.')
class LoginByTokenRoute(Resource):
    @api.doc(security=None)
    @api.marshal_with(login_results)
    @api.expect(login_model)
    def post(self):
        '''Login using Binary Token to get Server Token'''
        try:
            json_data = api.payload
            resp = User().validate_user(json_data=json_data)
            return masked_json_template(resp, 200)
        except:
            resp = get_json_template(response=False, message="No Json Input Found.", results=-1, total=-1)
            return resp, 404

    @api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
    @api.marshal_with(get_login_results)
    def get(self):
        '''Retrieve login status'''
        is_valid, code, msg   = is_token_valid(request.headers.get('Authorization'))
        if is_valid:
            return masked_json_template({"response": True}, 200)
        else:
            abort(code, msg)

@api.route('/auth/logout')
# @api.hide
@api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
class LogoutRoute(Resource):
    @api.marshal_with(get_logout_results)
    def get(self):
        '''Logout and autoamatically revoke current access_token (PS: refresh_token still can be used)'''
        is_valid, code, msg = is_token_valid(request.headers.get('Authorization'))
        if is_valid:
            encoded_token = request.headers.get('Authorization').replace('Bearer ', '')
            resp = User().do_logout(encoded_token=encoded_token)
            return masked_json_template(resp, 200)
        else:
            abort(code, msg)

# @api.route('/auth/refresh')
# # @api.hide
# @api.response(401, 'Unauthorized Access. Access Token should be provided and validated.')
# class RefreshTokenRoute(Resource):
#     @api.marshal_with(refresh_results)
#     @jwt_refresh_token_required
#     def get(self):
#         '''Use refresh_token to generate another access_token (because the old one has been expired)'''
#         resp = User().do_refresh_token()
#         return masked_json_template(resp, 404)
