""" WHATSAPP messenger as well as server BOT
A continous server which will work as a bot for whatsapp"""
import time
import pyautogui
import pywhatkit
import brain_whatsapp_response as wa
# from appointments import Send_message

MY_DIR = r"C:\Users\Tushar\Desktop\cloud_next\images\\"

def whatsapp_automation(number, message_type, message, image_file=None):
    """ Implemenation of whatsapp automation
    for bulk unknown numbers with an image or text (OPTIONAL)  """
    if len(number) < 10 or len(number) > 10:
        return f'Your {number} is an Invalid number'
    if not number.startswith('+91'):
        number = '+91'+ number
    message_type = message_type.lower()
    if message_type in ('text','txt','message','msg'):
        pywhatkit.sendwhatmsg_instantly(number, message,10)
    else:
        if image_file is not None:
            try:
                pywhatkit.sendwhats_image( number, image_file, message, 10)
            except FileNotFoundError:
                print('Error in sending image \nCheck the image file format')
        else:
            return 'Please provide an image file'
    time.sleep(10)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(4)
    try:
        pyautogui.click(pyautogui.locateCenterOnScreen(MY_DIR+"send.png"))
    except FileNotFoundError:
        print('Couldnt click the send button, doing it again')
        time.sleep(2)
        pyautogui.click(pyautogui.locateCenterOnScreen(MY_DIR+"send.png"))
    return message_type

if __name__ == "__main__":
    print(whatsapp_automation('7814891872','image',
    'Hey cloudnext client 👋 Thank you for being our valued customer. \
     We will be happy to notify you. For your queries  and\
     we Hope  met your expectations.',r'images\image.jpeg'))
    ...

    time.sleep(3)
    LAST_MESSAGE = ''
    while True:
        wa.navigate_to_image(MY_DIR+'new_message_1.png', 1, off_x = -100)
        wa.close_message_box()
        wa.close_message_box()
        message = wa.copy_latest_msg()
        if message != LAST_MESSAGE:
            wa.send_message(wa.process_message(message))
            
           
            # whatsapp_automation(wa.CONTACT_NUMBER_OF_PHARMACY,'txt', wa.MESSAGE_TO_PHARMACY)       #       Whatsapp message sent to pharamacy 
            
           
            # Send_message(sender_id = wa.CONTACT_NUMBER_OF_PHARMACY,  #       Phone text message sent to pharamacy 
            # clients_numbers = wa.CONTACT_NUMBER_OF_PHARMACY, 
            # message_for_clients = wa.MESSAGE_TO_PHARMACY)                
        
        else:
            print('No new message...\n')
        time.sleep(10)
                                             