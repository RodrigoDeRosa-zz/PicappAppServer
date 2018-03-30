import unittest
from flask import json
import os
import sys
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from src import main


class HomeResponseTest(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertEqual(json.loads(home.data)['id'], 'someOtherId')


if __name__ == "__main__":
    unittest.main()
