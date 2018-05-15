import unittest
import unittest.mock as mock
from src.security.input_sanitizer import InvalidFormatException, InputSanitizer


class InputSanitizerTestCase(unittest.TestCase):

    def test_successful_sanitize_boolean_true(self):
        data_input = "true"
        expected_output = True
        self.assertEqual(InputSanitizer.sanitize_boolean(data_input),expected_output)

    def test_successful_sanitize_boolean_false(self):
        data_input = "False"
        expected_output = False
        self.assertEqual(InputSanitizer.sanitize_boolean(data_input), expected_output)

    def test_failed_sanitize_boolean(self):
        data_input = "asd"
        with self.assertRaises(InvalidFormatException):
            InputSanitizer.sanitize_boolean(data_input)

    def test_successful_sanitize_positive_integer(self):
        data_input = "12151213"
        expected_output = 12151213
        self.assertEqual(InputSanitizer.sanitize_integer(data_input), expected_output)

    def test_successful_sanitize_negative_integer(self):
        data_input = "-51213"
        expected_output = -51213
        self.assertEqual(InputSanitizer.sanitize_integer(data_input), expected_output)

    def test_failed_sanitize_integer(self):
        data_input = "not_an_integer"
        with self.assertRaises(InvalidFormatException):
            InputSanitizer.sanitize_integer(data_input)