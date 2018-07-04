import unittest
from unittest.mock import patch, MagicMock

from src.model.flash import Flash
from src.resources.purge import PurgeResource, SERVER_TOKEN
from src.utils.response_builder import ResponseBuilder


class PurgeResourceTestCase(unittest.TestCase):

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_purge_wrong_token(self):
        with patch.object(ResponseBuilder, "build_error_response") as mocked_build_response,\
             patch.object(Flash, "delete_deprecated_flashes") as mocked_delete_flashes:

            mocked_build_response.side_effect = self.mocked_build_error_response
            mocked_delete_flashes.side_effect = MagicMock(return_value=0)

            service = PurgeResource()
            # not the right token
            service._get_token_from_header = MagicMock(return_value= SERVER_TOKEN + "sds")

            self.assertEqual(service.post(), 400)

    def test_purge_successful(self):
        with patch.object(ResponseBuilder, "build_response") as mocked_build_response,\
             patch.object(Flash, "delete_deprecated_flashes") as mocked_delete_flashes:

            mocked_build_response.side_effect = self.mocked_build_response
            amount_of_flashes_deleted = 10
            mocked_delete_flashes.side_effect = MagicMock(return_value=amount_of_flashes_deleted)

            service = PurgeResource()
            service._get_token_from_header = MagicMock(return_value=SERVER_TOKEN)

            expected_response = {'deleted': amount_of_flashes_deleted}

            self.assertEqual(service.post(), expected_response)