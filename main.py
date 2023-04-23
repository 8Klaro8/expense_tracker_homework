# from request import MyRequest
import json
import requests
from fixed_api_key import fixed_api_key
import datetime
from functools import reduce

class ExpenseTracker:
    def __init__(self, my_file: str) -> None:
        self.headers = {"apikey": fixed_api_key}
        self.my_file = my_file

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
        if self.file_exists():
            expenses = []
            json_datas = self.get_json_data_from_file()
            all_date = json_datas["users"][user]["date"]
            for date in all_date:
                expense_by_date = all_date[date]
                for expense in expense_by_date:
                    expenses.append(expense)
            return expenses

    def get_expenses_by_user_and_datum(self, user: str, datum: str):
        """ Returns all expenses by user and datum """
        if self.file_exists():
            expenses = []
            json_datas = self.get_json_data_from_file()
            all_expense_in_datum = json_datas["users"][user]["date"][datum]
            for expense in all_expense_in_datum:
                expenses.append(expense)
            return expenses
        
    def _simple_save(self, data):
        """ Saves whatever passed to json file """
        with open(self.my_file, "w") as file:
            file.write(data)
    
    def save_expense(self, user: str, expense: str):
        """ Saves expense to user """
        if self.file_exists():
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

    def file_exists(self) -> bool:
        """ Cheks if expenses.json exists """
        try:
            with open(self.my_file, "r") as file:
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
    def __init__(self, expense_tracker) -> None:
        self.expense_tracker = expense_tracker
        self.user = "user"

    def start(self):
        while True:
            prompt = ("Choose...", "\n1.)\tAdd expense","2.)\tSee today's expenses",
                      "3.)\tSee all time expense","4.)\tConvert currency")
            choice = self.control_input(*prompt)

            match choice:
                case "1":
                    expense = self.loop_while_not_number("Expense:")
                    expense_tracker.save_expense(self.user, expense)
                    print(f"\n========================\nExpense ${expense}"
                          " has been added.\n========================\n")

                case "2":
                    self.show_todays_expenses()

                case "3":
                    self.show_all_time_expense()

                case "4":
                    self.convert_currency_panel()

    def convert_currency_panel(self):
        prompt = ("Choose...", "\n1.)\tConvert", "2.)\tSee avaialble currencies")
        choice = self.control_input(*prompt)

        match choice:
            case "1":
                self.choose_to_convert()
            case "2":
                available_currencies = expense_tracker.get_all_available_currency()
                for currency in available_currencies:
                    print(currency)

    def choose_to_convert(self):
        curr_from = input("\nCurrency to convert from...").upper()
        curr_to = input("Currency to convert to...").upper()
        amount = self.loop_while_not_number("Give amount...")
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
        all_time_expense = expense_tracker.get_expenses_by_user(self.user)
        sum_all_time_expense = reduce(lambda x,y: int(x) + int(y), all_time_expense)
        print(f"\n========================\nAll time expense: ${sum_all_time_expense}")
        print(f"Trasactions: {len(all_time_expense)}\n========================\n")

    def show_todays_expenses(self):
        todays_date = str(datetime.datetime.now().date())
        todays_expenses = expense_tracker.get_expenses_by_user_and_datum(self.user, todays_date)
        print("\n=================\nToday's expenses:")
        print(f"Total: ${reduce(lambda x, y: int(x) + int(y), todays_expenses) }")
        print(f"Trasactions: {len(todays_expenses)}")
        for expense in todays_expenses:
            print(f"${expense}")
        print("=================\n")

    def loop_while_not_number(self, text) -> str:
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
                    
    def control_input(self, *text: str) -> str:
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
                if int(user_input) > (len(text) -1 ) or int(user_input) < 1:
                    print("\n==================\nChoose valid number"
                          "\n==================\n")
                    continue
                else:
                    break


        return user_input

expense_tracker = ExpenseTracker("datas/expenses.json")
my_manager = MyManager(expense_tracker)


# if __name__ == '__main__':
#     e_t = ExpenseTracker("datas/expenses.json")
#     result = e_t.convert_currency("USD", "HUF", "5")
#     print(result)