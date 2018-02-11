
import configparser
import os

config_path_var = "MARIGOLD_CONFIG_PATH"
base_path = os.environ.get(config_path_var, "../{}.ini")

def read(path):
    path = base_path.format(path)

    parser = configparser.ConfigParser()
    parser.read(path)

    return parser
