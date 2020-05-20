from datetime import datetime
from flask_jwt_extended import decode_token
from app.addons.database_blacklist.exceptions import TokenNotFound
from app.addons.redis.translator import redis_set, redis_get
from app import app, rc

def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)

def extract_identity(encoded_token):
    decoded_token   = decode_token(encoded_token)
    return decoded_token["identity"]

def is_token_valid(raw_token):
    try:
        encoded_token   = raw_token.replace('Bearer ','')
        decoded_token   = decode_token(encoded_token)
        try:
            is_revoked = is_token_revoked(decoded_token)
            if not is_revoked:
                return True, 200, 'OK'
        except:
            pass
        return False, 401, 'Token has expired'
    except:
        return False, 400, 'Please Provide a valid auth token.'

def revoke_current_token(encoded_token, json_data):
    result = {"message": None, "resp_code": 400}
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']

    if not json_data:
        result["message"] = "Missing 'revoke' in body"
    revoke = json_data.get('revoke', None)
    if revoke is None:
        result["message"] = "Missing 'revoke' in body"
    if not isinstance(revoke, bool):
        result["message"] = "'revoke' must be a boolean"

    try:
        if revoke:
            revoke_token(jti)
            result["message"] = "Token revoked"
            result["resp_code"] = 200
    except TokenNotFound:
        result["message"] = "The specified token was not found"
        result["resp_code"] = 404
    return result

def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']

    data = redis_get(rc, jti)
    if data is None:
        return True
    else:
        return data

def revoke_token(jti):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """

    try:
        rc.delete(jti)
    except:
        pass
    finally:
        return True
