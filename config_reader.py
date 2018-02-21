
import configparser

import os
import os.path

config_path_var = "MARIGOLD_CONFIG_PATH"
base_path = os.environ.get(config_path_var, "../")

def read(path):
    path = os.path.join(base_path, "{}.ini".format(path))

    parser = configparser.ConfigParser()
    parser.read(path)

    return parser
