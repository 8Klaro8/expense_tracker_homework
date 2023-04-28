# from request import MyRequest
import json
import requests
from fixed_api_key import fixed_api_key
import datetime
from functools import reduce
import keyboard

class ExpenseTracker:
    def __init__(self, my_file: str, password_file: str, logged_in_user: str) -> None:
        self.headers = {"apikey": fixed_api_key}
        self.my_file = my_file
        self.password_file = password_file
        self.logged_in_user = logged_in_user

    def save_user(self, username, password):
        """Saves user to password file"""
        user_and_password = {username: password}
        if self.file_exists(self.password_file):
            with open(self.password_file, 'r', encoding="utf-8") as file:
                datas = file.read()
                if datas.strip() == "": 
                    with open(self.password_file, "w", encoding="utf-8") as file:
                        dumped_data = json.dumps({"users": {username: password}})
                        file.write(dumped_data)
                else:
                    json_datas = json.loads(datas)
                    json_datas["users"].update({username: password})
                    with open(self.password_file, "w", encoding="utf-8") as file:
                        json_user_and_password = json.dumps(json_datas)
                        file.write(json_user_and_password)
        else:
            with open(self.password_file, "w", encoding="utf-8") as file:
                json_user_and_password = json.dumps({"users": user_and_password})
                file.write(json_user_and_password)

    def get_HUF_base_USD(self, base: str, symbol: str) -> str:
        """ Gets the current value of one currency compare to an other"""
        url = f"https://api.apilayer.com/fixer/latest?base={base}&symbols={symbol}"
        response = requests.get(url=url, headers=self.headers)
        return response.text  
    
    def get_converted_currency(self, base: str, convert_to: str, amount: str) -> str:
        """ Calls API and converts currency and returns converted value """
        url = f"https://api.apilayer.com/fixer/convert?from={base}&to={convert_to}& \
                amount={amount}"
        response = requests.get(url=url, headers=self.headers)
        return response.json()["result"]
    
    def convert_str_to_json(self, value: str) -> json:
        """ Converts given value to dict """
        json_result =  json.loads(value)
        return json_result
    
    def ask_expense(self) -> int:
        """ Asks the user to give an input as expense."""
        while True:
            expense = input("Write your expense:\n").strip()
            try:
                return int(expense)
            except:
                print("Type only number!")
                continue

    def get_expenses_by_user(self, user: str) -> list:
        """ Returns all expenses by user """
        if self.file_exists(self.my_file):
            expenses = []
            json_datas = self.get_json_data_from_file()
            try:
                all_date = json_datas["users"][user]["date"]
                for date in all_date:
                    expense_by_date = all_date[date]
                    for expense in expense_by_date:
                        expenses.append(expense)
                return expenses
            except:
                print("\n========================\nYou have no transaction yet."
                      "\n========================")
                return

    def get_expenses_by_user_and_datum(self, user: str, datum: str):
        """ Returns all expenses by user and datum """
        if self.file_exists(self.my_file):
            expenses = []
            json_datas = self.get_json_data_from_file()
            try:
                all_expense_in_datum = json_datas["users"][user]["date"][datum]
                for expense in all_expense_in_datum:
                    expenses.append(expense)
                return expenses
            except:
                print("\n========================\nYou have no transaction yet."
                      "\n========================")
                return
        
    def _simple_save(self, data):
        """ Saves whatever passed to json file """
        with open(self.my_file, "w") as file:
            file.write(data)
    
    def save_expense(self, user: str, expense: str):
        """ Saves expense to user """
        if self.file_exists(self.my_file):
                json_datas = self.get_json_data_from_file()
                # CHECK IF USER EXISTS
                try:
                    curr_user_datas = json_datas["users"][user]
                    # CHECK IF DATE EXISTS
                    try:
                        expenses = curr_user_datas["date"][self.get_date()]
                        expenses.append(expense)
                        json_datas["users"][user]["date"][self.get_date()] = expenses
                        string_data = json.dumps(json_datas)
                        self._simple_save(string_data)


                    except:
                        json_datas["users"][user]["date"][self.get_date()] = [expense]
                        string_data = json.dumps(json_datas)
                        self._simple_save(string_data)
                except:
                    json_datas["users"].update({user: {"date": {self.get_date(): [expense]}}})
                    string_data = json.dumps(json_datas)
                    self._simple_save(string_data)

        else:
            with open(self.my_file, "w") as file:
                my_dict = {"users": {"user": {"date": {self.get_date(): [expense]}}}}
                jsoned_dict = json.dumps(my_dict)
                file.write(jsoned_dict)
        
    def get_json_data_from_file(self) -> dict:
        """ Reads and retuns the expenses data in dict """
        with open(self.my_file, 'r') as file:
            datas = file.read()
            return json.loads(datas)

    def get_date(self) -> str:
        """ Returns today's date """
        return str(datetime.datetime.now().date())

    def file_exists(self, file_path) -> bool:
        """ Cheks if expenses.json exists """
        try:
            with open(file_path, "r") as file:
                file.read()
                return True
        except:
            return False

    def get_all_available_currency(self) -> list:
        """ Returns all available currency """
        all_currency_shorts = []
        url = f"https://api.apilayer.com/fixer/symbols"
        response = requests.get(url, self.headers)
        all_currency = response.json()["symbols"]
        for key, value in all_currency.items():
            all_currency_shorts.append(key)
        return all_currency_shorts


