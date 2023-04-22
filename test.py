import unittest
from main import ExpenseTracker
import json


class MyTest(unittest.TestCase):

    def setUp(self) -> None:
        self.expense_tracker = ExpenseTracker()
        self.examp_currs = ("USD", "HUF")
        self.amount = "6"

    # MAIN.PY
    def test_get_conversion(self):
        result = self.expense_tracker.get_HUF_base_USD(*self.examp_currs)
        self.assertIsInstance(result, str)

    def test_convert_str_to_json(self):
        result = self.expense_tracker.get_HUF_base_USD(*self.examp_currs)
        json_result = self.expense_tracker.convert_str_to_json(result)
        self.assertIsInstance(json_result, dict)

    def test_convert_currency(self):
        result = self.expense_tracker.convert_currency(*self.examp_currs, self.amount)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()