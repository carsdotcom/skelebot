from unittest import TestCase
from unittest import mock

import skelebot as sb
import os

class TestKerberos(TestCase):

    def test_appendDockerfile(self):
        kerberos = sb.components.kerberos.Kerberos(krbConf="krb/krb5.conf", keytab="krb/me.keytab")

        dockerfile = kerberos.appendDockerfile()
        expected = """COPY krb/krb5.conf /etc/krb5.conf
COPY krb/me.keytab /krb/auth.keytab
"""

        self.assertEqual(dockerfile, expected)

if __name__ == '__main__':
    unittest.main()
