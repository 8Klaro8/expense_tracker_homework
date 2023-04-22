# from request import MyRequest
import json
import requests
from fixed_api_key import fixed_api_key



class ExpenseTracker:
    def __init__(self) -> None:
        # self.my_request = MyRequest()
        pass

    def get_HUF_base_USD(self, base: str, symbol: str) -> str:
        """ Gets the current value of one currency compare to an other"""

        url = f"https://api.apilayer.com/fixer/latest?base={base}&symbols={symbol}"
        headers = {"apikey": fixed_api_key}
        response = requests.get(url=url, headers=headers)
        return response.text
    
    def convert_str_to_json(self, value: str) -> json:
        """ Converts given value to dict """

        json_result =  json.loads(value)
        return json_result
    
