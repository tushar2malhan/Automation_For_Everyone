from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import datetime
import time
from time import sleep
from selenium import webdriver

from job_apply_automation import initialize_information

driver = webdriver.Chrome()  # You may need to provide the path to your Chrome WebDriver

# Import the variables from the initiating_variables module
import initiating_variables
question_mappings = initiating_variables.question_mappings
ctc_expectations = initiating_variables.ctc_expectations
location_to_city_type_gid = initiating_variables.location_to_city_type_gid
experience = initiating_variables.experience
job_titles = initiating_variables.job_titles
location = initiating_variables.location
job_age = initiating_variables.job_age
exclude_keywords = initiating_variables.exclude_keywords
my_info = initiating_variables.my_info

driver = initiating_variables.driver
page_404_error = initiating_variables.page_404_error

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

contains_captcha_text = initiating_variables.contains_captcha_text
successfull_response = initiating_variables.successfull_response
get_element_xpath = initiating_variables.get_element_xpath
click_apply_button = initiating_variables.click_apply_button
is_career_section_unavailable = initiating_variables.is_career_section_unavailable
accept_cookies = initiating_variables.accept_cookies
wait = initiating_variables.wait
login_portal = initiating_variables.login_portal
click_element_or_js = initiating_variables.click_element_or_js
chatbot_questionnaire = initiating_variables.chatbot_questionnaire
resume_file_path = initiating_variables.resume_file_path
from initiate_functions import filling_questionnaire, initialize_information


def get_web():
    # url = "https://tresvistacareers.turbohire.co/surveys?token=SH3RVxWEbmWHSWgVU1ELI8fN8zzngUxfZ0Zmz5pVKVIDOsWVyUJn2d5XyNxRN8SnQuESBEcCgQA4Uw9_B67gMcnzs7ja1Qxmgtoclyp_4M%2Fj1zp55LRP_jhCNveetDQCW9zfGZHBippuDEVgDAZX1TYoLeNN1vp_20mZYPtwmhs=&company=nGouE9BaVHwVrgRUlwh3cqVB7jhQgMBxiNhOiYAT2%2Fc0JVdW1xICQmmiFoP4uAlZ&guest=tusharmalhan@gmail.com"
    url ='https://career44.sapsf.com/career?company=indegenepr&site=&lang=en_GB&requestParams=7I1ZJPtk0NY%2fQLgxiKv87QVj8Kh42m2S32oTQRTGj2li0z8opSDeCLLXJZhkaWl64Z9Ka6CCIHpT%0aZJ3OniTTTGamZ862CaE%2biY%2bgDyE%2bgV76AuKF7%2bDZWjQrDuywe%2bb7vjPz2%2fnwExqRYONUnatWwca2%0anqk4eq5CY%2fnbp8933n5ZgtoBrFqv8gOl2VMfVnhEGEfe5tPw8BGU4%2b5FU%2bb78qwzrCuLxPuEijEv%0aCDaPj67SrXLD1ksm44Z7H7%2b%2b%2fv7j3vywBjANYrvBUGcqkKGprUHH%2fbw4g3ew9HuteepPYucCTxg2%0atCJEyqSSEZ5lpiKsp520y3DLxL5jJKfsq4i0qGgMlI3SZ%2bU6x8XF1dtlrArBGq3YeMewSZNxVkhI%0aFggHSOg0Ljrez5NB4XQpVnbf%2b7HBmPSO32wlAWngaaLEUKmr%2fFz4mCgc%2ftbnifaToNws6SVHxo0x%0a77tkK9Ej1PKe9NqX4tS%2bcEwzngUUmQ9sSk0unHEaDJVB7Z32brrd6W53u532pQCJhiv7BYa16LVR%0a9rEcc%2fY%2fNGsC4YUJaI2rWG8%2blR6aBa%2f2RGivCGXVP7Uq%2fHd3HqTtNGVYvj7TH0FNBMblOESHgf75%0aqJcXpLIfdNnhk%2bkvGwnKsw%3d%3d&career_ns=job%5fapplication&career_job_req_id=4243&jobPipeline=Direct&clientId=jobs2web&_s.crb=PExFn1biqsC93zGV3muvwOYGX85ibovXNVNu11QZUuM%3d'
    try:
        # Open the URL
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        import sys
        sys.path.append('C:\\Users\\gyala\\Desktop\\Automation_For_Everyone')

        
        # recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

        # solver.click_recaptcha_v2(iframe=recaptcha_iframe)


    finally:
        initialize_information()
        # Close the browser and quit the driver
        # driver.quit()



# Call the function to initialize the information
get_web()



elements = driver.find_elements(By.PARTIAL_LINK_TEXT, 'accept the data')

if elements:
    first_element = elements[0]
    tag_name = first_element.tag_name
    if tag_name.lower() == 'a':
        first_element.click()

    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Find the Accept button using its label or text
accept_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[text()='Accept']"))
)

try:
    accept_button.click()
except:
    driver.execute_script("arguments[0].click();", accept_button)



### REPCAPTCHA SOLVER
    
#   1  # https://github.com/ohyicong/recaptcha_v2_solver


# 2.
# from selenium_recaptcha_solver import RecaptchaSolver
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


# test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

# options = Options()

# options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
# options.add_argument("--window-size=1920,1080")

# options.add_argument(f'--user-agent={test_ua}')

# options.add_argument('--no-sandbox')
# options.add_argument("--disable-extensions")

# test_driver = webdriver.Chrome(options=options)

# solver = RecaptchaSolver(driver=test_driver)

# test_driver.get('https://www.google.com/recaptcha/api2/demo')

# recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

# solver.click_recaptcha_v2(iframe=recaptcha_iframe)



# 3
    
# import cv2
# import pytesseract

# # Load the image
# image = cv2.imread("captcha.png")

# # Preprocess the image
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# # Recognize the text in the image
# text = pytesseract.image_to_string(thresh)

# # Print the text
# print(text)