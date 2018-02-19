
from flask import Blueprint, jsonify
import json

class Error(Exception):
    def to_dict(self):
        as_dict = dict(self.__dict__)
        as_dict["error_code"] = self.error_code
        as_dict["message"] = self.__doc__
        as_dict["name"] = type(self).__name__

        return as_dict

class MissingDataError(Error):
    """A field in the request body is missing"""
    status_code = 400
    error_code = 10

    def __init__(self, err):
        self.key = err.args[0]

def response_for_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
