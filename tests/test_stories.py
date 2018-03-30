import unittest
from flask import json
from src import stories


class HomeResponseTest(unittest.TestCase):

    def setUp(self):
        self.app = stories.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertEqual(json.loads(home.data)['id'], 'someOtherId')


if __name__ == "__main__":
    unittest.main()
