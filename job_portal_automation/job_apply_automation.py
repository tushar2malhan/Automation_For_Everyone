'''
        Description:  job Application Automation
        Date:         30/06/2023
        Status:       WIP
        Author:       Tushar Malhan
'''


""" 

    Config.ini  -> stores personal info for each user
    Config.json -> stores classname attributes for the portal 
"""

import os
import csv
import json
import datetime
import re
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import configparser
config = configparser.ConfigParser()
# Read the configuration file
config.read("config.ini")
skills = config.get("other", "skills", fallback="Default Value")
experience = config.get("other", "experience", fallback="3")
job_titles = config.get("other", "job_titles").split(",")
location = config.get("other", "location")
## options are 1, 3, 7, 15, 30 days | will take the max out of it automatically
job_age = max(config.get("other", "jobAge", fallback="").split(','))
## Applications that is not required to be applied for the respective Job Title !
exclude_keywords = config.get("other", "exclude_keywords", fallback="").split(",") 
my_info = dict(config.items("my_info"))
question_mappings = {
    "experience": experience,
    "first name": my_info.get        ("First", my_info.get("first", "")),
    "last name": my_info.get         ("Last", my_info.get("last", "")),
    "number": my_info.get            ("Number", my_info.get("number", "")),
    "phone": my_info.get             ("Number", my_info.get("number", "")),
    "contact": my_info.get           ("Number", my_info.get("number", "")),
    "website": my_info.get           ("Github", my_info.get("github", "")),
    "github": my_info.get            ("Github", my_info.get("github", "")),
    "current city": my_info.get      ("City", my_info.get("city", "")),
    "current location": my_info.get  ("City", my_info.get("city", "")),
    "expected annual": my_info.get   ("ECTC", my_info.get("ectc", "")),
    "expected salary": my_info.get   ("ECTC", my_info.get("ectc", "")),
    "expected ctc": my_info.get      ("ECTC", my_info.get("ectc", "")),
    "salary expectation": my_info.get("ECTC", my_info.get("ectc", "")),
    "join": my_info.get              ("notice_period", my_info.get("Notice Period", "")),
    "languages": my_info.get         ("languages", my_info.get("Languages", "")),
    "languages": my_info.get         ("languages", my_info.get("Languages", "")),
    "job change": my_info.get        ("job_change_reason", my_info.get("Job Change Reason", "")),
    "current ctc": my_info.get       ("CTC", my_info.get("ctc", "")),
    "current annual ctc": my_info.get("CTC", my_info.get("ctc", "")),
    "current ctc": my_info.get       ("CTC", my_info.get("ctc", "")),
    "current annual ctc": my_info.get("CTC", my_info.get("ctc", "")),
    "expected annual": my_info.get   ("ECTC", my_info.get("ectc", "")),
    "expected salary": my_info.get   ("ECTC", my_info.get("ectc", "")),
    "expected ctc": my_info.get      ("ECTC", my_info.get("ectc", "")),
    "salary expectation": my_info.get("ECTC", my_info.get("ectc", "")),
    "notice period": my_info.get     ("notice_period", my_info.get("Notice Period", "")),
    "join": my_info.get              ("notice_period", my_info.get("Notice Period", "")),
    "when can you start": my_info.get("notice_period", my_info.get("Notice Period", "")),
    "when can you start": my_info.get("notice_period", my_info.get("Notice Period", "")),
    "university": my_info.get        ("university", my_info.get("University", "")),
    "school": my_info.get            ("university", my_info.get("School", "")),
    "institute": my_info.get         ("university", my_info.get("Institute", "")),
    "university": my_info.get        ("university", my_info.get("University", "")),
    "school": my_info.get            ("university", my_info.get("School", "")),
    "institute": my_info.get         ("university", my_info.get("Institute", "")),
    "skills": skills
}
ctc_expectations = {
    1: "0to3",
    2: "3to6",
    3: "6to10",
    4: "10to15",
    5: "15to25",
    6: "25to50",
    7: "50to75",
}
location_to_city_type_gid = {
    1: {"mumbai": 134},
    2: {"chennai": 183},
    3: {"usa": 9044},
    4: {"Hyderabad": 17},
    5: {"bangalore": 97},
    6: {"delhi/NCR": 9508},
    7: {"Pune": 139},
    8: {"Kolkata": 232},
    9: {"Mumbai(All Areas)": 9509},
}
applied_jobs = set()  
# Redirect SSL handshake error messages to nul (Windows)
if os.name == 'nt':
    sys.stderr = open(os.devnull, 'w')
# Redirect SSL handshake error messages to /dev/null (Linux/Mac)
if os.name == 'posix':
    sys.stderr = open('/dev/null', 'w')


# Set up Chrome options
# Create a new instance of the Chrome web driver


from selenium.webdriver.chrome.service import Service

service = Service()
options = webdriver.ChromeOptions()
# options.add_argument("--headless")                # Without GUI
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")               # Disable GPU acceleration
options.add_argument("--disable-infobars")          # Disable the "Chrome is being controlled by automated software" infobar
options.add_argument("--disable-geolocation")       # Disable geolocation services
options.add_argument("--disable-dev-shm-usage")     # Disable /dev/shm usage (useful for Docker)
options.add_argument("--no-sandbox")                # Disable sandboxing (useful for some environments)
options.add_argument("--disable-popup-blocking")    # Disable popup blocking
options.add_argument("--ignore-certificate-errors") # Ignore certificate errors
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)


# read and modify the variables from the config file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)



# Function to accept cookies
def accept_cookies():
    actions = ActionChains(driver)
    actions.move_by_offset(1, 1).click().perform()
    
def refresh_page():
    driver.refresh()
    accept_cookies()  # Accept cookies after refreshing

def login_portal():
    
    # Navigate to the Naukri website
    driver.get("https://www.naukri.com/nlogin/login")
    accept_cookies()
    

    username = "tusharmalhan@gmail.com"
    password = "tusharmalhan@21"


    sleep(2)
    # Enter your login credentials
    driver.find_element(By.ID, "usernameField").send_keys(username)
    driver.find_element(By.ID, "passwordField").send_keys(password)
    driver.find_element(By.ID, "passwordField").send_keys(Keys.ENTER)

    sleep(4)

login_portal()

def get_element_xpath(element):
    return str(driver.execute_script("function absoluteXPath(element) {var comp, comps = [];var parent = null;var xpath = '';var getPos = function(element) {var position = 1, curNode;if (element.nodeType == Node.ATTRIBUTE_NODE) {return null;}for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {if (curNode.nodeName == element.nodeName) {++position;}}return position;};if (element instanceof Document) {return '/';}for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {comp = comps[comps.length] = {};switch (element.nodeType) {case Node.TEXT_NODE:comp.name = 'text()';break;case Node.ATTRIBUTE_NODE:comp.name = '@' + element.nodeName;break;case Node.PROCESSING_INSTRUCTION_NODE:comp.name = 'processing-instruction()';break;case Node.COMMENT_NODE:comp.name = 'comment()';break;case Node.ELEMENT_NODE:comp.name = element.nodeName;break;}}for (var i = comps.length - 1; i >= 0; i--) {comp = comps[i];xpath += '/' + comp.name.toLowerCase();if (comp.hasOwnProperty('position')) {xpath += '[' + comp.position + ']';}}return xpath;}return absoluteXPath(arguments[0]);", element))

