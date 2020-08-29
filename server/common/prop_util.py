import configparser


def load_properties(proppath):
    config = configparser.ConfigParser()
    config.read(proppath)
    return config
