import configparser


def get_list(self, section, option):
    strval = self.get(section, option)
    return [v.strip() for v in strval.split(",")]


def load_properties(proppath):
    config = configparser.ConfigParser()
    config.read(proppath)
    config.getlist = get_list
    return config
