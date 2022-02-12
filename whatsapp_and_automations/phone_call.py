
# from twilio.rest import Client
# import time


# # # Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# # # and use the E.164 format, for example: "+12025551234"
# TWILIO_PHONE_NUMBER = "+917814891872"

# # list of one or more phone numbers to dial, in "+19732644210" format
# DIAL_NUMBERS = ["+919988994191",]


# client = Client("AC28e41e6510a5ce033f7e16e86eab9df6", "67b15f0dab366a71f32e6a4a075a2145")


# def dial_numbers(numbers_list):
#     """Dials one or more phone numbers from a Twilio phone number."""
#     for number in numbers_list:
#         print("Dialing " + number)
#         # set the method to "GET" from default POST because Amazon S3 only
#         # serves GET requests on files. Typically POST would be used for apps
#         client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,
#                             #url=TWIML_INSTRUCTIONS_URL, 
#                             method="GET",
#                               twiml=f'<Response><Say>hello samridhi malhan ,  Im here to irritate you {time.sleep(2)} now you can go bye golu </Say></Response>')


# if __name__ == "__main__":
#     dial_numbers(DIAL_NUMBERS)



'''plivo'''



'''bandwith '''
# from os import getenv
# import time
# import messagebird

# # get system enviornment variable
# ACCESS_KEY =  getenv('MESSAGEBIRD_TEST_API') # test
# ACCESS_KEY2 =  getenv('MESSAGEBIRD_LIVE_API') # live

# #create instance of messagebird.Client using API key
# client = messagebird.Client(ACCESS_KEY2)

# try:
#     msg = client.voice_message_create(
#          '+917814891872', 
#          f'Hey Tushar Malhan   you have an appointment today at 10:00 am',
#           { 'voice' : 'male' })
#     print(msg.__dict__)

# except messagebird.client.ErrorException as e:
#     for error in e.errors:
#         print(error)

