import json
import pyautogui as pt  
import pywhatkit
import pyperclip as pc
import re
import sys

from datetime import datetime, date
from numpy import e
from pynput.mouse import Button, Controller
from time import sleep


pt.FAILSAFE = True
JSON_FILE = 'whatsapp_automation\MOCK_DATA.json'
mouse  = Controller()
DOCTORS_ID, date_set_by_user, confirmation_of_user, name_specialization_location, time_period_of_appointment, name_of_doc, days_tablets_required = None,None, None,'', '', '', ''
BASE_COMMAND = 'Please select the Doctor first  by typing the doctor id who is available the appointment'

CONTACT_NUMBER_OF_PHARMACY, MESSAGE_TO_PHARMACY = '', ''

JSON_FILE2 = 'whatsapp_automation\presciptions_MOCK_DATA.json'
COLUMN_CHECKED = 'RemindMe'

try:
    with open(JSON_FILE2, encoding="utf8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Not a valid JSON file")
    sys.exit()
try:
    Messages_tobe_delivered = [  (each_row) for each_row in data
    if each_row[COLUMN_CHECKED] is not None
    and each_row[COLUMN_CHECKED]]
except KeyError:
    print(f'No {COLUMN_CHECKED} data column in API')
    sys.exit()

try:
     with open(JSON_FILE, encoding="utf8") as f:
          data = json.load(f)
          names_id_of_doctors = ''.join(['   '.join(  str(each_data.get('doctorid'))+". "+each_data.get("name_of_doc").lower() for each_data in data)])
except:
     print("Not a valid JSON file")
     exit()

PHARMACY_NAMES_LIST = ' , '.join([ each_row['Prescriptions'][0]['PHARMACY_name'] for each_row in Messages_tobe_delivered   ])
PHARMACY_NAMES= [ each_row['Prescriptions'][0]['PHARMACY_name'].lower() for each_row in Messages_tobe_delivered   ]
TABLETS_LIST = [ each_row['Prescriptions'][2]['tablet_name'] for each_row in Messages_tobe_delivered   ]
tablet_name = TABLETS_LIST[0]
NO_OF_TABLETS = [ each_row['Prescriptions'][1]['no_of_tablets'] for each_row in Messages_tobe_delivered   ]


def validate_date(d):
    try:
        if len(d) == 10: 
            datetime.strptime(d, '%d/%m/%Y')
            return True
        else: return False

    except ValueError:
        return False


def navigate_to_image(image, clicks, off_x = 0, off_y = 0):
     """   image is the image to be searched for, 
           clicks is the number of times to click, 
           off_x and off_y are the offset from the center of the image 
           x == right horizontal, y == vertical MOVE
     """
     try:
          position = pt.locateOnScreen(image, confidence = .8)
     except:
          return f'\n{image}\n Image not found or Image is corrupted'
     if position is None:
          print(f'{image} \nImage Not Found')
     else:
          pt.moveTo(position, duration = .5)
          pt.moveRel(off_x, off_y, duration = .2)
          pt.click(clicks = clicks, interval = .1)


def copy_latest_msg():
     """  Get the new message from the client 
           and copy it to the clipboard &
           paste it to the terminal
           -> hardcode for my laptop  # pt.click(x=516, y=616)  
      """
     sleep(3)
     navigate_to_image(r'C:\Users\Tushar\Desktop\cloud_next\images\paperclip.png', 0, off_y = -70, off_x = 30)    
     pt.tripleClick()
     pt.hotkey('ctrl','c')
     return pc.paste()


def send_message(msg):
     """send a message in behalf of the client """
     navigate_to_image(r'C:\Users\Tushar\Desktop\cloud_next\images\paperclip.png', 2, off_x = 100)
     pt.typewrite(msg,interval=.001)          # type the message
     pt.typewrite('\n')                      # send the message


