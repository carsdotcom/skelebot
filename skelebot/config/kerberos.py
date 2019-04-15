from .yaml import *

class Kerberos(YamlClass):
    'Config object for the kerberos authentication details'
    hdfsUser = None
    keytab = None
    krbConf = None

    def __init__(self, hdfsUser, keytab, krbConf):
        self.hdfsUser = hdfsUser
        self.keytab = keytab
        self.krbConf = krbConf

    @classmethod
    def getOrderedAttrs(cls):
        return ["hdfsUser", "keytab", "krbConf"]
