import requests
import os

BEARER_TOKEN = os.environ['BEARER_TOKEN'] #Your Sheety BEARER_TOKEN
SHEETY_PRICES_ENDPOINT = os.environ["SHEETY_PRICES_ENDPOINT"] #Your SHEETY_PRICES_ENDPOINT
SHEETY_USERS_ENDPOINT = os.environ["SHEETY_USERS_ENDPOINT"] #Your SHEETY_USERS_ENDPOINT

class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.user_data = {}
        self.bearer_headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        
    def get_destination_data(self):
        """ This function get the prices from the SHEETY_PRICES_ENDPOINT """
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=self.bearer_headers)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        """ This update the IATA city code """
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self.bearer_headers,
            )

    def create_user(self):
        """ This function gets inputs from the user and it posts everything to the  SHEETY_USERS_ENDPOINT """
        name_input = input("What is your name:\n").title()
        last_name_input = input("What is your last name:\n")
        email_input = input("What is your email:\n")
        confirm_email_input = input("Type your email again:\n")

        while confirm_email_input != email_input:
            print("The second email wasn't equal to the first one.\nPlease enter your email again")
            email_input = input("What is your email:\n")
            confirm_email_input = input("Type your email again:\n")

        user_data = {
            "user": {
                "firstName": name_input,
                "lastName": last_name_input,
                "email": confirm_email_input,
            }
        }
        response = requests.post(url=SHEETY_USERS_ENDPOINT, json=user_data, headers=self.bearer_headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f'An HTTP error occurred: {error}')
        else:
            print("Your data has been successfully added!")

    def get_user_data(self):
        """ This function get the user data from the SHEETY_USERS_ENDPOINT """
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.bearer_headers)
        data = response.json()
        self.user_data = data["users"]
        return self.user_data