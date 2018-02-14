
from flask import Blueprint, jsonify
import json

class Error(Exception):
    def to_dict(self):
        as_dict = dict(self.__dict__)
        as_dict["error_code"] = self.error_code
        as_dict["message"] = self.__doc__

        return json.dumps(as_dict)

def response_for_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
