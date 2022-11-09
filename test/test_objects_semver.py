import unittest

import skelebot as sb

class TestSemver(unittest.TestCase):

    def test_representation(self):
        version = sb.objects.semver.Semver('1.2.3')
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(str(version), '1.2.3')

    def test_lt(self):
        a = sb.objects.semver.Semver('0.1.2')
        b = sb.objects.semver.Semver('1.1.2')
        c = sb.objects.semver.Semver('1.2.3')
        d = sb.objects.semver.Semver('1.2.10')
        self.assertTrue(a < b)
        self.assertTrue(b < c)
        self.assertTrue(c < d)

    def test_eq(self):
        a = sb.objects.semver.Semver('1.2.3')
        b = sb.objects.semver.Semver('1.2.3')
        c = sb.objects.semver.Semver('1.2.4')
        d = sb.objects.semver.Semver('1.4.3')
        e = sb.objects.semver.Semver('2.2.3')
        self.assertEqual(a, b)
        # Different patch
        self.assertNotEqual(a, c)
        # Different minor
        self.assertNotEqual(a, d)
        # Different major
        self.assertNotEqual(a, e)

    def test_le(self):
        a = sb.objects.semver.Semver('1.2.3')
        b = sb.objects.semver.Semver('1.2.3')
        c = sb.objects.semver.Semver('2.2.3')
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)

    def test_isBackwardCompatible(self):
        a = sb.objects.semver.Semver('1.2.3')
        b = sb.objects.semver.Semver('1.2.10')
        c = sb.objects.semver.Semver('2.2.3')
        self.assertTrue(b.isBackwardCompatible(a))
        self.assertFalse(a.isBackwardCompatible(b))
        self.assertFalse(a.isBackwardCompatible(c))
        self.assertFalse(b.isBackwardCompatible(c))

if __name__ == '__main__':
    unittest.main()
