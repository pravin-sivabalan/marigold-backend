
import configparser 

def read():
    parser = configparser.ConfigParser()
    parser.read('../database.ini')

    return parser
