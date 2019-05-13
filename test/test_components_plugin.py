from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os

class TestPlugin(TestCase):

    def test_addParsers(self):
        plugin = sb.components.plugin.Plugin()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = plugin.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["plugin"], None)

if __name__ == '__main__':
    unittest.main()
