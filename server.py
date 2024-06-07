import os
import requests
import json
from dotenv import load_dotenv
from read_phone_numbers import read_kenyan_phone_numbers

load_dotenv()

apikey = os.getenv('apikey')
partnerID = os.getenv('partnerID')
pass_type = os.getenv('pass_type')
file_name = 'sample.csv'
phone_numbers = read_kenyan_phone_numbers(file_name)
message = "Welcome to Toppline Kenya. Welcome to our monthly offers"
shortcode = 'TOPPLINE KE'
url = 'https://sms.textsms.co.ke/api/services/sendbulk/'


def send_sms(phone_numbers, message):
    """
    Sends an SMS message to a list of phone numbers using the
    TextSMS API.

    Args:
        phone_numbers (list): A list of phone numbers (strings)
        to send the SMS to.
        message (str): The message content to be sent.

    Return:
        None: This function does not return any value.
    Raises:
        Exception: If the SMS sending fails due to an error
        response from the API.
    """
    def chunk_list(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    chunks = list(chunk_list(phone_numbers, 20))
    headers = {
        'Content-Type': 'application/json'
    }

    for index, chunk in enumerate(chunks):
        contacts = [
            {
                "partnerID": partnerID,
                "apikey": apikey,
                "pass_type": pass_type,
                "clientsmsid": i + (index * 20),
                "mobile": phone_number,
                "message": message,
                "shortcode": shortcode
            } for i, phone_number in enumerate(chunk)
        ]

        payload = {
            'count': len(contacts),
            'smslist': contacts
        }

        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))

        if response.status_code == 200:
            print(f"Batch {index + 1}/{len(chunks)}:"
                  f"Messages sent successfully")
        else:
            print(f"Batch {index + 1}/{len(chunks)}:"
                  f"Failed to send messages, status code:"
                  f"{response.status_code}")
            print(response.text)


if __name__ == '__main__':
    send_sms(phone_numbers, message)
