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
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

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

applied_jobs = set()  


# Redirect SSL handshake error messages to nul (Windows)
if os.name == 'nt':
    sys.stderr = open(os.devnull, 'w')
# Redirect SSL handshake error messages to /dev/null (Linux/Mac)
if os.name == 'posix':
    sys.stderr = open('/dev/null', 'w')

def input_options_js(tag_name):
    '''
        find input elements via js if not found with python
    '''
    query = f"inputElements = document.querySelectorAll('{tag_name}'); "
    query += "return inputElements"
    all_inputs = driver.execute_script(query)
    print(all_inputs)

    
    query = " iframepath = document.querySelectorAll('input'); "
    query=query + ' return iframepath'
    query=query + ' console.log(iframepath) '
    driver.execute_script(query) 
    
def filling_questionnaire(company_name, job_data):
  
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
                
                print(f"\nQuestionnaire form found to manually apply for company {company_name} ")
                questions = qus_form.find_elements(By.CLASS_NAME, "row.txtL")
                if not questions:
                    # questions = qus_form.find_elements(By.CLASS_NAME, "row")
                    return 1 
                    
                question_texts = []
 
                unanswered_questions = []
                sleep(1)
                for question in questions:
                    print("\n Now Kindly Answer these questions to proceed ahead !")
                    try:
                        question_text = question.text.split('\n')[0]
                        question_texts.append(question_text)
                        print('\n',question_text,end='\n')
                        try:
                            input_element = question.find_element(By.TAG_NAME, "input")
                        except:
                            input_element = question.find_element(By.TAG_NAME, "select")

                        input_type = input_element.get_attribute("type")
                        
                        
                        if input_type == "text":
                            matched_key = next((key for key in question_mappings if key in question_text.lower()), None)
                            user_input = question_mappings.get(matched_key)
                            if not user_input:
                                user_input = input(f"\t: ")
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
                                            click_element_or_js(option)
                                           
                                            text = options[option_index-1].text.strip()
                                            
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
                                        
                                
                                # Break the loop if the user input is correct
                                break

                        elif input_type == "select-one":
                            
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
                        
                        
            
                    except Exception as e:
                        
                        print(f'Error found from input type {input_type}\n', e,'\n')
                        

                    ### Check if the input element is empty after entering the answer
                    if not input_element.get_attribute("value"):
                        unanswered_questions.append(question_text)

                ### From the above questions asked, may be some questions were left unanswered, completing them ‼️
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
                    
                    print('No Submit button found\n')
                    return 0
            
            except Exception as e :
                # import pdb; pdb.set_trace()
                # print(e)
                print(f"No Questionnaire form found for company {company_name}.\n")
                return page_404_error()
                
        except:
            
            qus_form = driver.find_element(By.ID, "qupSubmit").click()
            print('If Questionnaire fails, we submit the latest updates and move ahead\n')
            import pdb; pdb.set_trace()
            return 0
    except:
        
        print("\bNo  Questionnaire found \n")
        import pdb; pdb.set_trace()
        return 1

