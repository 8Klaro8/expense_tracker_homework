# from request import MyRequest
import json
import requests
from fixed_api_key import fixed_api_key



class ExpenseTracker:
    def __init__(self) -> None:
        # self.my_request = MyRequest()
        self.headers = {"apikey": fixed_api_key}
        

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
        while True:
            expense = input("Write your expense:\n").strip()
            try:
                return int(expense)
            except:
                print("Type only number!")
                continue


if __name__ == '__main__':
    e_t = ExpenseTracker()
    result = e_t.convert_currency("USD", "HUF", "5")
    print(result)