from app import app, jwt, api, rc
from app import controllers
from app.addons.database_blacklist.blacklist_helpers import is_token_revoked

@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = rc.get(jti)
    if entry is None:
        return True
    return entry == 'true'

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decoded_token):
    return is_token_revoked(decoded_token)

# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)

@api.errorhandler(Exception)
def handle_jwt_error(error):
    return {'response': False, 'message': str(error)}, getattr(error, 'code', 401)

