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


def get_web():
    url = "https://tresvistacareers.turbohire.co/surveys?token=SH3RVxWEbmWHSWgVU1ELI8fN8zzngUxfZ0Zmz5pVKVIDOsWVyUJn2d5XyNxRN8SnQuESBEcCgQA4Uw9_B67gMcnzs7ja1Qxmgtoclyp_4M%2Fj1zp55LRP_jhCNveetDQCW9zfGZHBippuDEVgDAZX1TYoLeNN1vp_20mZYPtwmhs=&company=nGouE9BaVHwVrgRUlwh3cqVB7jhQgMBxiNhOiYAT2%2Fc0JVdW1xICQmmiFoP4uAlZ&guest=tusharmalhan@gmail.com"

    # Initialize the Selenium WebDriver

    try:
        # Open the URL
        driver.get(url)
        time.sleep(2)  # Wait for the page to load



    finally:
        initialize_information()
        # Close the browser and quit the driver
        # driver.quit()



# Call the function to initialize the information
get_web()


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



