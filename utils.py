from configparser import ConfigParser


def getConfig(configFile="config/base.cfg"):
    """
    Returns a config object
    :param configFile: The config file to load
    """

    conf = ConfigParser()
    conf.read(configFile)

    return conf
