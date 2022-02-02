from gtts import gTTS
from os import getenv
from server import whatsapp_automation

import datetime
import json
import mysql.connector
import requests


recorded_messages = {}
SQLPROCEDURE = 'user_dates'


def Send_message(**kwargs):
     """ Bulk messages sent to clients on their phone numbers
       kwargs == sender_id, clients_numbers, message_for_clients """
     third_party_api_for_messages = "https://www.fast2sms.com/dev/bulk" 
     data_sent_to_users = {                        
     'sender_id': kwargs['sender_id'],             
     'message': kwargs['message_for_clients'],
     'language': 'english',
     'route': 'p',
     'numbers':kwargs['clients_numbers']    
     }
     headers = {
     'authorization': 'rRox0j5QTXtSiIO6GlhPANUbZumVfBW38zDC1E2s9qLe7Kva4pIEtbLQFxBraew28ZlpUcmSKVq9GgDi',
     'Content-Type': "application/x-www-form-urlencoded",
     'Cache-Control': "no-cache"
     }
     response_given_to_client = requests.request("POST",
                              third_party_api_for_messages,
                              data = data_sent_to_users,
                              headers = headers)
     returned_msg_from_client = json.loads(response_given_to_client.text)   
     return(returned_msg_from_client['message']) if returned_msg_from_client.get('return') else print('Error in sending message')

class Dbconnection():
     """ DB Connection """ 
     def __init__(self):
          """ Initialize the database """
          self.host = getenv('DB_HOST'),
          self.user = getenv('DB_USER'),
          self.passwd = getenv('DB_PASS'),
          self.database = getenv('DB_NAME')
          self.mydb = mysql.connector.connect(  
               host = self.host[0],  
               user = self.user[0],    
               passwd = self.passwd[0],    
               database = self.database )  

          self.cursor = self.mydb.cursor()
          self.cursor.execute("Show tables;")
          mytables = self.cursor.fetchall()  
          if mytables:
               self.list_of_tables = [ (each_table[0].decode("utf-8")  ) for each_table in mytables  if mytables  ]
          else:
               print("No tables found in the database")
          
     def check_Dbconnection(self):
          """ checks if the connection is working  """    
          try:
               self.mydb.is_connected()
               print(self.mydb.is_connected())
               db_info = self.mydb.get_server_info()
               print(db_info)
               return(f'Connected to MySQL Server version {db_info = }\n')    
          except Exception:
               exit('"A error occured while creating connection connection to the DB!"')

     def appointments_for_today(self):
          """ Get list of all appointment for today 
               from appointments & prescription table
               When func of send_message is called
               it will send real time message to the patient """

          self.check_Dbconnection()
          try:
               self.cursor.callproc(SQLPROCEDURE)
          except Exception:
               return f'Procedure named in constant {SQLPROCEDURE = } does not exist'

          for result in self.cursor.stored_results() :
               all_data_in_procedure = result.fetchall()
               column_names = result.column_names
               if all_data_in_procedure:
                    if 'appointments' in column_names:
                         for each_rows_data in all_data_in_procedure:    
                              slot_time = (datetime.datetime.strptime((json.loads(each_rows_data[2]).get('slot_time')), '%H:%M').time() )                  
                              notification_hour = (datetime.datetime.strptime((json.loads(each_rows_data[2]).get('slot_time')), '%H:%M').time().hour - 2 )
                              MESSAGES = 'You have an appointment today at ' + str(slot_time)
                              CONTACT_NUMBERS = each_rows_data[4]
                              if datetime.datetime.now().hour >= int(notification_hour)  and datetime.datetime.now().hour < int(slot_time.hour):
                                   Send_message(sender_id = each_rows_data[0], clients_numbers = CONTACT_NUMBERS, message_for_clients = MESSAGES)                
                                   recorded_messages[CONTACT_NUMBERS] = MESSAGES
                                   whatsapp_automation(CONTACT_NUMBERS,MESSAGES)
                                   print(f"Message sent to {CONTACT_NUMBERS}")
                              else:
                                   print(f'No need to send message as time has been extended for {each_rows_data[0]} user id \n')
                    else:
                         return ('No slot time column present')
               else:
                    return '0 rows returned'
       
          # # self.mydb.commit()
     
d = Dbconnection()
# d.appointments_for_today()
d.check_Dbconnection()
# print(d.list_of_tables)
# print(recorded_messages)
d.mydb.close()



               
























