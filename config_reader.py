
import configparser

base_path = "../{}.ini"

def read(path):
    path = base_path.format(path)

    parser = configparser.ConfigParser()
    parser.read(path)

    return parser
