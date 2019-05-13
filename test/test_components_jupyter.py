from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os

class TestJupyter(TestCase):

    def test_addParsers(self):
        jupyter = sb.components.jupyter.Jupyter(port=1127, folder="notebooks/")

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = jupyter.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["jupyter"], None)

if __name__ == '__main__':
    unittest.main()
