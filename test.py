import unittest
from main import ExpenseTracker, MyManager
import json
import datetime


class MyTest(unittest.TestCase):

    def setUp(self) -> None:
        self.USER_FILE = "datas/expenses.json"
        self.PASSWORD_FILE = "datas/passwords.json"
        self.LOGGED_IN_USER = "datas/logged_in_user.txt"
        self.expense_tracker = ExpenseTracker(self.USER_FILE, self.PASSWORD_FILE, self.LOGGED_IN_USER)
        self.example_user = "user"
        self.my_manager = MyManager(self.expense_tracker)
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
    #     self.expense_tracker.save_expense("Jani", "312")

    # def test_get_date(self):
    #     todays_date_ref = str(datetime.datetime.now().date())
    #     todays_date_func = self.expense_tracker.get_date()
    #     self.assertEqual(todays_date_func, todays_date_ref)

    # def test_save_expense_when_file_exists(self):
    #     self.expense_tracker.save_expense("user1", "33333")

    # def test_get_expenses_by_user(self):
    #     expenses = self.expense_tracker.get_expenses_by_user("user1")
    #     self.assertEqual(['1111', '2222', '33333'], expenses)


    # def test_get_expenses_by_user_and_datum(self):
    #     expenses = self.expense_tracker.get_expenses_by_user_and_datum("user1", "2023-04-22")
    #     self.assertEqual(["2222", "33333"], expenses)

    # def test_start(self):
    #     self.my_manager.start()

    # def test_get_all_available_currency(self):
    #     self.expense_tracker.get_all_available_currency()

    # def test_convert_currency(self):
    #     self.my_manager.convert_currency()

    # def test_starting_page(self):
    #     self.my_manager.starting_page()

    # def test_save_user(self):
    #     self.expense_tracker.save_user("BBB", "555")

    def test_start_page(self):
        self.my_manager.starting_page()

if __name__ == '__main__':
    unittest.main()

    # python -m unittest -k test_get_all_available_currency
