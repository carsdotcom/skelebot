from unittest import TestCase
import skelebot as sb

class TestConfigKerberos(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        yaml = sb.config.Kerberos("sshookman", "sshookman.keytab", "krb5.conf").getYaml()
        expected = """hdfsUser: sshookman
keytab: sshookman.keytab
krbConf: krb5.conf
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