if re.search(r'Invalid', driver.page_source, re.IGNORECASE):
    driver.refresh()
    login_portal()
else:
    print('\nLogged in Successfully to Naukri Portal \n')


def click_apply_button(job_apply_element):
    
    """
    Clicks apply button where we could find in the page
    - if clicked successfully, return 1 else 0

    Returns:
        _type_: int
    """
    
    sleep(1)
    print('\nClicking on the apply button\n ')
    accept_cookies()
    sleep(1)
    apply_elements = driver.find_elements(By.XPATH, "//*[contains(normalize-space(text()), 'Apply') or substring(normalize-space(text()), string-length(normalize-space(text())) - string-length('interested') +1) = 'interested']")
    if not apply_elements:
        apply_elements = driver.find_elements(By.XPATH, "//button[contains(normalize-space(lyte-yield[@yield-name='text']), 'interested') or contains(normalize-space(lyte-yield[@yield-name='text']), 'apply')]")
    apply_elements_check = [i.text for i in apply_elements if i.text !='' and 'apply' in i.text.lower() or 'interested' in i.text.lower() ]
    if not apply_elements:
        apply_elements = driver.find_elements(By.XPATH, "//*[contains(@value, 'Apply') or contains(@value, 'apply')]")
        apply_elements_check = [i.get_attribute('value') for i in apply_elements if 'Apply' in i.get_attribute('value') or 'apply' in i.get_attribute('value')]
    # import pdb;pdb.set_trace()
    if not apply_elements_check and job_apply_element is None:
        print("\nCouldnt find any apply Button Issue in Web Page\n")
        return 0
    sleep(1)
    
    ## Clicking apply button only with text
    apply_elements = [i for i in apply_elements if i.text]
    try:
        button_clicked = False
        for element in apply_elements:
            try:
                element.click()
                print("Apply button clicked successfully!")
                button_clicked = True
                return 1
            except:
                driver.execute_script("arguments[0].click();", element)
                sleep(3)
                print("Apply button clicked successfully!")
                button_clicked = True
                return 1

        if not button_clicked:
            refresh_page()
            sleep(2)
            for element in apply_elements:
                try:
                    element.click()
                except:
                    driver.execute_script("arguments[0].click();", element)
                    sleep(3)
                    return 1
                else:
                    print("Apply button clicked successfully!")
                    return 1
    except:
        # print('\nFaced issue in clicking the Apply button')
        return 0

def page_404_error():
    """
    Check for 404 error in the page
    |   - if no error or message shown in 
    |   the website current url : return 1

    Returns:
        _type_: int
    """
    if re.search(re.escape('Requested page not found'), 
        driver.find_element(By.TAG_NAME, 'body').text, re.IGNORECASE) or \
        re.search(re.escape("The page you are looking for doesn't exist"), 
        driver.find_element(By.TAG_NAME, 'body').text, re.IGNORECASE) or \
        re.search(re.escape("page not found"), 
        driver.find_element(By.TAG_NAME, 'body').text, re.IGNORECASE) or \
        re.search(re.escape('Error 404'), driver.find_element(By.TAG_NAME, 'body').text, re.IGNORECASE) :
        print('\n\tIssue in the Webpage as some 404 error is found\n')
        return 0
    return 1

def contains_captcha_text():
    
    page_source = driver.page_source
    # driver.refresh()
    sleep(1.5)
    captcha_text = "We want to make sure it is actually you we are dealing with and not a robot."
    captcha_domain = 'geo.captcha-delivery.com'

    if re.search(re.escape(captcha_text), page_source, re.IGNORECASE) or captcha_domain in page_source:
        return True

    return False

def successfull_response():
    """ 
    This function checks for successful response 
    if the job is submitted successfully or
    the resume is uploaded to a file path
    """
    words = [ "Congratulations", "Thank you", 'successfully applied', 
             'Application Sent', 'Back to Application']
    for word in words:
        if re.search(r'\b' + re.escape(word) + r'\b', driver.find_element(By.TAG_NAME,'body').text, re.IGNORECASE) :
            return True

def is_career_section_unavailable():
    unavailable_keywords = [
        "Career Section Unavailable",
        "The Career section you are trying to access is not available",
        "The system may be under maintenance",
        "We apologize for any inconvenience",
        'Job you are looking for is expired'
    ]

    for word in unavailable_keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', driver.find_element(By.TAG_NAME,'body').text, re.IGNORECASE) :
            return True

    return False

