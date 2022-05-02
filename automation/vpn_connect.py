from pickletools import pyunicode
import time 
import pyautogui 
import pyautogui as pt
from  credentials import all_credentials

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

class Connect():
     def __init__(self,name):
          self.username = name
     
     def confirmation(self):
          ''' confirmation of the  global protect vpn connection '''
          pyautogui.press('win')
          time.sleep(1)
          pyautogui.write('globalProtect')
          time.sleep(1)
          pyautogui.press('enter')
          time.sleep(1)
          if (pyautogui.locateOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\pics\confirmation_fortclient_connected.png')) is not None:
               print(' Connection successful ')
               return True
          time.sleep(5)


     def run(self):
          ''' Open windows and connect to globalProtect VPN 
          thus calling my number in the end  '''
          pyautogui.press('win')
          time.sleep(1)
          pyautogui.write('globalProtect')
          time.sleep(1)
          pyautogui.press('enter')
          time.sleep(1)
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\connect_blue_white.png'))
          time.sleep(10)
          
          print('\nClicking on the Requested Id\n')
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\signed_in_white_black.png'))
          print()
          time.sleep(4)
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\jjj_id_2_white.png'))
          time.sleep(2)

          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\type_password.png'))
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\type_password_2.png'))
          # print(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\type_password.png'))
          # print(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\type_password_2.png'))
          pyautogui.write(all_credentials['globalProtect']['password']),print("Written the password 😁") if pyautogui.position() == (871, 461)else  print('I"m not writing password in the air ')
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\signin_blue.png'))
          time.sleep(10)
          
          pyautogui.click()
          time.sleep(25)
          pyautogui.click(pyautogui.locateCenterOnScreen(r'C:\Users\tushar.m\Desktop\thinkpalm\images\check_box_black_white.png'))
          time.sleep(2)
          pyautogui.press('enter')
          time.sleep(5)
          
          
     def main(self):
          ''' running the main program 
          for this file only * '''
          self.run()
          time.sleep(5)
          self.confirmation()

if __name__ == '__main__':
     tushar = Connect(all_credentials['outlook']['username'])
     tushar.main()