def initialize_information():
    
    """
        Lets sub-divide selected options and input options asekd in the page
        and allow user to give an answer to it !!
    """

    # my_info = {"Given": "Tushar", "First": "Tushar", "Family": "Malhan", "Last": "Malhan", "Full Name": "Tushar Malhan", "Local given Name": "Tushar", "Address": "Khargar Laxmi Nivas", "Email": "tusharmalhan@gmail.com", "city": "Navi Mumbai", "Postal code": "400614", "Phone Number": "7814891872", "phone extension": "+91", "password": "Test@123", "Verify new": "Test@123", "LinkedIn Profile": "https://www.linkedin.com/in/tushar-malhan-9981841ab", "Website": "https://github.com/tushar2malhan", "Github": "https://github.com/tushar2malhan"}    
    
    ### one liner
    # matched_label = next((label for key in my_info.keys() for label in driver.find_elements(By.XPATH, '//label|//*[text()]') if re.search(rf"({'|'.join(map(re.escape, key.split()))})", label.text, re.IGNORECASE)), None)
   
    ### one liner >>> use ! in pdb
    # !for key in my_info.keys(): key_words = key.split(); pattern = re.compile(rf"({'|'.join(map(re.escape, key_words))})", re.IGNORECASE); labels = driver.find_elements(By.XPATH, '//label'); matched_label = None; for label in labels: if pattern.search(label.text): matched_label = label; break; if matched_label: input_element = driver.find_element(By.XPATH, f"//label[text()='{matched_label.text}']/following-sibling::input"); value = input_element.get_attribute('value'); print(f"Key: {key}  Value: {value}"); else: label_text = input(f"No label found for key '{key}'. Please enter the corresponding label text: "); print(f"{key}: {label_text}")
    
    
    sleep(1.5)
        
    def select_options():
        '''
            Find all the selected options text and ask suser to choose their answer 
        '''
        select_elements = driver.find_elements(By.XPATH, "//select")
        for select_element in select_elements:
            try:
                
                ### Find the heading TEXT  of the selected question
                heading_element = select_element.find_element(By.XPATH, 'preceding-sibling::*[1]').text
                if not heading_element:
                    # preceding_sibling  with label 
                    heading_element = select_element.find_element(By.XPATH, 'preceding-sibling::label[1]').text
                    # next sibling  with label 
                    if not heading_element:
                        heading_element = select_element.find_element(By.XPATH, "following-sibling::*[1]").text

                    
                if type(heading_element) == list:
                    heading_element = heading_element[0]
                if not type(heading_element) == str:
                    heading_text = heading_element.text.strip()
                else:
                    heading_text = heading_element
                
                if not heading_text:
                    continue
                    
                print(f'\n\t {heading_text}  \n')
                

                ### Select object will print the options and ask user to give an answer
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
        print('No select options available in the page \n')
        print(f"An error occurred: {str(e)}")


    def input_options_python():
        
        # Find all the  input elements on the page
        form_element = None
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
            input_elements = [i  for i in input_elements if  i.get_attribute('value') =='']
        try:
            try:
                resume_button = driver.find_element(By.XPATH, "//button[contains(., 'resume') or contains(., 'Select file')]")
                driver.execute_script("arguments[0].removeAttribute('disabled');", resume_button)
            except:
                resume_button = driver.find_element(By.XPATH, '//input[contains(text(), "resume")]')
            sleep(1)
            file_path = resume_file_path
            sleep(1)
            if resume_button:
                resume_button.send_keys(file_path)

                sleep(2)
                print(' Added file Attachment of Resume  ')
                
                import autoit
                autoit.win_activate(driver.title)
                sleep(3)            
                dialog_window_title="Open"
                try:
                    lbl = autoit.win_get_state(dialog_window_title)
                    if lbl !=5:
                        autoit.win_active(dialog_window_title)
                        sleep(5)
                        print('gonna send the file of Resume from the local system') 
                        lbl = autoit.control_send(dialog_window_title, "Edit1", file_path)
                        print('Edit', lbl)
                        sleep(2)
                        lbl = autoit.control_click(dialog_window_title, "Button1")
                        print('Sent', lbl)
                except:
                    ...
            else:...
        except:
            print('\nNo file Attachment Found of Resume, will try with input element. \n')

        try:
            [i.send_keys(resume_file_path) for i in input_elements if i.get_attribute('type') == 'file' ]
            try:
                resume_name_from_website = [i.get_attribute('value') for i in input_elements if i.get_attribute('type') == 'file' ][0].split('\\')[-1]
                if resume_name_from_website == resume_file_path.split('\\')[-1]:
                    sleep(2)
                    print(' Added file Attachment of Resume, can see it clearly on the screen ')
            except:
                print("Place the file manually, as we couldnt detect the extact location of the file path ")
                ...
        except:
            print("Place the file manually, as we couldnt detect the extact location of the file path ")


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
            sleep(1)
            print('\nContains Captcha, apply manually ')
            return 0

        # Iterate over the input elements

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
            print("Gonna initiate with Input options\n")
            if label_text:
                print(f"\n\nLabel Text: {label_text}")
                
                if (input_type == 'text') or input_type.lower() in [i.lower() for i in label_text.split()]:
                    print("\nTEXT OPTIONS\n")

                    # Check if the label_text starts with or contains any key in my_info
                    found_key = None
                    for key in question_mappings:
                        if key and (key.lower() in list(map(lambda word: word.lower(), label_text.split(' '))) ):
                            found_key = key
                    if not found_key:
                        found_key = next((key for key in my_info if key), None)
                        
                    if found_key:
                        # find the key from my_info dictionary and store the value in the response
                        if question_mappings.get(found_key) is not None:
                            response = question_mappings.get(found_key)
                    
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

                    try:
                        try:
                            input_element.clear()
                        except: print("cant clear the element")
                        input_element.send_keys(response)
                        ### Enter the response in the input element
                        print(f'Response Given for {found_key}:\t', response)
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
                    print("\nSELECTED OPTIONS")

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

            
                    # Select the chosen option
                    options[selected_option_index].click()

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
                        radio = radio[0]
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


        return input_elements

    try:
        elements = input_options_python()
    except:
        ... 
        print('No input options available\n')
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
        
        sleep(1)
        print('\nContains Captcha, apply manually \n')
        return 0
    
    
    job_apply_element = None
    if job_title:
        try:
            job_apply_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{job_title}')]")
            try:
                # Scroll to the element if it's not visible
                if not job_apply_element.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", job_apply_element)

                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, get_element_xpath(job_apply_element)))).click()
                except:
                    # Click on the element
                    click_element_or_js(job_apply_element)
               

            except :
                print("Element is not interactable or clickable.")
        except: ...

    ### In manual login, if we find any of the job title to be included in excluded words,will come out of the loop
    apply_flag = True
    for keyword in exclude_keywords:
        if keyword.lower() in [i.lower().replace('(', '').replace(')', '') for i in job_title.split(' ')]:
            print('Not applying for:', job_title, f' as keyword "{keyword.lower()}" is mentioned in the job title\n')
            job_data.append([job_title, '', f"Not Applying because of keyword mentioned {keyword.lower()}", '', '', "No URL", '', '', ''])
            apply_flag = False
            break

    if not apply_flag:
        sleep(0.5)
        # [driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != driver.current_window_handle]
   
        return True
                  

    # initial_html = driver.page_source
    click_result = click_apply_button(job_apply_element)
    if not click_result:
        return 1
    sleep(5)
    # updated_html = driver.page_source
    # if initial_html == updated_html:
    #     # if not initialize_information():
    #         print('\nNo info needs to be given, Apply manually')
    #         print("\nThe web page didn't change after clicking the Apply button.")
    #         print("\n Probably need to apply via Mail")
    #         return 1
    # else:
    #     ...
    
    # Fill Up the Questions if asked in Manual applyting ‼️
    result_ =  filling_questionnaire(company_name, job_data)
    
    sleep(2)

    # if no issue in result_ == webpage > Move Ahead
    if not result_:
        print("\nIssue in applying manually as page is not found ")
        return "Issue in Web Page as some 404 error is found"
    
    if successfull_response():
        print('\nApplied to the job Successfully | Filled up the questionnaire\n')
        return 1
    else: ...
    
    ### After clicking apply , check if it asks for account creation
    
    ## solve the captch if its ask for the same.
    if contains_captcha_text():
        sleep(1)
        print('\nContains Captcha, apply manually \n')
        return 0

    def is_element_clickable(driver, element):

        """Checks if an element is clickable.

        Args:
            driver: A Selenium WebDriver object.
            element: A Selenium WebElement object.

        Returns:
            True if the element is clickable, False otherwise.
        """

        try:
            # Wait for the element to be visible and enabled.
            WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(element))
            return True
        except ElementNotVisibleException:
            # The element is not visible.
            return False
        except TimeoutException:
            # The element is not enabled.
            return False

    ### PART 1 : to Upload resume manually where it will allow to click the button
    try:

        anchor_and_button_elements = driver.find_elements(By.XPATH, "//a | //button")
        for element in anchor_and_button_elements:
            element_text = element.text.lower()
            data_source_attribute = element.get_attribute("data-source")
            if 'attach' in element_text or 'resume' in element_text or \
            (data_source_attribute is not None and 'attach' in data_source_attribute.lower()):
                is_clickable = is_element_clickable(driver, element)
                if is_clickable:
                    print(element.text)
                    element.click()



        print('Checkbox Clicked which will apply directly with resume \n')
    except:
        print('No checkbox found for applying directly with resume')
    
    sleep(1)

    ### PART 2 : to Upload resume manually
    resume_button = None
    try:
        try:
            all_inputs = driver.find_elements(By.CSS_SELECTOR, "input")
            for input in all_inputs :
                if input.get_attribute('type') == 'file':
                    resume_button = input
                    if 'resume' in input.get_attribute('id').lower() or 'resume' in input.get_attribute('name').lower() :
                        print("\nI'm Quite sure i clicked on the right button of resume, cause the name or id matches with the word resume.")
                    break
        except:
            resume_button = driver.find_element(By.XPATH, "//button[contains(., 'Browse resume')]")
            driver.execute_script("arguments[0].removeAttribute('disabled');", resume_button)
        if resume_button:
            resume_button.send_keys(resume_file_path)
            driver.execute_script("arguments[0].removeAttribute('disabled');", resume_button)
            print('\nAttached the resume:\t', resume_file_path)
    except:...
    
    # if resume_button:
    #     workday_form()

    sleep(10)
    
    # Redirect Messages is present and click APPLY button
    try:
        redirect_message_element = driver.find_element(By.XPATH, "//*[contains(text(), 'redirect')]")
        if redirect_message_element and redirect_message_element.text:
            redirect_message = redirect_message_element.text
            # Switch Back to previous tab
            [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != driver.current_window_handle ]
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

                [i.click() for i in apply_elements if i.text]
                sleep(1)
            except: 
                print("\n Couldnt find any apply Button\n")
                return 0

            ### CHECK if new tab is opened for applying the job
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(initial_handles) + 1))
            
            ### SWITCH Back to previous tab
            [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != driver.current_window_handle ]
        
        else:
            print("No redirect message found \n")
    except: print("No redirect message found\n")

    
    ### try to accept norms if initiated
    try:    
        accept_element = driver.find_element(By.XPATH, "//input[contains(@title, 'Accept') or contains(@value, 'Accept')]")
        accept_element.click()
        sleep(2)
    except : ...
    
    
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
        print('Accepting Terms If Applicable',end='\t')
        try:
            agree_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGREE')] | //span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'AGREE')]")
        except:
            agree_element = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONSENT')] | //span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CONSENT')]")

        [i.click() for i in agree_element if i.text]
    
    except:
        print('Not asked to accept agreement, moving ahead ! \n')

    
    ###  initialize_ the information in creating the account
    initialize_information()
    
    
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
            try:
                create_account = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'START')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')]")
                create_account.click()
            except:
                try:
                    create_account = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CREATE')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT')]")
                    create_account.click()    
                except:
                    element_id = create_account.get_attribute('id')
                    if element_id:
                        driver.execute_script("document.getElementById('" + element_id + "').click()")
                    else:
                        element_id = create_account.get_attribute('class')
                        driver.execute_script("document.getElementsByClassName('" + element_id + "').click()")

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
    
    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Verify your account')]"):
        while wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Verify your account')]"))):
            sleep(10)
            print('Waiting ... ')
            ### Keep on clicking  sign in again until User approves email Manually
            sign_in_button = driver.find_element(By.XPATH, "//button[translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') = 'SIGN IN']")
            actions = ActionChains(driver)
            actions.move_to_element(sign_in_button).click().perform()
        
        

    ### ATTACH RESUME
    try:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(resume_file_path)
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

