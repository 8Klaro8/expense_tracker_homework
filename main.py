# from request import MyRequest
import json
import requests
from fixed_api_key import fixed_api_key
import datetime



class ExpenseTracker:
    def __init__(self, save_to_file: str) -> None:
        self.headers = {"apikey": fixed_api_key}
        self.file_to_save = save_to_file
        

    def get_HUF_base_USD(self, base: str, symbol: str) -> str:
        """ Gets the current value of one currency compare to an other"""
        url = f"https://api.apilayer.com/fixer/latest?base={base}&symbols={symbol}"
        response = requests.get(url=url, headers=self.headers)
        return response.text
    
    
    def convert_currency(self, base: str, convert_to: str, amount: str) -> str:
        url = f"https://api.apilayer.com/fixer/convert?from={base}&to={convert_to}& \
                amount={amount}"
        response = requests.get(url=url, headers=self.headers)
        return response.text
    
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

    def read_expense(self):
        """ Reads all expenses by user """
        if self.file_exists():
            with open(self.file_to_save, "r") as file:
                pass
    
    def save_expesne(self, user, expense):
        """ Saves expense to user """
        if self.file_exists():
            with open(self.file_to_save, "r") as file:
                pass
                # datas = file.read()
                # datas[user]
                # # TODO finsih it
        else:
            with open(self.file_to_save, "w") as file:
                my_dict = {"users": {"user": {"date": {str(self.get_date()): [expense]}}}}
                jsoned_dict = json.dumps(my_dict)
                file.write(jsoned_dict)

    def get_date(self) -> str:
        """ Returns today's date """
        return datetime.datetime.now().date()



    def file_exists(self) -> bool:
        """ Cheks if expenses.json exists """
        try:
            with open(self.file_to_save, "r") as file:
                file.read()
                return True
        except:
            return False



# if __name__ == '__main__':
#     e_t = ExpenseTracker("datas/expenses.json")
#     result = e_t.convert_currency("USD", "HUF", "5")
#     print(result)