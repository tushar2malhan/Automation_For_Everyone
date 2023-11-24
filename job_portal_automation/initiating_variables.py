import os
import re
from time import sleep
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

import configparser
config = configparser.ConfigParser()
# Read the configuration file
config.read("job_portal_automation/config.ini")
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
    "first": my_info.get               ("First", my_info.get("first", "")),
    "last": my_info.get                ("Last", my_info.get("last", "")),
    'email': my_info.get               ("Email", my_info.get("email", "tusharmalhan@gmail.com")),
    'gmail': my_info.get               ("Email", my_info.get("email", "tusharmalhan@gmail.com")),
    'mail': my_info.get                ("Email", my_info.get("email", "tusharmalhan@gmail.com")),
    'password': my_info.get            ("Password", my_info.get("password", "Test@123")),
    'credentials': my_info.get         ("Password", my_info.get("password", "Test@123")),
    'Verify New Password': my_info.get ("Password", my_info.get("password", "Test@123")),
    "number": my_info.get              ("Number", my_info.get("number", "")),
    "phone": my_info.get               ("Number", my_info.get("number", "")),
    "contact": my_info.get             ("Number", my_info.get("number", "")),
    "website": my_info.get             ("Github", my_info.get("github", "")),
    "github": my_info.get              ("Github", my_info.get("github", "")),
    "current city": my_info.get        ("City", my_info.get("city", "")),
    "current location": my_info.get    ("City", my_info.get("city", "")),
    "expected annual": my_info.get     ("ECTC", my_info.get("ectc", "")),
    "expected salary": my_info.get     ("ECTC", my_info.get("ectc", "")),
    "expected ctc": my_info.get        ("ECTC", my_info.get("ectc", "")),
    "salary expectation": my_info.get  ("ECTC", my_info.get("ectc", "")),
    "join": my_info.get                ("notice_period", my_info.get("Notice Period", "")),
    "languages": my_info.get           ("languages", my_info.get("Languages", "")),
    "languages": my_info.get           ("languages", my_info.get("Languages", "")),
    "job change": my_info.get          ("job_change_reason", my_info.get("Job Change Reason", "")),
    "current ctc": my_info.get         ("CTC", my_info.get("ctc", "")),
    "current annual ctc": my_info.get  ("CTC", my_info.get("ctc", "")),
    "current ctc": my_info.get         ("CTC", my_info.get("ctc", "")),
    "current annual ctc": my_info.get  ("CTC", my_info.get("ctc", "")),
    "expected annual": my_info.get     ("ECTC", my_info.get("ectc", "")),
    "expected salary": my_info.get     ("ECTC", my_info.get("ectc", "")),
    "expected ctc": my_info.get        ("ECTC", my_info.get("ectc", "")),
    "salary expectation": my_info.get  ("ECTC", my_info.get("ectc", "")),
    "notice period": my_info.get       ("notice_period", my_info.get("Notice Period", "")),
    "join": my_info.get                ("notice_period", my_info.get("Notice Period", "")),
    "when can you start": my_info.get  ("notice_period", my_info.get("Notice Period", "")),
    "when can you start": my_info.get  ("notice_period", my_info.get("Notice Period", "")),
    "university": my_info.get          ("university", my_info.get("University", "")),
    "school": my_info.get              ("university", my_info.get("School", "")),
    "institute": my_info.get           ("university", my_info.get("Institute", "")),
    "university": my_info.get          ("university", my_info.get("University", "")),
    "school": my_info.get              ("university", my_info.get("School", "")),
    "institute": my_info.get           ("university", my_info.get("Institute", "")),
    'LinkedIn':my_info.get             ('LinkedIn Profile','https://www.linkedin.com/in/tushar-malhan-9981841ab'),
    'linkedIn':my_info.get             ('LinkedIn Profile','https://www.linkedin.com/in/tushar-malhan-9981841ab'),
    'github':my_info.get               ('Github','https://github.com/tushar2malhan'),
    'website':my_info.get              ('Github','https://github.com/tushar2malhan'),
    'gender':                          ("Male"),
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