def filling_questionnaire(company_name, job_data):
    # import pdb;pdb.set_trace()
    """
    Filling up the Questionnaire if Initiated
    by the Portal 
    """
    
    try:
        try:
            try:
                try:
                    sleep(3)
                    qus_form = driver.find_element(By.NAME, "qusForm")
                except:
                    qus_form = driver.find_element(By.NAME, "qupForm")
                
                print(f"\nQuestionnaire form found for company {company_name} ")
                questions = qus_form.find_elements(By.CLASS_NAME, "row.txtL")
                if not questions:
                    # questions = qus_form.find_elements(By.CLASS_NAME, "row")
                    return 1 
                    
                question_texts = []
 
                unanswered_questions = []
                sleep(1)
                for question in questions:
                    try:
                        question_text = question.text.split('\n')[0]
                        question_texts.append(question_text)
                        print('\n\n',question_text,end='\n')
                        try:
                            input_element = question.find_element(By.TAG_NAME, "input")
                        except:
                            input_element = question.find_element(By.TAG_NAME, "select")

                        input_type = input_element.get_attribute("type")
                        
                        # import pdb;pdb.set_trace()
                        if input_type == "text":
                            matched_key = next((key for key in question_mappings if key in question_text.lower()), None)
                            user_input = question_mappings.get(matched_key)
                            if not user_input:
                                user_input = input(f"\t: {question_text.lower() } ")
                            input_element = question.find_element(By.TAG_NAME, "input")
                            while True:
                                input_element.clear()  
                                input_element.send_keys(user_input)
                                
                                if len(user_input) > 100:
                                    error_message = "\n\t: You have exceeded the maximum limit of 100 characters"
                                    user_input = input(f"{error_message}\tPlease type again (under 100 characters):\t" )
                                else:
                                    break 
                            
                            print('\n\t: Response sent:\t', user_input,'\n')
                            user_input_text = user_input
                    
                        elif input_type == "date":
                            if "date" in question_text.lower():
                                user_input = "1999-03-02" 
                            else:
                                user_input = input(f"Enter in format (YYYY-MM-DD): ")
                            input_element.send_keys(user_input)
                            user_input_text = user_input
                                            
                        elif input_type == "checkbox":
                            while True:
                                user_input_text = []
                                options = question.find_elements(By.TAG_NAME, "input")
                                
                                for index, option_label in enumerate(options):
                                    label = option_label.find_element(By.XPATH, "../label")
                                    print(f"\t{index+1}. {label.text}")
                                
                                user_input = input("\n\tSelect the options you want to choose (numeric values separated by commas): ")
                                try:
                                    selected_options = [int(option_index.strip()) for option_index in user_input.split(",")]
                                except:
                                    print("\n\tApologies, Only integer values are allowed.\n")
                                    continue
                                
                                if not selected_options:
                                    selected_options.append(1)
                                    print("\tNo option selected. Selecting the first option by default.")

                                for option_index in selected_options:
                                    if option_index > 0 and option_index <= len(options) :
                                        option = options[option_index - 1]
                                        if not option.is_selected():
                                            option.click()
                                            text = options[option_index-1].text.strip()
                                            # import pdb;pdb.set_trace()
                                            if text is None or text =='':
                                                label_text = option.find_element(By.XPATH, "../label").text
                                                user_input_text.append(label_text)
                                            else:
                                                user_input_text.append(text)
                                            print(f"\tOption {option_index}.   {' '.join(user_input_text)}\t selected.")
                                            # import pdb;pdb.set_trace()
                                    else:
                                        # import pdb;pdb.set_trace()
                                        print("\n\tInvalid option selected...\n")
                                        print('\n\n',question_text,end='\n')
                                        continue
                                        
                                
                                # Break the loop if the user input is correct
                                break

                        elif input_type == "select-one":
                            # import pdb;pdb.set_trace()
                            while True:
                                dropdown = question.find_element(By.TAG_NAME, "select")
                                options = dropdown.find_elements(By.TAG_NAME, "option")
                                user_input_text = options[1].text
                                
                                for index, option in enumerate(options):
                                    if index == 0:
                                        continue  # Skip the "Select" option
                                    print(f"\t{index}. {option.text}")
                                
                                user_input = input("\n\tSelect an option (numeric value): ")
                                
                                try:
                                    user_input = int(user_input)
                                except ValueError:
                                    print("\n\n\tInvalid input. Please enter a numeric value.\n")
                                    print('\n\n',question_text,end='\n')
                                    continue
                                
                                if user_input > 0 and user_input <= len(options)-1:
                                    selected_option = options[user_input]
                                    selected_option.click()
                                    text = selected_option.text.strip()
                                    
                                    if text:
                                        user_input_text = text
                                    else:
                                        label = selected_option.find_element(By.XPATH, "../label")
                                        user_input_text = label.text
                                    print(f"\n\tSelected option: {user_input} - {user_input_text}\n")  # Print selected option with index
                                else:
                                    print("\n\tInvalid option selected....\n")
                                    print('\n\n',question_text,end='\n')
                                    continue
                                
                                # Break the loop if the user input is correct
                                break

                        elif input_type == "radio":
                            
                            # import pdb;pdb.set_trace()
                            while True:
                                radio_options = question.find_elements(By.TAG_NAME, "input")
                                options_displayed = False
                                user_input_text = ""
                                for index, option in enumerate(radio_options):
                                    option_label = option.find_element(By.XPATH, "../label")
                                    if not options_displayed:
                                        options_displayed = True
                                    print(f"\t{index+1}. {option_label.text}")
                                
                                user_input = input("\n\tSelect an option (numeric value): ")
                                
                                try:
                                    user_input = int(user_input)
                                except ValueError:
                                    print("\n\n\tInvalid input. Please enter a numeric value.\n")
                                    print('\n\n',question_text,end='\n')
                                    continue
                                
                                if user_input > 0 and user_input <= len(radio_options):
                                    selected_option = radio_options[user_input - 1]
                                    selected_option.click()
                                    
                                    label_text = selected_option.find_element(By.XPATH, "../label").text
                                    if label_text.strip():
                                        user_input_text = label_text
                                    else:
                                        user_input_text = option_label.text
                                    print(f"\tOption.   {user_input_text}\t selected.\n")
                                else:
                                    print("\n\tInvalid option selected....\n")
                                    print('\n\n',question_text,end='\n')
                                    continue
                                
                                # Break the loop if the user input is correct
                                break

                        job_data.append(['', '', '', '', '', '', question_text, input_type, user_input_text])
                        
                        # import pdb;pdb.set_trace()
            
                    except Exception as e:
                        
                        print(f'Error found from input type {input_type}\n', e,'\n')
                        # import pdb;pdb.set_trace()

                    # Check if the input element is empty after entering the answer
                    if not input_element.get_attribute("value"):
                        unanswered_questions.append(question_text)

                if unanswered_questions:
                    print("The following questions are left unanswered:")
                    for unanswered_question in unanswered_questions:
                        print(unanswered_question)
                    
                    for unanswered_question in unanswered_questions:
                        user_input = input(f"{unanswered_question}: ")
                        input_element = qus_form.find_element(By.XPATH, f"//*[text()='{unanswered_question}']/following-sibling::input")
                        input_element.send_keys(user_input)
                
                try:
                    ### Every question from Questionnaire was sent successfully
                    sleep(1)
                    submit_button = driver.find_element(By.ID, "qusSubmit")
                    submit_button.click()
                    return True
                
                except:
                    # import pdb;pdb.set_trace()
                    print('No Submit button found\n')
                    return 0
            
            except Exception as e :
                # import pdb; pdb.set_trace()
                # print(e)
                print(f"\nNo Questionnaire form found for company {company_name}.\n")
                return page_404_error()
                
        except:
            # import pdb;pdb.set_trace()
            qus_form = driver.find_element(By.ID, "qupSubmit").click()
            print('If Questionnaire fails, we submit the latest updates and move ahead\n')
            import pdb; pdb.set_trace()
            return 0
    except:
        # import pdb;pdb.set_trace()
        print("\bNo  Questionnaire found \n")
        import pdb; pdb.set_trace()
        return 1

