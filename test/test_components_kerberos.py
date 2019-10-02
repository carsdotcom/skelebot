import copy
import unittest

from schema import SchemaError

import skelebot as sb

class TestKerberos(unittest.TestCase):

    kerberos = {
        "krbConf": "test",
        "keytab": "test",
        "hdfsUser": "test"
    }

    def test_appendDockerfile(self):
        kerberos = sb.components.kerberos.Kerberos(krbConf="krb/krb5.conf", keytab="krb/me.keytab")

        dockerfile = kerberos.appendDockerfile()
        expected = """COPY krb/krb5.conf /etc/krb5.conf
COPY krb/me.keytab /krb/auth.keytab
"""

        self.assertEqual(dockerfile, expected)

    def test_validate_valid(self):
        try:
            sb.components.kerberos.Kerberos.validate(self.kerberos)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_validate_missing(self):
        kerberos = copy.deepcopy(self.kerberos)
        del kerberos["krbConf"]
        del kerberos["keytab"]
        del kerberos["hdfsUser"]

        try:
            sb.components.kerberos.Kerberos.validate(kerberos)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'hdfsUser', 'keytab', 'krbConf'")

    def validate_error(self, attr, reset, expected):
        kerberos = copy.deepcopy(self.kerberos)
        kerberos[attr] = reset

        try:
            sb.components.kerberos.Kerberos.validate(kerberos)
        except SchemaError as error:
            self.assertEqual(error.code, "Kerberos '{attr}' must be a{expected}".format(attr=attr, expected=expected))

    def test_invalid(self):
        self.validate_error('krbConf', 123, ' String')
        self.validate_error('keytab', 123, ' String')
        self.validate_error('hdfsUser', 123, ' String')

if __name__ == '__main__':
    unittest.main()
