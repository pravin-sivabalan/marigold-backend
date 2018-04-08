
import os.path
from pathlib import Path

import pickle

cache_folder = Path(os.path.dirname(__file__), "cache")

def open(name, perm="r"):
    return (cache_folder / name).open(perm)

def dump(name, obj):
    with open(name, "wb") as fp:
        pickle.dump(obj, fp) 

def load(name):
    with open(name, "rb") as fp:
        return pickle.load(fp)