def process_message(msg):
          """ Revert to the replies of the client
          based on copy_latest_msg function  """
     
          raw_msg = msg.lower().strip()

          if raw_msg in('hello', 'hi', 'hey','hii','heyy','hey there','heyy there'):
               return 'Hi How can I help you?\n\
                    I am here to help you with your queries related to cloudnext.\n\
                    You can ask me about the following:\
                         \
                         \
                         \
                         \
                         1. What is cloudnext ?\
                         \
                         \
                         \
                         \
                         2. What can you do ?\
                         \
                         \
                         \
                         \
                         3. Book an appointment ?\
                         \
                         \
                         \
                         \
                         4. Show list of Doctors\
                         \
                         \
                         \
                         \
                         \
                         5. Respective Id of the Doctor to know more about them\
                         \
                         \
                         \
                         \
                         \
                         6. Ask to me to Do changes\
                         \
                         \
                         \
                         \
                         \
                         7. Ask to me to Cancel the appointment as well!\
                         \
                         \
                         \
                         \
                         \
                         8. Show Tablets & Book Tablets \
                         '
                         
          elif raw_msg in ('cloudnext', 'what is cloudnext ?','what is cloudnext'):
               return f'Cloudnext is a cloud based platform for medical services.\
                    It is a platform that provides a platform for doctors to provide their services to patients,\
                    allows you to book appointments with the doctors,\
                    provides a platform for patients to get medical reports from the doctors.\
                    Thus I am here to help you with your bookings with the Doctor as per your requirements.'

          elif raw_msg in ('what','?','how','when','what can you do','what can u do'):
               return 'Respected Client , I am here to give  all the details regarding the doctors we have , Book an appointment , Consultation and much more'
          
          elif raw_msg in ('bye','goodbye','see you','see you later','see you later'):
               return 'Bye, Have a good day'
          
          elif raw_msg in ('thanks','thank you','thank','thank you very much',
                         'great','good'):
               return 'You are welcome, Have a good day Ahead'
          
          elif raw_msg in ('book appointment','appointment','book','book an appointment',
                         'book an appointment for','book an appointment for doctor',
                         'book an appointment for doctor','book appointment',
                         'book an appointment for doctor','kindly book','book it'
                         'how can I book an appointment ?','how can I book an appointment'):
               return 'Sure We will definitely assist you on the same\
                    Kindly Choose a doctor by typing The Doctor ID from the list to know more about the Availablity and Time slots for the respective doctor or\
                    Type all to see all the doctors we have currently have !'
          
          elif raw_msg in [str(i) for i in range(1,11)] :
               global DOCTORS_ID, name_specialization_location, name_of_doc
               DOCTORS_ID = raw_msg
               try: # based on use input > we get doctor id and now we get name, specilization, location which we make global use for everyone
                    name_specialization_location = [ (  each_row['name_of_doc'].upper() ,each_row['specilization'],each_row['location'],each_row['availability']) for each_row in data if each_row['doctorid'] ==  int(raw_msg)]
                    availability = ' '.join([ 'Yes ,The Doctor would be availabile\n Kindly Confirm the date for slots Bookings in "dd/mm/yy"  format : ' for each_row in data if each_row['doctorid'] ==  int(raw_msg) and each_row['availability']   ])
               except NameError:
                    return('Error in fetching the JSON data')
               name_of_doc = ''.join( name_specialization_location[0][0])
          
               if availability:
                    for specific_detail_in_each_row in name_specialization_location:
                         return f" Doctor's name - { specific_detail_in_each_row[0] }   \
                              \
                         Location - {specific_detail_in_each_row[2]}  \
                              \
                              \
                         Specialized in - {specific_detail_in_each_row[1]}  \
                              \
                         Availability - {availability }\
                              \
                              "
               else:
                    DOCTORS_ID = None
                    for specific_detail_in_each_row in name_specialization_location:
                         return f" Doctor's name - { specific_detail_in_each_row[0] }     Location - {specific_detail_in_each_row[2]}  \
                                   \
                              Specialized in - {specific_detail_in_each_row[1]}  \
                                   \
                              Availability - Sorry,  Doctor {name_of_doc} is not available at the moment \
                                   \
                              "
     
          elif validate_date(raw_msg):              
               if DOCTORS_ID is not None:
                    global date_set_by_user 
                    date_set_by_user = raw_msg
                    print('VALIDATED DATE BY USER ',date_set_by_user)
                    try:
                         dt = datetime.strptime(raw_msg, '%d/%m/%Y').date()
                    except ValueError:
                         dt = None
                    today = date.today()
                    print(dt)
                    if dt and dt >= today and dt.year <= today.year+2 and date_set_by_user is not None :
                         return f'Do you want Morning or Evening Timings for Dr {name_of_doc}...'
                    else:
                         return 'Sorry the date is not valid as we cant book appointment for yesterday or past dates or future dates above 2 years'
               else:
                    return 'Please select a Doctor first by typing the doctor id'

          elif raw_msg in ('morning','mor','evening','eve','even'):
               if DOCTORS_ID is not None:
                    if raw_msg in ('morning','mor'):
                         return f'Here  are the morning detail slot bookings of {name_of_doc}... \n\
                              Kindly provide the Time in "hh:mm" format \
                              Example: 10:30 \n\
                              '
                         # call morning detail api
                    else:
                         return f'Here are the evening detail slot bookings of {name_of_doc}... \n\
                              Kindly provide the Time in "hh:mm" format \
                              Example: 12:35 \n\
                              '
                         # call evening detail api
               else:
                    return 'Please select a Doctor first by typing the doctor id'
     
          elif re.match(r'\d{2}:\d{2}',raw_msg):  
               #CHECK POINT  if it matches in morning or evening batch api
               if DOCTORS_ID is not None :
                    if date_set_by_user is not None:
                         global time_period_of_appointment 
                         time_period_of_appointment = ''
                         time_period_of_appointment = raw_msg
                         return f'I will book the appointment for {name_of_doc} at {time_period_of_appointment}, \
                         Kindly provide us confirmation by replying confirm it \
                         Are you Sure about it ?\n'
                    else: return 'Please select a date first by typing the date in dd/mm/yy format:'
               else:
                    return 'Please select a Doctor first by typing the doctor id'
     
          elif raw_msg in ('confirm','confirm it','confirm it please','confirm appointment'
                         'confirm it too','confirm them','confirm the appointment',):
               if DOCTORS_ID is not None:
                    global confirmation_of_user
                    confirmation_of_user = True
                    if time_period_of_appointment is not None:
                         return f'Sure, Booked the appointment for {name_of_doc} at {time_period_of_appointment}\n\
                              How do You wanna Choose your payment Mechanism - COD or UPI  ... '
                    else: return 'Please select a time slot first by typing the time in hh:mm format'
               return BASE_COMMAND

          elif raw_msg in ('no','n','nahh','nope','no thanks',
                         'not now''na','nah','cancel','cancel the appointment',
                         'exit','leave','stop','stop the appointment',
                         'cancel the appointment as well',): 
               if DOCTORS_ID is not None:
                    DOCTORS_ID = None
                    return f'Ok, Booking has been Cancelled ,You can contact me again by saying hi\
                         or choosing a doctor by typing the doctor id from the list\n\
                         Thanks for choosing us '
               return BASE_COMMAND
          
          elif raw_msg in ('cod','cash on delivery','cod payment','cash on delivery payment',
                         'cod payment','cash on delivery payment','upi','google pay'):

               if DOCTORS_ID is not None:
                    if confirmation_of_user is not None:
                         return f'Selected the payment mechanism as {raw_msg}\n\
                              Kindly provide us with the details \n'
                    else:
                         return 'Sorry, You have not confirmed the appointment yet'

               return BASE_COMMAND
     
          elif raw_msg in ('change','need to change','do changes','change the appointment',
                         'changes','do a change','do change'):
               return f'Sure you can do That , the respective Doctor name is { name_of_doc if name_of_doc else "not selected yet " }\
                    Just type the doctor id again if You wanna Change the Doctor  \
                    Type the date in "dd/mm/yy"  format : to change the date for the appointment   \
                    Type the Slot timings as "morning" or "evening" if You wanna Change the Slot timings \n\
                    '
          
          elif raw_msg in ('show me docs','list','doctors','ids','doctor',
                         'shoe me doctors','show list','show me list of doctors',
                         'list of doctors','ids of doctor','id of doctor','all',
                         'show me all ids','show me doctors','all doctors',
                         'all doctors list','i need a doctor','need a doctor','show me list',
                         'show list of doctors','show me list of doctors','show me all doctors',):
               return f"Here's the list of doctors we have \n{names_id_of_doctors}\n\
                    Please select the Doctor by typing the doctor id "
          
          elif raw_msg in ('show tablets','tablets','presciption','number of tablets','no of tablets',
                         'tabs','show me tablets'):
               if DOCTORS_ID is not None:
                    return f'Here we have  the tablet {tablet_name}\n\
                         Kindly specify the number of tablets you require ? Example: 2 days, 7 days, 30 days '
               return BASE_COMMAND

          elif raw_msg  in   [str(i)+' days' for i in range(1,61)] or raw_msg in [str(i)+' day' for i in range(1,61)] or raw_msg in [str(i)+'days' for i in range(1,61)] :
               if DOCTORS_ID is not None :
                    global days_tablets_required 
                    days_tablets_required = raw_msg
                    return f' {NO_OF_TABLETS[0]} {tablet_name} tablets will be generated,Kindly confirm by saying Order tablets\n\
                         Shall i proceed with that ?'
               return BASE_COMMAND
          
          elif raw_msg in ('order tablets','order','order the tablets','order the tablets now',
                         'order it','order the tablets','order the tablets now','order them',
                         'orderr','book tablets','book the tablets','book the tablets now','order that'):
               if DOCTORS_ID is not None and tablet_name is not None and days_tablets_required is not None:
                    return f'Sure, I will order the {NO_OF_TABLETS[0]} tablets for you for {days_tablets_required} Would like to go for Walk-in or Online ?'
               return 'Kindly select the tablet name and Tablets you want to order'
          
          elif raw_msg in ('online','online pay','debit card','credit card','pay online',
                         'pay online now',):
               if DOCTORS_ID is not None:
                    if days_tablets_required is not None and tablet_name is not None:
                         return f' Here are some of Our Pharmacy ids available\n : {PHARMACY_NAMES_LIST}:\
                              Kindly specify the Pharmacy Name By: typing their name and i will order it from there'
                    return f'First Kindly say for how many days I should book your tablets for ? \
                         Example : 2 days, 7 days, 30 days '
               return BASE_COMMAND
          
          elif raw_msg in PHARMACY_NAMES:
               if DOCTORS_ID is not None:
                    if days_tablets_required is not None:
                         for each_row in Messages_tobe_delivered:
                                   try:
                                        PHARMACY_NAME = each_row['Prescriptions'][0]['PHARMACY_name'].lower()
                                        if raw_msg == PHARMACY_NAME :
                                             global CONTACT_NUMBER_OF_PHARMACY, MESSAGE_TO_PHARMACY
                                             PRESCRIPTIONS_TOTAL_TABLETS = each_row['Prescriptions'][1]['no_of_tablets']
                                             PRESCRIPTIONS_TOTAL_DAYS = each_row['Prescriptions'][2]['no_of_days']
                                             PRESCRIPTIONS_TABLET_NAME = each_row['Prescriptions'][2]['tablet_name']
                                             CONTACT_NUMBER = each_row['Mobile_number'] if not None else 0
                                             MESSAGE = f"Dear {PHARMACY_NAME}\
                                             The Tablet name is {PRESCRIPTIONS_TABLET_NAME}\
                                             which The user needs to take total of {PRESCRIPTIONS_TOTAL_TABLETS} tablets\
                                             for {days_tablets_required} consecutive days.\
                                             Please do not forget the days of the tablets. Kindly book them\
                                             Thank you for using our service."
                                             print(MESSAGE)
                                             print()
                                             CONTACT_NUMBER_OF_PHARMACY = CONTACT_NUMBER
                                             MESSAGE_TO_PHARMACY = MESSAGE
                                             # Send_message(sender_id = PHARMACY_NAME, clients_numbers = CONTACT_NUMBER, message_for_clients = MESSAGE)  
                                             # pywhatkit.sendwhatmsg_instantly(CONTACT_NUMBER,MESSAGE,10)
                                             return f'Dear User I Have successfully placed Your order at {PHARMACY_NAME} Pharmacy \
                                                  Thank you for using our service'   
                                   except KeyError as e:
                                        print(e)
                    return f'First Kindly provide us information for how many days I should book your tablets for ? \
                         Example : 2 days, 7 days, 30 days '
               return BASE_COMMAND


          elif raw_msg in ('walkin','walk-in','walk-in pay','walkin pay','walk-in pay now',):
               if DOCTORS_ID is not None:
                    return('Sure,Thanks for being with Us. Have a nice day')
          else:
               print('\n\n',raw_msg,'\n\n')
               return f'Sorry, I did not understand'


def  close_message_box():
     """  Close the message box"""
     navigate_to_image(r'C:\Users\Tushar\Desktop\cloud_next\images\cross_whatsapp.png',1)

