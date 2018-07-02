import unittest
from unittest.mock import MagicMock, patch

from src.resources.ping import PingResource
from src.utils.response_builder import ResponseBuilder


class PingResourceTestCase(unittest.TestCase):

    def test_ping_ok(self):
        with patch.object(ResponseBuilder, "build_response") as mocked_build_response:
            mocked_build_response.side_effect = lambda response, status_code: status_code
            service = PingResource()
            self.assertEqual(service.get(), 200)
