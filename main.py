# Before to run this program this program run this commands:
# python3 -m venv venv
# pip3 install requests
# pip3 install twilio
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "" #Put your ORIGIN_CITY_IATA
MY_EMAIL = "" #Put your email here
MY_PASSWORD = "" #Put your AppPassword (take a look in google account -> Security --> App Password)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

print("Welcome to Matteo's Flights Club\nWe find the best flight deals and email you!")
# Create User
data_manager.create_user()

#Update the Google sheet file by entering the IATA codes that will be needed for the check_flights() function where it will use them as 'destinations'.
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# Get the actual date and the six month from today's date
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Looping into the ['prices'] Google sheet file
for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )

    # Contune the loop if the fligt is None
    if flight is None:
        continue

    # Check whether the new flight has a lower price than the flight with the lowest price within the Google Sheet file.
    if flight.price < destination["lowestPrice"]:
        message = f"Low price alert! Only €{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        # Check if the flight makes a stop_over
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        # get the user data
        user_data = data_manager.get_user_data()
        # Send an email to the user
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        email_body = f"""
            <html>
                <body>
                    <p>{message}</p>
                    <a href={link}>
                        {link}
                    </a>
                </body>
            </html>
        """
        for user in user_data:
            notification_manager.sends_email(
                my_email=MY_EMAIL, 
                my_password= MY_PASSWORD, 
                user_email=user["email"], 
                message=email_body,
            )
        # Send an sms to the user
        notification_manager.send_sms(message=message)