def naukri_portal(experience, job_title, location, job_age, exclude_keywords):
        
    try:    
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
        apply_btn_cssname_variation_3 = config_data.get('job_title').get('apply_btn_cssname_variation_3')
        
        
        
        
        for positions in job_title:

            
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

            ### Add the CTC expectations to the job URL
            ctc_expectations_values = [ctc_expectations[5], ctc_expectations[6], ctc_expectations[4]]
            for ctc_expectations_value in ctc_expectations_values:
                job_url += f"&ctcFilter={ctc_expectations_value}"

            ### Change the job experience level in both url and front end 
            job_url += f"&jobAge={job_age}"

        
            sleep(2)
            driver.get(job_url)
            accept_cookies()

            sleep(5)
            ### Change the job experience level in both url and front end 
            span_element = driver.find_element(By.CLASS_NAME,'inside').find_element(By.TAG_NAME,'span');driver.execute_script("arguments[0].innerHTML = '3';", span_element)
           
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
                
                sleep(1)
                try:
                    click_element_or_js(job)
                except:
                    sleep(3)
                    print("\nStaleElementReferenceException occurred in job click. Retrying...\n")
                    
                    sleep(2)
                    try:
                        driver.refresh()
                        driver.get(job_url)
                        accept_cookies()
                        sleep(5)
                        click_element_or_js(job)
                    except:
                        print("\nCant proceed with the stale element\n")
                                    
                        # try:
                        #     job_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, job_links_classname )))
                        #     try:
                        #         sleep(1)
                        #         all_jobs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, all_job_classname  )))
                        #     except:
                        #         all_jobs = [link.find_elements(By.TAG_NAME, "article") for link in job_links][0]
                        #     print(f"\nLets initiate Automatic Job Search on Naukri Portal for {positions.upper()} position \n")
                        
                        # except Exception as e :
                        #     print(f"\n\t Apologies, No Jobs found for Position {positions.upper()} as per your requirement \n ")
                        #     continue
        
                        # df.to_csv(csv_file_path, index=False)

                        # # Print a success message
                        # print(f"\nJob data has been saved to {csv_file_path}\n")
                        # driver.quit()

                        
                        # job_data.append([job_title, '', f"Not Applying because of keyword mentioned {keyword.lower()}", '', '', "No URL", '', '', ''])
                        # driver.refresh()
                        # driver.get(job_url)
                        # accept_cookies()
                        # sleep(3.5)
                        
                    
                accept_cookies()
                sleep(2)
                
                ## Switch to the First tab.
                for window_handle in driver.window_handles:
                    if window_handle != current_window_handle:
                        driver.switch_to.window(window_handle)
            
                ## Switch to the First tab
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
                    recruiters_details = recruiters_details

                    
                    
                ###  Generate Info for the Job and save it in the csv file   
                try:
                    job_title = driver.find_elements(By.CLASS_NAME, job_variation_name )
                    if not job_title:
                        job_title = driver.find_elements(By.CLASS_NAME, job_title_name_variation_2 )
                        if len(job_title) <=0:
                            job_title = driver.title

                    ### extracting the text from first element
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
                        
                    print(f'\nClicking the  Job Title {job_title}  Apply Button...\t\n')
                    job_data.append([job_title, company_name, "Applied Successfully", salary, recruiters_details ,"No URL", '','',''])
                
                except Exception as e :

                    sleep(2)
                    print(f"Found some issues in getting meta info from the job we need to click \n" )

                    print("############## PORTAL TO APPLY DIRECTLY ON THE WEBSITE ############# \n")
                    
                    

                    company_name = driver.title
                    result = manual_apply(job_data, job_title, company_name)
                    if result == "Career Section Unavailable":
                        job_data.append([job_title, company_name, "Career Section Unavailable", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    elif result == "Issue in Web Page":
                        job_data.append([job_title, company_name, "Issue in Web Page", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    else:
                        job_data.append(["job_title" if not job_title else job_title, "company_name", "Applied on the company's portal", "  Not Disclosed by Recruiter ", recruiters_details, driver.current_url, '','',''])
                    driver.close()
                    driver.switch_to.window(current_window_handle)
                    sleep(3) 
                    continue
                

                ### Click on the apply button  
                try:
                    try:
                        link_text = driver.find_elements(By.CLASS_NAME, apply_btn_classname )
                        if link_text:
                            link_text = link_text[0] 
                        else:
                            link_text = driver.find_elements(By.CSS_SELECTOR, apply_btn_cssname_variation_2 )[0]
                            
                    except :
                        link_text = driver.find_element(By.CLASS_NAME, "already-applied")
                        print(f"Wait, Already applied to {company_name} for the title {job_title}.\n ")
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
                        link_text = driver.find_element(By.CLASS_NAME, apply_btn_cssname_variation_3)[0].click()
                    sleep(10)
                    company_website = driver.current_url
                    driver.close()
                    # Switch to company website
                    [ driver.switch_to.window(window_handle) for window_handle in driver.window_handles if window_handle != current_window_handle ]
                
                    ### WHEN MANUAL RUN , JUST RETURN FROM FUNCTION, DONT SWITCH IN WINDOW
                    result = manual_apply(job_data, job_title, company_name)
                    if result == "Career Section Unavailable":
                        job_data.append([job_title, company_name, "Career Section Unavailable", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    elif result == "Issue in Web Page":
                        job_data.append([job_title, company_name, "Issue in Web Page", "Not Disclosed by Recruiter", [], driver.current_url, '', '', ''])
                    else:
                        job_data.append(["job_title", "company_name", "Apply manually on company's portal", "  Not Disclosed by Recruiter ", recruiters_details, driver.current_url, '','',''])
                    driver.close()
                    driver.switch_to.window(current_window_handle)
                    sleep(3)
                    continue
                
                sleep(1)
                print('Clicking Apply button... \t\n')
                try:    link_text.click()
                except: sleep(2.5);link_text.click()
                print('Clicked on apply button ❗\t\n')
                sleep(2)

                ### check if company has disabled you to apply 
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
                    
                    driver.close()
                    driver.switch_to.window(current_window_handle)
                    continue
                #### will give answers to the chatbot questionnaire
                chatbot_questionnaire()
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
                    print(f"Job submitted successfully for the title {job_title} to {company_name}\n\n")
                    sleep(1)
                else:
                    try:
                        if link_text.text !='Applied':
                            
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

            timestamp = datetime.now().strftime("%d_%m__%H__%M%S")
        
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

    except Exception as e:
        print(str(e),'\n')
        print("\nIssue in one submitting request for the job\n")

def manual_intervention():
    websites = ['freshworks', 'tejas networks', 'amdocs', 'remotive', 'flexjobs', 'simplyhired', 'workingnomads', 'remoteok', 'remoterocketship', 'telus international', 'ets', 'quillbot']
   
    keywords = ["careers", "jobs", "positions", "employment"]

    keywords = ["careers"]
    valid_extensions = [".php", ".html", ""]  
    websites = websites[:1]
    for website in websites:
        
        driver.get('https://www.google.com/')

        # Search for the website keyword
        search_box = driver.find_element(By.NAME,'q')
        search_box.send_keys(website)
        search_box.send_keys(Keys.ENTER)
        url = None
        time.sleep(2)
        # Click the first search result
        first_result = driver.find_element(By.CSS_SELECTOR, 'div.tF2Cxc')

        if click_element_or_js(first_result):
            try:
                # Find all href attributes under the parent element
                href_elements = first_result.find_elements(By.CSS_SELECTOR, 'a[href]')
                for href_element in href_elements:
                    href_value = href_element.get_attribute('href')
                    url = href_value
                    print(href_value)
                driver.get(url)
            except:
                continue
    
            
        import time ; time.sleep(5)
        for keyword in keywords:
            url_with_keyword = driver.current_url + keyword
            # Check for valid extension
            valid_extensions = ["", ".php", ".html", ".aspx", ".jsp", ".aspx", ".htm", ".shtml", ".xhtml", ".cgi"]
            valid_url_found = False
            for extension in valid_extensions:
                full_url = url_with_keyword + extension
                print(full_url)
                driver.get(full_url)
                if "404" in driver.page_source or "Page not found" in driver.page_source or 'not found' in driver.page_source:
                    continue 
                else:
                    print(f"Valid URL found: {full_url}")
                    valid_url_found = True
                    break

if __name__ == "__main__":

    # manual_intervention()

    ### read and modify the variables from the config file
    with open('job_portal_automation/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    login_portal()

    if re.search(r'Invalid', driver.page_source, re.IGNORECASE):
        driver.refresh()
        login_portal()
    else:
        print('\nLogged in Successfully to Naukri Portal \n')

    naukri_portal(experience, job_titles, location, job_age, exclude_keywords)