def initialize_information():
    

    # my_info = {"Given": "Tushar", "First": "Tushar", "Family": "Malhan", "Last": "Malhan", "Full Name": "Tushar Malhan", "Local given Name": "Tushar", "Address": "Khargar Laxmi Nivas", "Email": "tusharmalhan@gmail.com", "city": "Navi Mumbai", "Postal code": "400614", "Phone Number": "7814891872", "phone extension": "+91", "password": "Test@123", "Verify new": "Test@123", "LinkedIn Profile": "https://www.linkedin.com/in/tushar-malhan-9981841ab", "Website": "https://github.com/tushar2malhan", "Github": "https://github.com/tushar2malhan"}    
    
    ### one liner
    # matched_label = next((label for key in my_info.keys() for label in driver.find_elements(By.XPATH, '//label|//*[text()]') if re.search(rf"({'|'.join(map(re.escape, key.split()))})", label.text, re.IGNORECASE)), None)
   
    ### one liner >>> use ! in pdb
    # !for key in my_info.keys(): key_words = key.split(); pattern = re.compile(rf"({'|'.join(map(re.escape, key_words))})", re.IGNORECASE); labels = driver.find_elements(By.XPATH, '//label'); matched_label = None; for label in labels: if pattern.search(label.text): matched_label = label; break; if matched_label: input_element = driver.find_element(By.XPATH, f"//label[text()='{matched_label.text}']/following-sibling::input"); value = input_element.get_attribute('value'); print(f"Key: {key}  Value: {value}"); else: label_text = input(f"No label found for key '{key}'. Please enter the corresponding label text: "); print(f"{key}: {label_text}")
    
    # import pdb;pdb.set_trace()
    sleep(1.5)
        
    def select_options():
        select_elements = driver.find_elements(By.XPATH, "//select")
        for select_element in select_elements:
            try:
                if select_element.text.strip():
                    continue
                # Find the heading of the select question
                heading_element = select_element.find_element(By.XPATH, "./ancestor::*[text()][1]")
                heading_text = heading_element.text.strip()
                
                if not heading_text:
                    continue
                    
                print(f'\n\t {heading_text}  \n')
                
                # Create a Select object for the select element
                select = Select(select_element)

                # Print the option text with index starting from 0
                options = select.options
                valid_choices = []
                for i, option in enumerate(options, start=0):
                    if option.text:
                        valid_choices.append(i)

                # Proceed further only if there are valid choices
                if valid_choices:
                    # Retrieve the option text using JavaScript
                    option_texts = driver.execute_script("return Array.from(arguments[0].options).map(option => option.textContent.trim())", select_element)

                    # Iterate over valid choices and their corresponding option texts
                    for choice in valid_choices:
                        option_text = option_texts[choice]
                        print(f"{choice}. {option_text}")

                    # Allow user input to select an option
                    while True:
                        try:
                            choice = int(input("Enter the number corresponding to your choice: "))
                            if choice in valid_choices:
                                break
                            print("Invalid choice. Please try again.")
                        except ValueError:
                            print("\n\n\tInvalid input. Please enter a number.")

                    selected_option_text = option_texts[choice]
                    selected_option = options[choice]
                    selected_option.click()
                    print(f"You selected: {selected_option_text}")
                    # Add your desired logic here
                else:
                    print("No valid options available")
                    # Handle the case when there are no valid choices
                    # Add alternative logic or display an appropriate message
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    try:
        select_options()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print('No select options available\n')


    def input_options():
        # Find input elements on the page
        form_element = None
        # import pdb;pdb.set_trace()
        try:
            form_element = driver.find_element(By.TAG_NAME, 'form')
        except: ...
        if form_element:
            input_elements = form_element.find_elements(By.XPATH, './/input[@type!="hidden" and not(@hidden) and (@class or @id)]|//select[@style!="display:none" and (@class or @id)]')
            if not input_elements:
                input_elements = form_element.find_elements(By.XPATH, './/input[@type="hidden"]')
        else:
            input_elements = driver.find_elements(By.XPATH, '//input[@type!="hidden" and not(@hidden) and (@class or @id)]|//select[@style!="display:none" and (@class or @id)]')

        if not input_elements:
            input_elements = driver.find_elements(By.TAG_NAME,'input')
        try:
            try:
                resume_button = driver.find_element(By.CSS_SELECTOR, "input.file-upload-input")
            except:
                try:
                    resume_button = driver.find_element(By.XPATH, "//button[contains(., 'resume')]")
                    driver.execute_script("arguments[0].removeAttribute('disabled');", resume_button)
                except:
                    resume_button = driver.find_element(By.XPATH, '//a[contains(text(), "resume")]')
            sleep(1)
            file_path = r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf"
            sleep(1)
            if resume_button:
                resume_button.send_keys(file_path)
                sleep(2)
                print(' Added file Attachment of Resume  ')
            else:...
        except:
            print('\nNo file Attachment Found of Resume, will try with input element. \n')

        def find_label_text(input_element):
            
            tags = ['label', 'input', 'textarea', 'div', 'span', 'p']  # Add more tags as needed
            label_text = None

            for tag in tags:
                try:
                    if tag == 'label':
                        # Check for previous label if tag is label
                        label_element = input_element.find_element(By.XPATH, f'./preceding::{tag}[1]')
                        label_text = label_element.text.strip()
                    elif tag == 'input':
                        # Find the preceding element of other tags except label
                        label_text = input_element.find_element(By.XPATH, './preceding::*[normalize-space(text())!=""][1]').text
                    else:
                        label_text = input_element.find_element(By.XPATH, f'./preceding::{tag}[1]').text
                        
                    if label_text:
                        break
                except Exception:
                    continue

            if not label_text:
                parent_element = input_element.find_element(By.XPATH, '..')
                parent_text = parent_element.text.strip()

                if '*' in parent_text:
                    grandparent_element = parent_element.find_element(By.XPATH, '..')
                    label_text = grandparent_element.text.strip()
            if not label_text:
                try:
                    label_text = input_element.get_attribute('id') or input_element.get_attribute('name')
                except Exception: ...
            return label_text


        if contains_captcha_text():
            import pdb;pdb.set_trace()
            sleep(1)
            print('\nContains Captcha, apply manually ')
            return 0

        # Iterate over the input elements
        import pdb;pdb.set_trace()

        for input_element in input_elements:
            # Try to find the inner input element's text or label
            label_text = None
            try:
                inner_text = input_element.text
            except: 
                inner_text = None
            ### if no inner text found, then find the latest element which contains text  
            if not inner_text:
                try:
                    import pdb;pdb.set_trace()
                    label_text = find_label_text(input_element)
                    # label = input_element.find_element(By.XPATH, './preceding::*[normalize-space(text())!=""][1]')
                    if not label_text:
                        placeholder_value = input_element.get_attribute("placeholder") or input_element.get_attribute('id') or input_element.get_attribute('name')
                        label_text = placeholder_value
                except:  
                    label_text = None

            if not label_text:
                label_text = input_element.get_attribute("value") or input_element.get_attribute("title")

            # Determine the type of input element
            input_type = input_element.get_attribute('type')

            response = None

            # Determine the type of input element
            input_type = input_element.get_attribute('type')
            response = None

            if label_text:
                # Suppose input type starts with 'email', that's why 'or' case is placed here
                print(f"Label Text: {label_text}")
                if (input_type == 'text') or input_type.lower() in [i.lower() for i in label_text.split()]:
                    print("\nTEXT OPTIONS\n")
                    import pdb;pdb.set_trace()

                    # Check if the label_text starts with or contains any key in my_info
                    found_key = None
                    for key in question_mappings:
                        if key and (key.lower() in label_text.lower() or label_text.lower() in key.lower()):
                            found_key = key
                    if not found_key:
                        found_key = next((key for key in my_info if key), None)
                        
                    if found_key:
                        # find the key from my_info dictionary and store the value in the response
                        if my_info.get(found_key) is not None:
                            response = my_info.get(found_key)
                        else:
                            if 'date' in input_type.lower():
                                # Prompt the user to enter the date value
                                date_input = input(f"Enter the date for '{label_text}' (YYYY-MM-DD): ")
                                try:
                                    # Validate the date format
                                    datetime.strptime(date_input, "%Y-%m-%d")
                                    response = date_input
                                except ValueError:
                                    print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
                            else:
                                # Prompt the user to enter the value, as label text couldn't be found in my_info
                                response = input(f"Enter value for '{label_text}': ")
                    else:
                        # Prompt the user to enter the value, as label text couldn't be found in my_info
                        response = input(f"Enter value for '{label_text}': ")

                    ### Enter the response in the input element
                    print(f'Response Given for {found_key}\t', response)
                    try:
                        input_element.send_keys(response)
                    except Exception as e:
                        print(' Issue in sending in the response', e)

                    # break

                elif 'date' in input_type.lower():
                    # Prompt the user to enter the date value
                    date_input = input(f"Enter the date for '{label_text}' (YYYY-MM-DD): ")
                    try:
                        # Validate the date format
                        datetime.strptime(date_input, "%Y-%m-%d")
                        response = date_input
                    except ValueError:
                        print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

                    # Enter the response in the input element
                    input_element.send_keys(response)
                    # child_input = input_element.find_element(By.CSS_SELECTOR, 'input')
                    # child_input.send_keys(response)

                elif input_type == 'select-one':
                    print("SELECTED OPTIONS")

                    import pdb;pdb.set_trace()

                    # Get the available options for the select element
                    options = input_element.find_elements(By.XPATH, './option')

                    # Display the label and available options to the user
                    if label_text is None or label_text == "*":
                        parent_element = input_element.find_element(By.XPATH, '..')
                        parent_text = parent_element.text
                        print("Parent Text:", parent_text)
                        label_text = parent_text

                    print(label_text)

                    for index, option in enumerate(options, start=1):
                        print(f"{index}. {option.text}")

                    # Prompt the user to select an option
                    selected_option_index = int(input("Enter the option number: ")) - 1

                    import pdb;pdb.set_trace()
                    # Select the chosen option
                    options[selected_option_index].click()

                elif input_type == 'file':

                    print("  FILE OPTIONS  ")

                    import pdb;pdb.set_trace()
                    # Prompt the user to enter the file path or provide it programmatically
                    input_id = input_element.get_attribute('id')
                    input_name = input_element.get_attribute('name')
                    if input_id and 'resume' in input_id.lower() or input_name and 'resume' in input_name.lower() or 'cv' in input_name.lower():
                        attribute_name = 'resume'
                        file_path = r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf"
                    else:
                        attribute_name = input_id or input_name
                        file_path = r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf"  # input(f"Enter the file path for {attribute_name}: \t {label_text} ")

                    # Set the file path for the file input element
                    input_element.send_keys(file_path)

                    sleep(3)
                    if successfull_response():
                        print('\n Resume Uploaded Successfully \n')

                elif input_type == 'radio':

                    print("RADIO OPTIONS")

                    # Find the parent element
                    parent_element = input_element.find_element(By.XPATH, '..')

                    # Print the text of the parent element
                    parent_text = parent_element.text.strip()
                    print(parent_text)

                    # Find all radio elements and their corresponding labels or child elements' text
                    radio_elements = parent_element.find_elements(By.XPATH, './/input[@type="radio"]')
                    for radio in radio_elements:
                        try:
                            label_text = radio.find_element(By.XPATH, './following-sibling::label').text
                            print(f"[{radio.get_attribute('value')}] {label_text}")
                        except NoSuchElementException:
                            child_text = radio.text
                            print(f"[{radio.get_attribute('value')}] {child_text}")

                    # Prompt the user to select a radio option
                    response = input("Enter the option: ")

                    # Find the corresponding radio element based on the response
                    radio_element = driver.find_element(By.XPATH, f'//label[contains(text(), "{response}")]/input[@type="radio"]')
                    radio_element.click()

                    print(f"\nLabel/Text: {label_text}\nInput Type: {input_type}\nValue given: {response}\n")

                    import pdb;pdb.set_trace()

        return input_elements

    try:
        elements = input_options()
    except:
        ... ;
        print('No input options available\n')


    # import pdb;pdb.set_trace()

    return elements