### location of the resume
DownloadLocation = str(os.path.join(Path.home(), "Documents\\"))
resume_file_path = DownloadLocation+"Tushar's Resume.pdf"
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
    password = ""


    sleep(2)
    # Enter your login credentials
    driver.find_element(By.ID, "usernameField").send_keys(username)
    driver.find_element(By.ID, "passwordField").send_keys(password)
    driver.find_element(By.ID, "passwordField").send_keys(Keys.ENTER)

    sleep(4)

def get_element_xpath(element):
    return str(driver.execute_script("function absoluteXPath(element) {var comp, comps = [];var parent = null;var xpath = '';var getPos = function(element) {var position = 1, curNode;if (element.nodeType == Node.ATTRIBUTE_NODE) {return null;}for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {if (curNode.nodeName == element.nodeName) {++position;}}return position;};if (element instanceof Document) {return '/';}for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {comp = comps[comps.length] = {};switch (element.nodeType) {case Node.TEXT_NODE:comp.name = 'text()';break;case Node.ATTRIBUTE_NODE:comp.name = '@' + element.nodeName;break;case Node.PROCESSING_INSTRUCTION_NODE:comp.name = 'processing-instruction()';break;case Node.COMMENT_NODE:comp.name = 'comment()';break;case Node.ELEMENT_NODE:comp.name = element.nodeName;break;}}for (var i = comps.length - 1; i >= 0; i--) {comp = comps[i];xpath += '/' + comp.name.toLowerCase();if (comp.hasOwnProperty('position')) {xpath += '[' + comp.position + ']';}}return xpath;}return absoluteXPath(arguments[0]);", element))

