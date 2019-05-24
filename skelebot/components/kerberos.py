from ..objects.component import *

# This component provides the ability authentice with Kerberos HDFS based on user config
class Kerberos(Component):
    activation = Activation.CONFIG

    krbConf = None
    keytab = None
    hdfsUser = None

    def __init__(self, krbConf=None, keytab=None, hdfsUser=None):
        self.krbConf = krbConf
        self.keytab = keytab
        self.hdfsUser = hdfsUser

    # Appends copy commands to the Dockerfile in order to add the needed Kerberos files to the correct location based on config
    def appendDockerfile(self):
        dockerfile = ""
        if (self.krbConf is not None) and (self.keytab is not None):
            dockerfile += "COPY {krb} /etc/krb5.conf\n".format(krb=self.krbConf)
            dockerfile += "COPY {keytab} /krb/auth.keytab\n".format(keytab=self.keytab)
        return dockerfile

    # If run inside of docker, execute the init.sh script with the username in order to initialize krb auth
    def prependCommand(self, job, native):
        return "/./krb/init.sh {user}".format(user=self.hdfsUser) if native == False else None
