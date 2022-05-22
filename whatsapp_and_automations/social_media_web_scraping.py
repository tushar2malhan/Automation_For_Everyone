import time
import sys 
import pyautogui
from selenium import webdriver
import credentials

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# REMOVE POP UP NOTIFICATIONS 
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

u_input = input("Which Social Media account  would you require information for ?: \n\n\
   \t Instagram \t Facebook \t Twitter \t Linkedin \n").lower().strip()

linkedin_email = credentials.all_credentials['linked_email']
linkedin_password = credentials.all_credentials.get('linked_password')
fb_email = credentials.all_credentials['fb_email']
fb_password = credentials.all_credentials['fb_password']
insta_email = credentials.all_credentials['insta_email']
insta_password = credentials.all_credentials['insta_password']

path_to_chromedriver = r"C:\Users\Tushar\Downloads\chromedriver.exe"

def user_information(username):

    """ Display user information from
    their social media accounts """
   
    driver = webdriver.Chrome( chrome_options=option,executable_path=f"{path_to_chromedriver}"  )
    
    def block_page():
            ' WANNA Block any page ? - For only facebook Pages '
            
            #               3 button Option
            ''' Since element is not interactable, we use driver.execute_script() to click the button '''
            print()
            print(1)
            try:
                print('Clicked 3 button Options')
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[3]/div/div/div/div[2]/div/div/div[3]/div/div/div[1]"))))
            except Exception as e:
                print(e)
                ...
                print('1 not respond')
            time.sleep(2)

          
            #                  Report Page     :->     As page will be not be clickable sometimes , we start with 1 step from except Block !
            print(2)
            try:
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[6]/div[2]/div/div/span"))))
                print('Report Page')
            except Exception as e:
                print('try to click  2 button again with 1 button ')
                WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[3]/div/div/div/div[2]/div/div/div[3]/div/div/div[1]'))).click()
                WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[6]/div[2]/div/div/span'))).click()
                print('\n\n ',e)
            time.sleep(2)
          
          
            #                  Fake Page
            print(3)
            try:
                # driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[4]/div/div/div/div[1]/div/div[1]/div/div/div/div/span').click()
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[4]/div/div/div/div[1]/div/div[1]/div/div/div/div/span"))))
                print('Fake Page')
            except:driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[6]/div/div/div/div[1]/div').click()
            time.sleep(2)
           
           
            #               Something Suspecious          
            try:
                print('Called Suspecious Button ')
                # driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div/div/div/span').click()
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div/div/div/span"))))
            except: driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[2]/div/div/div[4]/div/div/div/div[1]/div/div[1]/div/div/div/div/span').click()
            time.sleep(2)
           
           
            #               Submit
            print(4)
            try:
                print('Submitted')
                # driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div[1]/div/span/span').click()
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div[1]/div/span/span"))))
            except:driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div[1]/div/span').click()
            time.sleep(2)
            
            
            #               Done
            print(5)
            try:
                print('DONE ')
                # driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div[1]/div/span/span').click()
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div/div[1]/div/span/span"))))
            except: driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div[2]/div/div/div/div').click()
            time.sleep(2)
       

    try:
        if u_input.startswith('i'):
            print('Instagram\n')
            url = f"https://www.instagram.com/accounts/login/?next=%2F&source=logged_out_half_sheet"
            driver.get(url)
            time.sleep(5)
            try:
                driver.find_element(By.NAME,'username').send_keys(insta_email)
                driver.find_element(By.NAME,'password').send_keys(insta_password+Keys.ENTER)
                try:driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button/div').click()
                except: ...
                print('Logged In Successfully to Instagram')
            except: print("Cant login to instagram ")
            time.sleep(10)
            name = driver.title

            url = f"https://www.instagram.com/{username}/"
            driver.get(url)
            time.sleep(3)
            try:
                name = driver.find_element(By.CLASS_NAME,'XBGH5').text
            except:
                # name = driver.find_element(By.CSS_SELECTOR ,'._7UhW9.fKFbl.yUEEX.KV-D4.fDxYl').text
                # name = driver.find_element(By.CLASS_NAME,'_2s25').text
                print('No name \n\n')
 
            try:
                image = driver.find_element(By.XPATH,'//img[@class="_6q-tv"]')
            except:
                image = driver.find_element(By.XPATH,'//img[@class="be6sR"]')
        
            profile_pic = image.get_attribute('src')

            try:
                total_posts = driver.find_element(By.CLASS_NAME, "g47SY").text
            except:
                print('Couldnt fetch the total posts of the User from Instagram')
            try:
                brief = driver.find_element(By.CLASS_NAME, "k9GMp ").text
            except:
                brief = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').text
            # data[f'total_posts_of_{username}'] = total_posts
            # data[f'followers_of_{username}'] = followers
            
            # print(f'Profile pic URL is \t',profile_pic,end='\n\n')
            print(f'Total posts are \t',total_posts,end='\n\n')
           
        
        elif u_input.startswith('f'):
            print('Facebook\n')
        
            url = f"https://www.facebook.com/"
            driver.get(url)
            
            """ here we try to find element by class name by looking at page source and we get attribute
                 we make some time with sleep so that it doesn't break the code'
                 xlink:href  is the attribute of the image we want from FB 
                 IF U DONT FIND UR USERNAME HERE , TRY USING name.sername
                 name = driver.title """
           
            """ LOGGED IN FIRST """
            # login button
            time.sleep(5)
            try:driver.find_element(By.XPATH,('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/a/div/div[1]')).click()
            except: ...
            driver.find_element(By.ID,'email').send_keys(fb_email)
            driver.find_element(By.ID,'pass').send_keys(fb_password+Keys.ENTER)
            
            try:driver.find_element(By.CLASS_NAME,'_6ltg').click()
            except:print('Logged in \n')

            
            
            ''' SEATCH BOX FOR USERNAMES '''
            # time.sleep(10)
            # search_box = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/label/input')
            # search_box.click()
            # search_box.send_keys(username)
            # search_box.send_keys(Keys.RETURN)
            

            # NOW LOGEGD IN WITH USERNAME SUCCESSFULLY
            url = f"https://www.facebook.com/{username}"
            driver.get(url)

            ''' Blocking the page 
            driver.minimize_window()
            def recursive_attack_on_a_page():
                try:
                    while 1:
                        try:block_page() if u_input.startswith('f') else 'break'
                        except:block_page() 
                except:
                    while 1:
                        try:block_page() if u_input.startswith('f') else 'break'
                        except:block_page() 
            # try:recursive_attack_on_a_page()
            # except:recursive_attack_on_a_page()
            '''
   

            
            name = driver.title         # .split('Facebook')[0].split('|')[0]
            time.sleep(10)

            profile_pic = [i.get_attribute('xlink:href') for i in driver.find_elements(By.TAG_NAME,"image")][1:3]
            try:followers = driver.find_element(By.CSS_SELECTOR,'.'+ '.'.join('oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 m9osqain lrazzd5p'.split(' '))  ).text
            except: followers = 'Cant Access Followers'
            # brief = driver.find_element(By.CSS_SELECTOR,'.'+ '.'.join('dati1w0a tu1s4ah4 f7vcsfb0 discj3wi'.split(' '))) .text


          
        elif u_input.startswith('t'):
            """
            SO u wanna get element having multiple classes ? 
                - Followers classname refers to the element having multiple classes.which refers
            to a single element, hence we used CSS selector or can use xpath
            where we need to join classes with . DOT .  
            but not for XPATH - was not working properly
            """
            print('Twitter\n')
            url = f"https://www.twitter.com/{username}/"
            driver.get(url)
            time.sleep(7)
            followers_class_name = '.'+ '.'.join('css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'.split(' '))    
            total_words_list = [total_followers.text for total_followers in driver.find_elements(By.CSS_SELECTOR,followers_class_name)]
            time.sleep(5)
            followers =' '.join([ total_words_list[i-1] for i,word in enumerate(total_words_list) if word == 'Followers'])
            name = driver.find_element(By.CSS_SELECTOR,'.'+ '.'.join('css-1dbjc4n r-6gpygo r-14gqq1x'.split(' '))).text
            if name is  None or name == '':
                print('\nCan fetch the name\n')
            time.sleep(5)
            profile_pic = driver.find_element(By.CLASS_NAME,'css-9pa8cd').get_attribute('src')
            brief = [driver.find_element(By.CLASS_NAME,'css-1dbjc4n').text]

        elif u_input.startswith('l'):
            """ here we have to signin first and
            then click on url to search the name in the linkedin
            Finding only indian users  """
            print('Linkedin\n')
            url = f"https://www.linkedin.com/login"   
            driver.get(url)
            time.sleep(8)
            
            driver.find_element(By.ID,'username').send_keys(linkedin_email)
            driver.find_element(By.ID,'password').send_keys(linkedin_password+Keys.ENTER)
     
            # pyautogui.click(pyautogui.locateOnScreen(r'C:\Users\Tushar\Desktop\cloud_next\images\linkedin_in_url_white.png',confidence = .8))
            # pyautogui.write(url)
            # pyautogui.press('enter')
            url = f'https://www.linkedin.com/in/{username}/?_l=en_US' 
            driver.get(url)
            time.sleep(10)
            followers = driver.find_element(By.CLASS_NAME,'t-bold').text
            name = driver.find_element(By.CLASS_NAME,'pv-text-details__left-panel').text
            profile_pic = driver.find_element(By.ID,'ember33').get_attribute('src')
            if profile_pic is None:
                profile_pic = driver.find_element(By.ID,'ember38').get_attribute('src')
            ul = driver.find_elements(By.CLASS_NAME,'pvs-list__outer-container')
            brief = []
            
            for each_li in ul:
                text =  each_li.find_element(By.TAG_NAME,'li').text
                # print (text)
                brief.append(text)

        
        else:sys.exit("Invalid input")

        try:print(f'\n\nUsername is \t\t',name,end='\n\n')      
        except: print('❌ name  ')
        try:print(f'Profile pic URL is \t',profile_pic,end='\n\n')
        except: print(' ❌ Profile Pic ')
        try: print(f'Total Followers are \t\t\n',followers,end='\n\n') if followers is not None  else print('No Followers')
        except : print(' ❌ Followers ')
        try:print(f'In Brief \t\t\n',brief,end='\n\n')  
        except: print("❌ Brief here ")
      
        driver.close()
        return name
    
    except Exception as e :
        print(f'{username}\t\n Check The Username Again\n ')
        print('\n\t',e)
        return(f'\n\n Issue with User named -> {username} for getting the information for {u_input}')


names = [ 
        # 'samridhi',
        # 'jimmymalhanf'
        # 'thejohnabram
        # 'rahul.vij.127',
        # 'ok',
        # 'tusharmalhan',
        # 'iamsrk',
        'cristiano',
        # 'ktrtrs',
        # 'bajaj',
        # 'virat.kohli',
        # 'ronaldo',
        # 'rahul_vij','egg', 'Tushar79958956',

        ]
[user_information(name) for name in names]




    




