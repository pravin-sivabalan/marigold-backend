
from flask import Blueprint, jsonify

class Error(Exception):
    def to_dict(self):
        return {
            "code": self.error_code,
            "message": self.__doc__,
        }

def response_for_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
