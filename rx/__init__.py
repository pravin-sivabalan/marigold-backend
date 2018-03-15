"""
This module contains helper methods for working with the NIH rx* family of apis
"""

import requests as req

url = "https://rxnav.nlm.nih.gov/REST/"

def get(path, params):
    return req.get(url + path, params=params)
