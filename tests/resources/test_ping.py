import unittest

from src.resources.ping import PingResource
from src.utils.response_builder import ResponseBuilder


class PingResourceTestCase(unittest.TestCase):

    def test_ping_ok(self):
        service = PingResource()
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.get(), 200)
