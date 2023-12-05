import unittest
from logging_and_error_handling import perform_division


class TestLoggingAndErrorHandling(unittest.TestCase):
    def test_perform_division(self):
        result = perform_division(10, 2)
        self.assertEqual(result, 5.0)

    def test_perform_division_by_zero(self):
        result = perform_division(10, 0)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
