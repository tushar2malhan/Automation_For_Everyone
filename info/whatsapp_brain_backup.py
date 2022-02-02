from numpy import e
from pynput.mouse import Button, Controller
from time import sleep

import json
import pyautogui as pt  
import pyperclip as pc



pt.FAILSAFE = True
mouse  = Controller()


with open('MOCK_DATA.json', encoding="utf8") as f:
     data = json.load(f)


names_id_of_doctors = ''.join(['   '.join(  str(each_data.get('doctorid'))+". "+each_data.get("name_of_doc").lower() for each_data in data)])

def navigate_to_image(image, clicks, off_x = 0, off_y = 0):
     """   image is the image to be searched for, 
           clicks is the number of times to click, 
           off_x and off_y are the offset from the center of the image 
     """
     position = pt.locateOnScreen(image, confidence = .8)
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
     """ Revert to the replies of the client """

     raw_msg = msg.lower().strip()
     if raw_msg in('hello', 'hi', 'hey','hii','heyy','hey there','heyy there'):
          return 'Hi How can I help you?'
     elif raw_msg in ('yes','y','ok','done','k','im interested',):
          return 'Thank you, We will get back to you soon'
     elif raw_msg in ('no','n','nahh','nope','no thanks','not now'):
          return 'Okay, no problem'
     elif raw_msg in ('what','?','how','when'):
          return 'Respected Client , dont worry, i will give you all the details'
     elif raw_msg in ('bye','goodbye','see you','see you later','see you later'):
          return 'Bye, Have a good day'
     elif raw_msg in ('thanks','thank you','thank','thank you very much'):
          return 'You are welcome, Have a good day'
    
     elif raw_msg in ('doctors','list of doctors','show docs','show doctors','show list of doctors','show doctors list','doctors list','show'):
          try:
               each_doctors_detail =  [  (each_row['doctorid'], each_row['name_of_doc'], each_row['specilization'],each_row['location']) for each_row in data ]
          except:
               print('Error in fetching the JSON data')
          val = []
          for specific_details in each_doctors_detail:
               val.append( f'\
                         \
                         \
                         Doctors ID - { specific_details[0] }  \
                                                  \
                                                  \
                         Doctors Name - { specific_details[1] }  \
                                                  \
                                                  \
                         Specialized in - {specific_details[2]}  \
                                                  \
                                                  \
                                                  \
                         Located - {specific_details[3]}  \
                                                  \
                                                  \
                                                  \
                                                  \
                                                       '  )
          return ' '.join(val) +" \
               \
               \n\
               Kindly select the Doctor's ID from the list to know more about the Availablity and Time slots"


     elif raw_msg in [str(i) for i in range(1,11)] :
          try:
               name_specialization_location = [ (each_row['name_of_doc'],each_row['specilization'],each_row['location']) for each_row in data if each_row['doctorid'] ==  int(raw_msg)]
               availability = ' '.join([ 'Yes ,The Doctor would be availabile' for each_row in data if each_row['doctorid'] ==  int(raw_msg) and each_row['availability']   ])
          except:
               print('Error in fetching the JSON data')
          for specific_detail_in_each_row in name_specialization_location:
               return f' Doctors Name - { specific_detail_in_each_row[0] }  \
                    \
                    \
                    \
               Specialized in - {specific_detail_in_each_row[1]}  \
                    \
                    \
                    \
               Located - {specific_detail_in_each_row[2]}  \
                    \
                    \
                    \
                    \
                    \
               and {availability if availability else f"Sorry the Doctor is not available, Kindly choose from them !                           "+names_id_of_doctors}'
               

     elif raw_msg in ('book appointment','appointment','book an appointment','book an appointment for','book an appointment for doctor','book an appointment for doctor'):
          return 'what time do you want to book it for ?'
     elif raw_msg in ('doctor id','ids','doctor','id','id of','id of doctor','id of doctor'):
          return f'{names_id_of_doctors}'
     else:
          return f'Sorry, I did not understand\
               \
               \
               \
               \
               \
               Kindly type \
               \
               \
               . The Doctor ID from the list to know more about the Availablity and Time slots for the respective doctor \
               \
               \
               \
               \
               \
               . Doctors list  to get all information about doctors'


def  close_message_box():
     """  Close the message box"""
     navigate_to_image(r'C:\Users\Tushar\Desktop\cloud_next\images\cross_whatsapp.png',1)


     
     
 


 