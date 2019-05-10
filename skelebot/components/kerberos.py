from ..objects.component import *

# This component provides the ability authentice with Kerberos HDFS based on user config
class Kerberos(Component):
    activation = Activation.CONFIG

    krbConf = None
    keytab = None

    def __init__(self, krbConf=None, keytab=None):
        self.krbConf = krbConf
        self.keytab = keytab

    # Appends copy commands to the Dockerfile in order to add the needed Kerberos files to the correct location based on config
    def appendDockerfile(self):
        dockerfile = ""
        if (self.krbConf is not None) and (self.keytab is not None):
            dockerfile += "COPY {krb} /etc/krb5.conf\n".format(krb=self.krbConf)
            dockerfile += "COPY {keytab} /krb/auth.keytab\n".format(keytab=self.keytab)
        return dockerfile