def click_apply_button(job_apply_element):
    
    """

        - Clicks apply button whereever we could find in the page 
        when trying to find and click it manuallu
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
                print("Apply button clicked‼️")
                button_clicked = True
                return 1
            except:
                driver.execute_script("arguments[0].click();", element)
                sleep(3)
                print("Apply button clicked‼️")
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
                    query = ' iframepath = document.querySelector("#email")'

                    driver.execute_script('document.querySelector("#email").value = "tushar"', element)
                    sleep(3)
                    return 1
                else:
                    print("Apply button clicked‼️")
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

def click_element_or_js(element):
    try:
        element.click()
    except Exception as e:
        # print("\nStaleElementReferenceException occurred. Clicking using JavaScript...\n")
        driver.execute_script("arguments[0].click();", element)
    
def chatbot_questionnaire():
    ### chatbot forum quite completed
    try:
        questions = driver.find_element(By.CLASS_NAME, 'chatbot_DrawerContentWrapper').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME,'li')
        if questions: print("Chat-bot Questions !")
        all_questions = []
        while 1:
            sleep(2)

            try:
                chat_bot_class_questions = driver.find_element(By.CLASS_NAME, 'chatbot_DrawerContentWrapper').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME,'li')
            except:
                print("\nNo more Chat bot questions need to be answered ")
                break
            for question in chat_bot_class_questions:
                question_text = question.text
                try:
                    chat_bot_class_questions = driver.find_element(By.CLASS_NAME, 'chatbot_DrawerContentWrapper').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME,'li')
                except:
                    print("\nNo more Chat bot questions need to be answered ")
                    break
                matched_key = next((key for key in question_mappings if key in question_text.lower()), None)
                if question.text not in all_questions and  question.text:
                    all_questions.append(question.text)
                    print('\n\n',question.text,'\n')
            try:
                chatbotInputContainer = driver.find_element(By.CSS_SELECTOR, '.chatbot_InputContainer')
                userInput = chatbotInputContainer.find_element(By.CSS_SELECTOR, '[data-placeholder]')
                
                userInput.clear()
                automated_input = question_mappings.get(matched_key)  if question_mappings.get(matched_key) else input('answer:\t')

                while True:

                    userInput.send_keys(automated_input)
                    
                    if len(automated_input) > 50:
                        error_message = "\n\t: You have exceeded the maximum limit of 50 characters"
                        automated_input = input(f"{error_message}\tPlease type again (under 100 characters):\t" )
                    else:
                        print(f"\nYour answer:\t{automated_input if not userInput.text else userInput.text}")
                        print()
                        break 
            except :
                try:
                    select_btn_options = driver.find_element(By.CLASS_NAME, 'singleselect-radiobutton-container')
                    print('\tRADIO button\n\tSelect the options:\n') if select_btn_options else None
                    
                    radio_buttons = select_btn_options.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
                    radio_button_options = {}
                    for index, radio_button in enumerate(radio_buttons):
                        radio_button_options[index + 1] = radio_button.get_attribute('value')
                    for index, option in radio_button_options.items():
                        print(f'\t{index}. {option}')
                    user_input = int(input('\tEnter Your option Number: ')) if radio_button_options else print('We are done\n')
                    radio_button_to_select = radio_buttons[user_input - 1]
                    try:
                        radio_button_to_select.click()
                    except :
                        # If the radio button element is not interactable, use JavaScript to click on it.
                        try:
                            driver.execute_script("document.querySelector('#{}').click()".format(radio_button_to_select.get_attribute('id')))
                        except:
                            ### tryna click label option if cant click the button's parent element
                            parent_element = radio_button_to_select.find_element(By.XPATH, '..')
                            parent_element.find_element(By.TAG_NAME,'label').click()
                            print("\n\tYou selected option:")           
                except:
                    checkbox_btn_options = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
                    print('\tCHECKBOX button\n\tSelect the options:\n ')if checkbox_btn_options else None
                    
                    checknox_button_options = {}
                    user_input_text = []

                    for index, checkbox_button in enumerate(checkbox_btn_options):
                        checknox_button_options[index + 1] = checkbox_button.get_attribute('value')

                    for index, option in checknox_button_options.items():
                        print(f'\t{index}. {option}')
                    
                    # user_input = int(input('\tEnter Your option Number: ')) if checkbox_btn_options else print('We are done\n')
                   
                    if checknox_button_options:
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
                            if option_index > 0 and option_index <= len(checkbox_btn_options) :
                                option = checkbox_btn_options[option_index - 1]
                                if not option.is_selected():
                                    click_element_or_js(option)

                                    text = checkbox_btn_options[option_index-1].text.strip()
                                    
                                    if text is None or text =='':
                                        label_text = option.find_element(By.XPATH, "../label").text
                                        user_input_text.append(label_text)
                                    else:
                                        user_input_text.append(text)
                                    print(f"\tOption {option_index}.   {' '.join(user_input_text)}\t selected.")    
                            else:
                                print("\n\tInvalid option selected...\n")
                                print('\n\n',question_text,end='\n')
                                continue
                                    
                                     
                    # checkbox_button_to_select = checkbox_btn_options[user_input - 1]
                    # try:
                    #     checkbox_button_to_select.click()
                    # except :
                    #     # If the select button element is not interactable, use JavaScript to click on it.
                    #     try:
                    #         checkbox_button_to_select.find_element(By.XPATH, "following-sibling::label[1]").click()
                    #         ### after label text click
                    #     except:
                    #         ### tryna click label option if cant click the button's parent element
                    #         ### Before label text click
                    #         parent_element = checkbox_button_to_select.find_element(By.XPATH, '..')
                    #         parent_element.find_element(By.TAG_NAME,'label').click()
                    #         print("\nYou selected option:")        


            send_btn = driver.find_element(By.CLASS_NAME,'sendMsg')
            send_btn.click()
    except:
        print("No Chat bot questions asked ‼️\n")