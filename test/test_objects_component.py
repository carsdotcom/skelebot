import argparse
import unittest
from unittest import mock

import skelebot as sb

# Just a dummy component for testing
class StoreUtterance(sb.objects.component.Component):
    activation = sb.objects.component.Activation.ALWAYS
    utterance = None

    def __init__(self, utterance=None):
        self.utterance = utterance

    def scaffold(self):
        self.utterance = sb.systems.scaffolding.prompt.promptUser("Say something")
        return self.utterance

class TestComponent(unittest.TestCase):

    def setUp(self):
        self.component = StoreUtterance()

    @mock.patch('skelebot.systems.scaffolding.prompt.input')
    def test_scaffold(self, mock_input):
        mock_input.return_value = "Something awesome"

        self.component.scaffold()

        mock_input.assert_called_once_with("Say something: ")
        self.assertEqual(self.component.utterance, "Something awesome")

    def test_addParsers(self):
        parser = argparse.ArgumentParser()
        subparsers_before = parser.add_subparsers(dest="dummy")
        subparsers_after = self.component.addParsers(subparsers_before)

        self.assertEqual(subparsers_before, subparsers_after)

    def test_execute(self):
        self.assertIsNone(self.component.execute(1, 2, 3))

if __name__ == '__main__':
    unittest.main()
