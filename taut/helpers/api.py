import functools
from flask import jsonify, g, request

def require_token(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        token = request.args.get('token', None)

        if not token:
            return json_error(400, 'Please provide token')

        return method(*args, **kwargs)
    return wrapper

def json_error(status, message):
    message = {
        'status' : status,
        'message': message,
    }

    response = jsonify(error=message)
    response.status_code = status

    return response