def manual_apply(job_data, job_title, company_name):
    """
      If quesForm not available, 
      it will fill the form manually 
      Any Issues in Manual apply will go down to the main app with message 
    |   - just return with the message or Number 
    |   - Main app will handle and mark the log the Issue
    """
    
     
    sleep(11)
    
    if not page_404_error():
        print("\nIssue in the Web page")
        return "Issue in Web Page"
    
    if contains_captcha_text():
        # import pdb;pdb.set_trace()
        sleep(1)
        print('\nContains Captcha, apply manually \n')
        return 0
    
    ## Finding apply button
    job_apply_element = None
    if job_title:
        try:
            job_apply_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{job_title}')]").click()
            try:
                # Scroll to the element if it's not visible
                if not job_apply_element.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", job_apply_element)

                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, get_element_xpath(button)))).click()
                except:
                    # Click on the element
                    job_apply_element.click()

            except :
                print("Element is not interactable or clickable.")
            # import pdb;pdb.set_trace()
        except: ...
    
    
    # import pdb;pdb.set_trace()
    initial_html = driver.page_source
    click_result = click_apply_button(job_apply_element)
    if not click_result:
        return 1
    sleep(5)
    updated_html = driver.page_source
    if initial_html == updated_html:
        # if not initialize_information():
            # import pdb;pdb.set_trace()
            print('\nNo info needs to be given, Apply manually')
            print("\nThe web page didn't change after clicking the Apply button.")
            print("\n Probably need to apply via Mail")
            return 1
    else:
        ...
    
    # Fill up questionnaire if required ! 
    result_ =  filling_questionnaire(company_name, job_data)
    
    sleep(2)

    # if no issue in result_ == webpage > Move Ahead
    if not result_:
        print("\nIssue in applying manually as page is not found ")
        return "Issue in Web Page as some 404 error is found"
    
    if successfull_response():
        print('\nFilled up the questionnaire, Applied to the job Successfully\n')
        return 1
    else: ...
    
    ### After clicking apply , check if it asks for account creation
    
      
    if contains_captcha_text():
        sleep(1)
        print('\nContains Captcha, apply manually \n')
        return 0

    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), 'Autofill with Resume')]").click()
        print('Checkbox Clicked which will apply directly with resume \n')
    except:
        print('No checkbox found for applying directly with resume')
    
    sleep(1)
    # def workday_form():
       
    #     import pdb;pdb.set_trace()
    #     initialize_information()
    #     try: next_button_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Next')]")
    #     except:...
    #     sleep(2)
    #     initialize_information()
    #     try: next_button_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Next')]")
    #     except:...
    #     sleep(2)
    #     initialize_information()
    #     try: next_button_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Next')]")
    #     except:...
    #     sleep(2)
    #     initialize_information()
    #     try: next_button_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Next')]")
    #     except:...
    #     sleep(2)
    #     initialize_information()
    #     try: next_button_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Next')]")
    #     except:...
    #     sleep(2)
    #     try:driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT')] | //input[contains(translate(@value, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT')]")
    #     except: ...
    
    # if "workdayjobs" in driver.current_url:
    #     print("URL contains 'workday jobs'. Returning 0.")
    #     return 0

        
    "Check if resume path is directly asked then run function workday_form()"
    # import pdb;pdb.set_trace()
    resume_button = None
    try:
        try:
            resume_button = driver.find_element(By.CSS_SELECTOR, "input.file-upload-input")
        except:
            resume_button = driver.find_element(By.XPATH, "//button[contains(., 'Browse resume')]")
            driver.execute_script("arguments[0].removeAttribute('disabled');", resume_button)
    except:...
    
    # if resume_button:
    #     workday_form()

    sleep(10)
    
    # Redirect Messages is present and click APPLY button
    try:
        redirect_message_element = driver.find_element(By.XPATH, "//*[contains(text(), 'redirect')]")
        if redirect_message_element and redirect_message_element.text:
            redirect_message = redirect_message_element.text
            # Switch to the new tab
            [driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != driver.current_window_handle]
            # Update the current URL to the redirected URL
            current_url = driver.current_url
            # Continue with the rest of your code
            initial_handles = driver.window_handles
            
            try:
                apply_elements = driver.find_elements(By.XPATH, "//*[starts-with(normalize-space(text()), 'Apply') or substring(normalize-space(text()), string-length(normalize-space(text())) - string-length('interested') +1) = 'interested']")  
            except:
                driver.find_element(By.XPATH, f"//*[contains(text(), {job_title})]").click()
            sleep(1.3)
            

            try:
                # import pdb;pdb.set_trace()
                [i.click() for i in apply_elements if i.text]
                sleep(1)
            except: 
                print("\n Couldnt find any apply Button\n")
                return 0

            ### CHECK if new tab is opened for applying the job
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(initial_handles) + 1))
            
            ### SWITCH to the last tab in one line
            [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != driver.current_window_handle ]
        
        else:
            print("\nNo redirect message found \n")
    except: print("\nNo redirect message found\n")

    
    ### try to accept norms if initiated
    try:    
        accept_element = driver.find_element(By.XPATH, "//input[contains(@title, 'Accept') or contains(@value, 'Accept')]")
        accept_element.click()
        sleep(2)
    except : ...
    
    # import pdb;pdb.set_trace()
    ### If Career Page Unavailable
    if is_career_section_unavailable():
        print("\nCareer page unavailable\n")
        return "Career Section Unavailable"
    
    sleep(10)
    
    ### We first try to create account for the User using the email id and password
    button_clicked = False
    try:
        try:
            create_account = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'START')]")
            sleep(0.5)
            create_account.click()
            button_clicked = True
            print(button_clicked)
        except:
            create_account = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'START')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')]")
        # import pdb;pdb.set_trace()
        sleep(1)
        if not create_account:
            create_account = driver.find_elements(By.XPATH, "//button[contains(., \"I'm interested\")]")
  
        create_account = [element for element in create_account if element.text]
        for button in create_account:
            sleep(1)
            try:
                driver.execute_script("arguments[0].click();", button)
                # for  _ in range(2):
                #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, get_element_xpath(button)))).click()
            except:
                print("\nClicked on element : Create Account")
                continue

    except:
        print("\nNo sign up required for the User, Can directly fill the form\n")
    
    try:
        print('Accepting Terms If Applicable')
        try:
            agree_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGREE')] | //span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGREE')]")
        except:
            agree_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONSENT')] | //span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONSENT')]")

        [i.click() for i in agree_element if i.text]
    
    except:
        print(' Not asked to accept agreement \n')

    
    ###  initialize_ the information in creating the account
    initialize_information()
    
    # import pdb;pdb.set_trace()
    if successfull_response():
        print("\nCongratulations Job applied automatically\n")
        return 1
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
    except:
        print('\nNo continue button found \n')
        
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()
        
    except:
        print('No Next button found \n')

    sleep(1.2)
    checkbox_elements = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    # [i.click() for i in checkbox_elements]
    # [driver.execute_script("arguments[0].click();", i) for i in checkbox_elements]

    
    for checkbox_element in checkbox_elements:
        try:
            checkbox_element.click()
            print("Checkbox clicked successfully!")
        except :
            print("Checkbox is not interceptable. Trying alternative approach...")
            driver.execute_script("arguments[0].click();", checkbox_element)
            print("Checkbox clicked using JavaScript execution!")

    sleep(1.2)

    ### IF SUBMIT CLICK IS THERE CLICK IT AND PROCCED TO OTHER JOBS
    submit = None
    try:
        submit = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT APPLICATION')] | //input[contains(translate(@value, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT APPLICATION')]")
    except: ...
    if submit:
        submit.click() 
        sleep(2)
        if successfull_response():
            print("\nCongratulations Job applied automatically\n")
            return True
        if 'error' in  driver.page_source:
            print('\n Some Issue occured while submitting application\n')
            print(driver.current_url)
            print('Apply MANUALLY\n')
            return driver.current_url
        else:
            print('\n Some captch issue \n')


    ### Create account Confirmation after giving values in the checkbox
    try:
        
        try:
            create_account = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'START')]")
            create_account.click()
        except:
            create_account = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'START')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')]")

        if not create_account:
            create_account = driver.find_elements(By.XPATH, "//button[contains(., \"I'm interested\")]")

        create_account = [element for element in create_account if element.text]
        for button in create_account:
            try:
                for  _ in range(2):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, get_element_xpath(button)))).click()
            except:
                print("\nClicked on element : Create Account")
                continue

    except:
        print("\n No sign up required for the User, Can directly fill the form")
    
    
    ## Check and confirm if User had already signed in earlier to the website 
    page_source = driver.page_source

    if "Sign in to this account or enter an email address that isn't already in use" in page_source:
        
        try:
            sign_in_button = driver.find_element(By.XPATH, "//button[translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') = 'SIGN IN']")
            sign_in_button.click()
            print("\n'Sign You In ', as you already created account here")
            print("Using the same credentials to login\n")
            initialize_information()   # fill in signed email and password
            sign_in_button = driver.find_element(By.XPATH, "//button[translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') = 'SIGN IN']")
            actions = ActionChains(driver)
            actions.move_to_element(sign_in_button).click().perform()
            sleep(4)
        except NoSuchElementException:
            print("No 'Sign in' button found.")
    else:
        print("The sign in error text has not appeared on the page.")

    # if "Verify your account" in page_source:
    # Wait for "Verify your account" page to disappear
    wait = WebDriverWait(driver, 10)
    # import pdb;pdb.set_trace()
    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Verify your account')]"):
        while wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verify your account')]"))):
            sleep(10)
            ### Keep on clicking  sign in again until User approves email Manually
            sign_in_button = driver.find_element(By.XPATH, "//button[translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') = 'SIGN IN']")
            actions = ActionChains(driver)
            actions.move_to_element(sign_in_button).click().perform()
        
        

    ### ATTACH RESUME
    try:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf")
    except:
        ...
    sleep(5)
    if successfull_response():
        print("\nFile uploaded successfully.\n")
    else:
        print("File upload message not found or does not contain 'Uploaded'.")
    sleep(4)

    # Click Continue button
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
    except:
        print('\nNo continue button found \n')

    # Fill Up Details
    initialize_information()
    
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
        button.click()
    except:
        print('\nNo continue button found \n')
   
    try:
        error_button = driver.find_element(By.XPATH, "//div[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ERRORS') or contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), '1 ERROR')]")
        print(error_button.text +" Found \t") if error_button.text is not None else print('No error')
    except: ...

    
    # element = driver.find_element(By.XPATH, "//button[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'websites')]")

    # PAGE 3  Work exp
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
        button.click()
    except:
        print('\nNo continue button found \n')
   


    # PAGE 4 acknowledgment
    try:

        checkbox_elements = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        [i.click() for i in checkbox_elements] 
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
        sleep(1)
    except:
        print('\nNo Checkbox element buttons found \n')
   

    # PAGE 5 Review  ~  SUBMIT
    try:
        driver.find_element(By.XPATH, "//button[text()='Submit']").click()
    except:
        driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT APPLICATION')] | //input[contains(translate(@value, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SUBMIT APPLICATION')]").click()  


    if successfull_response():
        print("\nCongratulations Job applied automatically\n")
    else:
        print("\nCouldnt submit the job successfully\n")


