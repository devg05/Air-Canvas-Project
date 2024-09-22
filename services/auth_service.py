'''JWT Tokens will be managed here ie creation or deletion or refresh'''

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

def generate_tokens(user_identity):
    access_token = create_access_token(identity=user_identity)
    refresh_token = create_refresh_token(identity=user_identity)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def decode_jwt_token(token):
    try:
        decoded = decode_token(token)
        return decoded
    except Exception as e:
        return None
