import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TWILIO_SID = os.environ['TWILIO_SID'] #Your TWILIO_SID
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN'] #Your TWILIO_AUTH_TOKEN
TWILIO_VIRTUAL_NUMBER = os.environ['TWILIO_VIRTUAL_NUMBER'] #Your TWILIO_VIRTUAL_NUMBER
TWILIO_VERIFIED_NUMBER = os.environ['TWILIO_VERIFIED_NUMBER'] #Your TWILIO_VERIFIED_NUMBER

class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def sends_email(self, my_email, my_password, user_email, message):
        msg = MIMEMultipart()
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # set up the message parameters
            msg['From'] = my_email
            msg['To'] = user_email
            msg['Subject'] = "Flight Deal"
            msg.attach(MIMEText(message, 'html'))
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs=user_email,
                msg=msg.as_string(),
            )