"""Main testing module"""
import unittest
from flask import json
from src import main


class MainTest(unittest.TestCase):
    """Testing class"""
    def setUp(self):
        """Testing set up"""
        self.app = main.app.test_client()
        self.app.testing = True

    def test(self):
        """Main test"""
        home = self.app.get('/')
        self.assertEqual(json.loads(home.data)['id'], 'someOtherId')


if __name__ == '__main__':
    unittest.main()