class MyManager:
    def __init__(self, expense_tracker: ExpenseTracker) -> None:
        self.expense_tracker = expense_tracker
    def starting_page(self):
        """Very first page the user sees"""
        values = ("Choose", "\n1.)\tLogin", "2.)\tRegister")
        choice = self._control_input(*values)
        match choice:
            case "1":
                self.login_page()
            case "2":
                self.register_page()

    def start(self):
        """Shows the starting page after login/ register"""
        while True:
            prompt = ("Choose...", "\n1.)\tAdd expense", "2.)\tSee today's expenses",
                      "3.)\tSee all time expense", "4.)\tConvert currency", "5.)\tLog out")
            choice = self._control_input(*prompt)

            match choice:
                case "1":
                    expense = self._loop_while_not_number("Expense:")
                    expense_tracker.save_expense(self.get_logged_user(), expense)
                    print(f"\n========================\nExpense ${expense}"
                          " has been added.\n========================\n")

                case "2":
                    self.show_todays_expenses()

                case "3":
                    self.show_all_time_expense()

                case "4":
                    self.convert_currency_panel()
                case "5":
                    self.log_out_user()

    def login_page(self):
        """Creates a login page"""
        while True:
            username = input("Username:\n")
            if self.does_user_exists(username):
                password = input("Password:\n")
                if self.does_password_match(username, password):
                    self.save_logged_user(username)
                    self.start()

            else:
                print("\n================================\n"
                      "User does not exists!\n"
                      "================================"
                      "\nPress 'b' to go back...")
                
                user_choice = input("Press 'b' to go back or enter to try again.")
                if user_choice.lower()== "b":
                    self.starting_page()
                else:
                    continue

    def log_out_user(self):
        with open(self.expense_tracker.logged_in_user, "w") as file:
            file.write("")
        self.starting_page()

    def get_logged_user(self) -> str:
        """Retuns the currently logged in user"""
        with open(self.expense_tracker.logged_in_user, "r") as file:
            return file.read()

    def save_logged_user(self, user):
        """ Saves the user when he is logged in"""
        with open(self.expense_tracker.logged_in_user, "w") as file:
            file.write(user)

    def does_password_match(self, user: str, password: str) -> bool:
        """ Checks whether the password matched or not"""
        with open(self.expense_tracker.password_file, "r") as file:
            datas = file.read()
            json_datas = json.loads(datas)
            saved_password = json_datas["users"][user]
            if saved_password == password:
                return True
            return False

    def does_user_exists(self, user: str) -> bool:
        """Checks whether the user exists"""
        with open(self.expense_tracker.password_file, "r") as file:
            datas = file.read()
            json_datas = json.loads(datas)
            try:
                json_datas["users"][user]
                return True
            except Exception:
                return False

    def register_page(self):
        """Opens the regster page"""
        username = input("\nGive a username...\n")
        password = input("Give a password...\n")
        self.expense_tracker.save_user(username, password)
        self.save_logged_user(username)
        self.start()

    def convert_currency_panel(self):
        """ Prompt options what user want to do before converting"""
        prompt = ("Choose...", "\n1.)\tConvert", "2.)\tSee avaialble currencies")
        choice = self._control_input(*prompt)

        match choice:
            case "1":
                self.choose_to_convert()
            case "2":
                available_currencies = expense_tracker.get_all_available_currency()
                for currency in available_currencies:
                    print(currency)

    def choose_to_convert(self):
        """ Asks user to give currencies which the suer want to convert """
        curr_from = input("\nCurrency to convert from...").upper()
        curr_to = input("Currency to convert to...").upper()
        amount = self._loop_while_not_number("Give amount...")
        converted_amount = expense_tracker.get_converted_currency(curr_from, curr_to, amount)

        currency_sign = ""
        if curr_to == "USD":
            currency_sign = "$"
        elif curr_to == "HUF":
            currency_sign = "Ft "
        elif curr_to == "EUR":
            currency_sign = "€"

        print(f"\n======================\nConverted rate: {currency_sign}"
              f"{converted_amount}\n======================")
        input("Type anythnig to continue...")

    def show_all_time_expense(self):
        """ Shows the all time expense of the user"""
        all_time_expense = expense_tracker.get_expenses_by_user(self.get_logged_user())
        try:
            sum_all_time_expense = reduce(lambda x, y: int(x) + int(y), all_time_expense)
            print(f"\n========================\nAll time expense: ${sum_all_time_expense}")
            print(f"Trasactions: {len(all_time_expense)}\n========================\n")
        except Exception:
            print("\n========================\nYou have no transaction yet."
                  "\n========================")
            return

    def does_user_have_transaction(self, user: str) -> bool:
        json_datas = self.expense_tracker.get_json_data_from_file()
        try:
            json_datas["users"][user]["date"][self.expense_tracker.get_date()]
            return True
        except Exception:
            return False

    def show_todays_expenses(self):
        """ Shows today's expense of the user """
        if self.does_user_have_transaction(self.get_logged_user()):
            todays_date = str(datetime.datetime.now().date())
            todays_expenses = expense_tracker.get_expenses_by_user_and_datum(self.get_logged_user(),
                                                                             todays_date)
            print("\n=================\nToday's expenses:")
            print(f"Total: ${reduce(lambda x, y: int(x) + int(y), todays_expenses) }")
            print(f"Trasactions: {len(todays_expenses)}")
            for expense in todays_expenses:
                print(f"${expense}")
            print("=================\n")
        else:
            print("\n========================\nYou have no transaction yet."
                  "\n========================")
            return

    def _loop_while_not_number(self, text) -> str:
        """ Loops until user doesnt give valid expense """
        while True:
            choice = input(f"{text}\n")
            if choice.strip().isalpha():
                print("\n==================\nGive number only"
                      "\n==================\n")
                continue
            else:
                break
        return choice

    def _control_input(self, *text: str) -> str:
        """ Loops while input is not correct """
        while True:
            if len(text) > 1:
                for i in range(1, len(text)):
                    print(text[i])
            user_input = input(f"{text[0]}\n")

            if user_input.strip().isalpha():
                print("\n=====================\nType number "
                      "only.\n=====================\n")
                continue
            else:
                if int(user_input) > (len(text) - 1) or int(user_input) < 1:
                    print("\n==================\nChoose valid number"
                          "\n==================\n")
                    continue
                else:
                    break
        return user_input

if __name__ == '__main__':
    USER_FILE = "datas/expenses.json"
    PASSWORD_FILE = "datas/passwords.json"
    LOGGED_IN_USER = "datas/logged_in_user.txt"
    expense_tracker = ExpenseTracker(USER_FILE, PASSWORD_FILE, LOGGED_IN_USER)
    my_manager = MyManager(expense_tracker)
    my_manager.starting_page()
