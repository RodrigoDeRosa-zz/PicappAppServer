"""Main testing module"""
import os
import sys
import inspect
import unittest
from flask import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from src import main


class MainTest(unittest.TestCase):
    """Testing class"""
    def setUp(self):
        """Testing set up"""
        self.app = main.APP.test_client()
        self.app.testing = True

    def test(self):
        """Main test"""
        home = self.app.get('/')
        self.assertEqual(json.loads(home.data)['id'], 'someOtherId')


if __name__ == '__main__':
    unittest.main()
