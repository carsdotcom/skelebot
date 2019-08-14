"""Kerberos Component"""

from schema import Schema, And
from ..objects.component import Activation, Component

class Kerberos(Component):
    """
    Kerberos Class

    Provides the ability authentice with Kerberos HDFS based on user config
    """

    activation = Activation.CONFIG

    schema = Schema({
        'krbConf': And(str, error='Kerberos \'krbConf\' must be a String'),
        'keytab': And(str, error='Kerberos \'keytab\' must be a String'),
        'hdfsUser': And(str, error='Kerberos \'hdfsUser\' must be a String')
    }, ignore_extra_keys=True)

    krbConf = None
    keytab = None
    hdfsUser = None

    def __init__(self, krbConf=None, keytab=None, hdfsUser=None):
        """Initialize the kerberos auth details when constructing the component object"""

        self.krbConf = krbConf
        self.keytab = keytab
        self.hdfsUser = hdfsUser

    def appendDockerfile(self):
        """
        Dockerfile Hook

        Appends copy commands to the Dockerfile in order to add the needed Kerberos files to the
        correct location based on the config
        """

        dockerfile = ""
        if (self.krbConf is not None) and (self.keytab is not None):
            dockerfile += "COPY {krb} /etc/krb5.conf\n".format(krb=self.krbConf)
            dockerfile += "COPY {keytab} /krb/auth.keytab\n".format(keytab=self.keytab)
        return dockerfile

    def prependCommand(self, job, native):
        """
        CommandBuilder Hook

        If run inside of docker, execute the init.sh script with the username in order to
        initialize krb auth so that the user can access HDFS inside the container
        """

        return "/./krb/init.sh {user}".format(user=self.hdfsUser) if native is False else None
