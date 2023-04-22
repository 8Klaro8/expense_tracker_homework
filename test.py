import unittest
from main import ExpenseTracker
import json
import datetime


class MyTest(unittest.TestCase):

    def setUp(self) -> None:
        self.PATH = "datas/expenses.json"
        self.expense_tracker = ExpenseTracker(self.PATH)
        self.examp_currs = ("USD", "HUF")
        self.amount = "6"

    # MAIN.PY
    # def test_get_conversion(self):
    #     result = self.expense_tracker.get_HUF_base_USD(*self.examp_currs)
    #     self.assertIsInstance(result, str)

    # def test_convert_str_to_json(self):
    #     result = self.expense_tracker.get_HUF_base_USD(*self.examp_currs)
    #     json_result = self.expense_tracker.convert_str_to_json(result)
    #     self.assertIsInstance(json_result, dict)

    # def test_convert_currency(self):
    #     result = self.expense_tracker.convert_currency(*self.examp_currs, self.amount)
    #     self.assertIsInstance(result, str)

    # def test_ask_expense(self):
    #     expense = self.expense_tracker.ask_expense()
    #     self.assertIsInstance(expense, int)

    # def test_file_does_not_exists(self):
    #     does_exist = self.expense_tracker.file_exists()
    #     self.assertFalse(does_exist)

    # def test_file_exists(self):
    #     does_exist = self.expense_tracker.file_exists()
    #     self.assertTrue(does_exist)

    # def test_save_expense_when_file_doesnt_exsits(self):
    #     self.expense_tracker.save_expesne("Jani", "312")

    # def test_get_date(self):
    #     todays_date_ref = datetime.datetime.now().date()
    #     todays_date_func = self.expense_tracker.get_date()
    #     self.assertEqual(todays_date_func, todays_date_ref)

    def test_save_expesne_when_file_exists(self):
        self.expense_tracker.save_expesne("user", "5454")


if __name__ == '__main__':
    unittest.main()

    # python -m unittest -k test_save_expesne_when_file_exists
