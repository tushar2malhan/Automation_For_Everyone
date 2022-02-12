""" Send voice messages to the Clients """
import json
import sys
from datetime import date,datetime
import time
import pyautogui
import pywhatkit
import pyttsx3
from brain_whatsapp_response import navigate_to_image
  

JSON_FILE = 'MOCK_DATA_3.json'
dt = datetime.strptime("17/1/2022", '%d/%m/%Y').date()
today = date.today()
current_hour = datetime.now().hour

def check_json_file(JSON_FILE):
    """ Check if the json file exists and return the data """
    try:
        with open(JSON_FILE, encoding="utf8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Not a valid JSON file")
        sys.exit()
    return data


def speak(name,tablet_name):
    """send and save voice message for clients"""
    text = f'Dear {name} , As per your reminder\
                you have to take {tablet_name} tablet now.\
                Thanks for using our service'
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)
    # engine.say(text)
    engine.save_to_file(text, f'recorded_message/{name}.mp3')
    engine.runAndWait() 


def inform_morn_weekly(types):
    ''' inform them on either daily or weekly basis 
    depending upon the type of the arg '''
    check_json_file(JSON_FILE)
    today_rows_daily = [each_row for each_row in check_json_file(JSON_FILE) 
    if  datetime.strptime(each_row['Start'], '%d/%m/%Y').date() 
    == today and each_row['Username'] and each_row['contact_no'] 
    not in ['', None] and  each_row['remindme'] and each_row['Days'] == types] 
    for row in today_rows_daily:
        name = row["Username"]
        number = row["contact_no"]
        tablet_name = row['Tabletname']

        morning_time = row['Morning']
        evening_time = row['Evening']
        night_time = row['Night']

        if morning_time and current_hour < 12:
            speak(name,tablet_name)
            send_file_whatsapp(name,number)
            
        if evening_time and current_hour > 12 and current_hour < 18:
            speak(name,tablet_name)
            send_file_whatsapp(name,number)
            
        if night_time and current_hour >= 18:
            speak(name,tablet_name)
            send_file_whatsapp(name,number)

        print(row)


def send_file_whatsapp(name,number):
    """ send the recorded message to the client """
    time.sleep(5)
    pywhatkit.sendwhatmsg_instantly(number, ' ', 10)
    time.sleep(2)
    navigate_to_image(r'images\paperclip.png',1)
    time.sleep(2)
    navigate_to_image(r'images\docs_purple.png',1)
    time.sleep(2)
    recorded_message = fr'C:\Users\Tushar\Desktop\cloud_next\recorded_message\{name}'
    pyautogui.write(recorded_message)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    pyautogui.press('enter')


def main():
    """ main function """
    inform_morn_weekly('daily')
    inform_morn_weekly('weekly')

if __name__ == '__main__':
    main()