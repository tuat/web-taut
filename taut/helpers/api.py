import functools
from flask import jsonify, g

def json_error(status, message):
    message = {
        'status' : status,
        'message': message,
    }

    response = jsonify(error=message)
    response.status_code = status

    return response