if __name__ == "__main__":

    def naukri_portal(experience, job_title, location, job_age, exclude_keywords):
        
        
        job_links_classname = config_data["job_links_classname"]
        all_job_classname = config_data.get('all_job_classname')
        job_variation_name = config_data.get('job_title').get('class_name')
        job_title_name_variation_2 = config_data.get('job_title').get('class_name_variation_2')
        
        company_name_raw = config_data.get('job_title').get('company_name_raw')
        company_name_variation_2 = config_data.get('job_title').get('company_variation_2')
        
        
        salary_classname = config_data.get('job_title').get('salary_classname')
        salary_classname_variation_2 = config_data.get('job_title').get('salary_classname_variation_2')
        
        
        apply_btn_classname = config_data.get('job_title').get('apply_btn_classname')
        apply_btn_cssname_variation_2 = config_data.get('job_title').get('apply_btn_cssname_variation_2')
        
        
        
        
        for positions in job_title:

            # import pdb;pdb.set_trace()
            job_title = '-'.join(positions.split(' ')).lower()
            job_url = f"https://www.naukri.com/{job_title}-jobs?experience={experience}"

            if location is None or location =="None":
                location_preference = [
                    location_to_city_type_gid[4].get("Hyderabad"), 
                    location_to_city_type_gid[5].get("bangalore"),
                    location_to_city_type_gid[5].get("Mumbai(All Areas)")
                    ]
                job_url = f"https://www.naukri.com/{job_title}-jobs?experience={experience}"
                for location in location_preference:
                    if location:
                        job_url += f"&cityTypeGid={location}"
            else:
                job_url +="&wfhType=2"

            # Add the CTC expectations to the job URL
            ctc_expectations_values = [ctc_expectations[5], ctc_expectations[6], ctc_expectations[4]]
            for ctc_expectations_value in ctc_expectations_values:
                job_url += f"&ctcFilter={ctc_expectations_value}"

            job_url += f"&jobAge={job_age}"

        
            sleep(2)
            driver.get(job_url)
            accept_cookies()

            # Get the current window handle.
            current_window_handle = driver.current_window_handle
            sleep(1)
            
            
            try:
                job_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, job_links_classname )))
                try:
                    sleep(1)
                    all_jobs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, all_job_classname  )))
                except:
                    all_jobs = [link.find_elements(By.TAG_NAME, "article") for link in job_links][0]
                print(f"\nLets initiate Automatic Job Search on Naukri Portal for {positions.upper()} position \n")
            
            except Exception as e :
                print(f"\n\t Apologies, No Jobs found for Position {positions.upper()} as per your requirement \n ")
                continue
        
            # Create a DataFrame to store the job data
            job_data = []

            for job in all_jobs:

                if job in applied_jobs:
                    continue
        
                # import pdb;pdb.set_trace()
                sleep(1)
            
                try:
                    job.click()
                    
                except:
                    sleep(1)
                    print("\nStaleElementReferenceException occurred in job click. Retrying...\n")
                    # import pdb;pdb.set_trace()
                    sleep(2)
                    try:
                        driver.refresh()
                        driver.get(job_url)
                        accept_cookies()
                        sleep(3.5)
                        job.click()
                    except:
                        driver.quit()
                        print("\nCant proceed with the stale element\n")
                        df.to_csv(csv_file_path, index=False)

                        # Print a success message
                        print(f"\nJob data has been saved to {csv_file_path}\n")
                        
                        # job_data.append([job_title, '', f"Not Applying because of keyword mentioned {keyword.lower()}", '', '', "No URL", '', '', ''])
                        # driver.refresh()
                        # driver.get(job_url)
                        # accept_cookies()
                        # sleep(3.5)
                        # job.click()
                    
                accept_cookies()
                sleep(2)
                
                ## Switch to the new tab.
                for window_handle in driver.window_handles:
                    if window_handle != current_window_handle:
                        driver.switch_to.window(window_handle)
            
                ## Switch to the new tab one liner
                # [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != current_window_handle ]

                    
                recruiters_details = "No Recruiters Details Found"
                
                try:
                    try:
                        try:
                            html_content = driver.find_element(By.CLASS_NAME, "job-desc").text
                        except:
                            html_content = driver.find_element(By.CLASS_NAME, "styles_job-desc-container__txpYf").text
                            
                        recruiters_details = re.findall(r'\+91\d{10}', html_content)
                        if not recruiters_details:
                            try:
                                recruiters_details = driver.find_element(By.CLASS_NAME, "rec-details").text
                            except:
                                recruiters_details = "No Recruiters Details Found"
                        else:...
                    except: 
                        # print('Look for phone number in description ')
                        recruiters_details = ''.join(recruiters_details)
                        
                except NoSuchElementException:
                    recruiters_details = "No Recruiters Details Found"

                    
                    
                    
                try:
                    job_title = driver.find_elements(By.CLASS_NAME, job_variation_name )
                    if not job_title:
                        job_title = driver.find_elements(By.CLASS_NAME, job_title_name_variation_2 )
                        if len(job_title) <=0:
                            job_title = driver.title
                    job_title = [i for i in job_title if i.text ][0].text
                        
                    apply_flag = True
                    for keyword in exclude_keywords:
                        if keyword.lower() in [i.lower().replace('(', '').replace(')', '') for i in job_title.split(' ')]:
                            print('Not applying for:', job_title, f' as keyword "{keyword.lower()}" is mentioned in the job title\n')
                            job_data.append([job_title, '', f"Not Applying because of keyword mentioned {keyword.lower()}", '', '', "No URL", '', '', ''])
                            apply_flag = False
                            break

                    if not apply_flag:
                        sleep(1)
                        driver.close()
                        driver.switch_to.window(current_window_handle)
                        sleep(1.5)
                        continue
                    
                    try:
                        company_name_raw = driver.find_element(By.CLASS_NAME, company_name_raw)
                    except:
                        company_name_raw = driver.find_element(By.CLASS_NAME, company_name_variation_2)
                    
                    company_name = company_name_raw.find_element(By.TAG_NAME, "a").text
                    try:
                        salary = driver.find_element(By.CLASS_NAME,salary_classname).text
                    except:
                        salary = driver.find_element(By.CLASS_NAME, salary_classname_variation_2 ).text
                        
                    print(f'\nClicking the Next Job Title {job_title}  Button...\t\n')
                    job_data.append([job_title, company_name, "Applied Successfully", salary, recruiters_details ,"No URL", '','',''])
                
                except Exception as e :

                    sleep(2)
                    print(f"\nFound some issues in getting meta info from the job we need to click \n" )

                    print("\n############## PORTAL TO APPLY DIRECTLY ON THE WEBSITE ############# \n")
                    
                    # import pdb;pdb.set_trace()

                    company_name = driver.title.split('-')[1].split(',')[0]
                    # result = manual_apply(job_data, job_title, company_name)
                    # if result == "Career Section Unavailable":
                    #     job_data.append([job_title, company_name, "Career Section Unavailable", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    # elif result == "Issue in Web Page":
                    #     job_data.append([job_title, company_name, "Issue in Web Page", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    # else:
                    #     job_data.append(["job_title", "company_name", "Apply manually on company's portal", "  Not Disclosed by Recruiter ", recruiters_details, driver.current_url, '','',''])
                    # driver.close()
                    # driver.switch_to.window(current_window_handle)
                    # sleep(3) 
                    continue
                
                ### Apply for the job        
                try:
                    try:
                        link_text = driver.find_elements(By.CLASS_NAME, apply_btn_classname )
                        if link_text:
                            link_text = link_text[0] 
                        else:
                            link_text = driver.find_elements(By.CSS_SELECTOR, apply_btn_cssname_variation_2 )[0]
                            
                    except NoSuchElementException:
                        link_text = driver.find_element(By.CLASS_NAME, "already-applied")
                        print(f"\nAlready applied to {company_name} for the title {job_title}.\n ")
                        job_data.append([job_title, company_name, "Already applied", salary, recruiters_details, "No URL", '','',''])
                        driver.close()
                        driver.switch_to.window(current_window_handle)
                        continue

                except NoSuchElementException:
                    print('\n############## PORTAL TO APPLY DIRECTLY ON THE WEBSITE ############# \n')
                    
                    try:
                        link_text = driver.find_element(By.CLASS_NAME, "company-site-button")
                        link_text.click()
                    except:
                        # link_text = driver.find_element(By.CLASS_NAME, "walkin-button")
                        print('\nWalkin position\n')
                    sleep(1.5)
                    company_website = driver.current_url

                    driver.close()
                    # Switch to company website
                    [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != current_window_handle ]

                    
                

                    # import pdb; pdb.set_trace()
                    # result = manual_apply(job_data, job_title, company_name)
                    # if result == "Career Section Unavailable":
                    #     job_data.append([job_title, company_name, "Career Section Unavailable", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    # elif result == "Issue in Web Page":
                    #     job_data.append([job_title, company_name, "Issue in Web Page", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    # else:
                    #     job_data.append(["job_title", "company_name", "Apply manually on company's portal", "  Not Disclosed by Recruiter ", recruiters_details, driver.current_url, '','',''])
                    # driver.close()
                    # driver.switch_to.window(current_window_handle)
                    # sleep(3)
                    continue
                
                sleep(1)
               
                print('Clicking Apply button... \t\n')
                
                
                try:    link_text.click()
                except: sleep(2.5);link_text.click()

                # import pdb;pdb.set_trace()
                print(' clicking on Update and apply button \n\t')

                sleep(2)
                
                if 'This company does not require you to apply again as you have previously' in driver.page_source:
                    print(f"\nJob submission failed for the title {job_title} to {company_name}, as company has blocked you\n")
                    job_data.append([job_title, company_name, "Company Banned You, LOL ! ", salary, recruiters_details ,driver.current_url, '','',''])
                    ### Switch back to original tab, as job cant be posted
                    driver.close()
                    driver.switch_to.window(current_window_handle)
                    continue

                filling_questionnaire(company_name, job_data)

            
                ### After filling the Quesstionnaire form , if still you find questionnaire, issue in Page
                qus_form = None
                try:
                    sleep(3)
                    qus_form = driver.find_element(By.NAME, "qusForm")
                except:
                    try:
                        qus_form = driver.find_element(By.NAME, "qupForm")
                    except: ...
                if qus_form:
                    print(f"\nApply Manually \nJob submission failed for the title {job_title} to {company_name}.\n")
                    job_data.append([job_title, company_name, "Submission Failed ", salary, recruiters_details ,driver.current_url, '','',''])
                    # import pdb;pdb.set_trace()
                    driver.close()
                    driver.switch_to.window(current_window_handle)
                    continue
                
                sleep(2)
                try:success_element = driver.find_element(By.CLASS_NAME, "apply-status-header.green")
                except:...
                daily_quota_limit = None
                
                try:daily_quota_limit = driver.find_element(By.XPATH, "//span[contains(text(),'Your daily quota has been expired.')]")
                except NoSuchElementException: ...
                if daily_quota_limit:
                    driver.close()
                    print("\nThe limit to apply to all your specific jobs has been reached!")
                    print('Catch yeah tommorrow')
                    break
                sleep(1.2)
                if success_element:
                    print(f"\nJob submitted successfully for the title {job_title} to {company_name}\n\n")
                    sleep(1)
                else:
                    try:
                        if link_text.text !='Applied':
                            # import pdb;pdb.set_trace()
                            print(f"Job submission failed for the title {job_title} to {company_name}.\n")
                            job_data.append([job_title, company_name, "Submission Failed ", salary, recruiters_details ,driver.current_url, '','',''])
                        else: ...
                    except:
                        driver.refresh()
                        driver.back()

                # close the driver for current job portal
                driver.close()

                # add the job to the set
                applied_jobs.add(job)

                # Switch back to the original tab.
                driver.switch_to.window(current_window_handle)

            # Generate a timestamp as the sheet name
            timestamp = datetime.now().strftime("%d_%m__%H__%M%S")
        
            # Create the main directory
            main_directory = "Naukri_Jobs_cv"
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)

            # Create the directory for the current date if it doesn't exist
            directory_name = datetime.now().strftime("%Y-%m-%d")
            directory_path = os.path.join(main_directory, directory_name)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Construct the full file path with the directory and file name
            csv_file_path = os.path.join(directory_path, f"job_data_{timestamp}.csv")

            # Create a DataFrame from the job data
            df = pd.DataFrame(job_data, columns=["Job Title", "Company Name", "Status", "CTC", "Recruiters Details" ,"URL", "question_text", "input type", "user input text"])
            
        
            df.to_csv(csv_file_path, index=False)

            # Print a success message
            print(f"\nJob data has been saved to {csv_file_path}\n")

        driver.quit()

    naukri_portal(experience, job_titles, location, job_age, exclude_keywords)





