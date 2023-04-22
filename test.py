import unittest
from main import ExpenseTracker
import json


class MyTest(unittest.TestCase):

    def setUp(self) -> None:
        self.expense_tracker = ExpenseTracker()

    # MAIN.PY
    def test_get_conversion(self):
        result = self.expense_tracker.get_HUF_base_USD("USD", "HUF")
        self.assertIsInstance(result, str)

    def test_convert_str_to_json(self):
        result = self.expense_tracker.get_HUF_base_USD("USD", "HUF")
        json_result = self.expense_tracker.convert_str_to_json(result)
        self.assertIsInstance(json_result, dict)

if __name__ == '__main__':
    unittest.main()