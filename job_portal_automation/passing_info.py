from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import datetime
import time
from time import sleep
from selenium import webdriver

driver = webdriver.Chrome()  # You may need to provide the path to your Chrome WebDriver

def get_web():
    url = "https://tresvistacareers.turbohire.co/surveys?token=SH3RVxWEbmWHSWgVU1ELI8fN8zzngUxfZ0Zmz5pVKVIDOsWVyUJn2d5XyNxRN8SnQuESBEcCgQA4Uw9_B67gMcnzs7ja1Qxmgtoclyp_4M%2Fj1zp55LRP_jhCNveetDQCW9zfGZHBippuDEVgDAZX1TYoLeNN1vp_20mZYPtwmhs=&company=nGouE9BaVHwVrgRUlwh3cqVB7jhQgMBxiNhOiYAT2%2Fc0JVdW1xICQmmiFoP4uAlZ&guest=tusharmalhan@gmail.com"

    # Initialize the Selenium WebDriver

    try:
        # Open the URL
        driver.get(url)
        time.sleep(2)  # Wait for the page to load



    finally:
        import pdb;pdb.set_trace()
        initialize_information()
        # Close the browser and quit the driver
        # driver.quit()


def initialize_information():


    # my_info = {"Given": "Tushar", "First": "Tushar", "Family": "Malhan", "Last": "Malhan", "Full Name": "Tushar Malhan", "Local given Name": "Tushar", "Address": "Khargar Laxmi Nivas", "Email": "tusharmalhan@gmail.com", "city": "Navi Mumbai", "Postal code": "400614", "Phone Number": "7814891872", "phone extension": "+91", "password": "Test@123", "Verify new": "Test@123", "LinkedIn Profile": "https://www.linkedin.com/in/tushar-malhan-9981841ab", "Website": "https://github.com/tushar2malhan", "Github": "https://github.com/tushar2malhan"}

    my_info = {
    "Given": "Tushar",
    "First": "Tushar",
    "Family": "Malhan",
    "Last": "Malhan",
    "Full Name":"Tushar Malhan",
    "Local given Name": "Tushar",
    "Address": "Khargar Laxmi Nivas",
    "Email": "tusharmalhan@gmail.com",
    "city": "Navi Mumbai",
    "Postal code": "400614",
    "Phone Number": "7814891872",
    "phone extension": "+91",
    "password":"Test@123",
    "Verify new":"Test@123",
    "LinkedIn Profile":"https://www.linkedin.com/in/tushar-malhan-9981841ab",
    "Website":"https://github.com/tushar2malhan",
    "Github":"https://github.com/tushar2malhan"
    }
    
    
    ### one liner
    # matched_label = next((label for key in my_info.keys() for label in driver.find_elements(By.XPATH, '//label|//*[text()]') if re.search(rf"({'|'.join(map(re.escape, key.split()))})", label.text, re.IGNORECASE)), None)
    ### one liner
    # !for key in my_info.keys(): key_words = key.split(); pattern = re.compile(rf"({'|'.join(map(re.escape, key_words))})", re.IGNORECASE); labels = driver.find_elements(By.XPATH, '//label'); matched_label = None; for label in labels: if pattern.search(label.text): matched_label = label; break; if matched_label: input_element = driver.find_element(By.XPATH, f"//label[text()='{matched_label.text}']/following-sibling::input"); value = input_element.get_attribute('value'); print(f"Key: {key}  Value: {value}"); else: label_text = input(f"No label found for key '{key}'. Please enter the corresponding label text: "); print(f"{key}: {label_text}")

    sleep(1.5)
    # # Iterate over each key in the my_info dictionary
    # for key, value in my_info.items():
        
    #     key_words = key.split()
    #     # Create a regular expression pattern to match the key or its associated value
    #     pattern = re.compile(rf"({'|'.join(map(re.escape, key_words))})", re.IGNORECASE)
        
    #     # Find the label element that matches the pattern
    #     labels = driver.find_elements(By.XPATH, '//label|//*[text()]') 
    #     matched_label = None
    #     for label in labels:
    #         if pattern.search(label.text):
    #             matched_label = label
    #             break
    #     if matched_label: # If a matching label is found, retrieve the associated input value
    #         import pdb;pdb.set_trace()
    #         try:
    #             label = driver.find_element(By.XPATH, f"//label[contains(text(), '{matched_label.text.split('(')[0]}')]")
    #             input_element = label.find_element(By.XPATH, "./following-sibling::div//input")
    #         except NoSuchElementException:
    #             try:
    #                 input_element = driver.find_element(By.XPATH, f"//input[@id='{matched_label.get_attribute('for')}']")
    #             except NoSuchElementException:
    #                 input_elements = driver.find_elements(By.TAG_NAME, 'input')
    #                 for element in input_elements:
    #                     if element.get_attribute('type') != 'hidden':
    #                         input_element = element
    #                         break
    #         input_element.clear()
    #         try:
    #             input_element.send_keys(value)
    #         except StaleElementReferenceException:
    #             label = driver.find_element(By.XPATH, f"//label[contains(text(), '{matched_label.text.split('(')[0] }')]")
    #             input_element = label.find_element(By.XPATH, "./following-sibling::div//input")
    #             input_element.send_keys(value)

    #         print(f"\n For Key: {key}   \t Value given: {value}\n")
    #     else:
    #         # Prompt the user to input the label text manually
    #         # label_text = input(f"No label found for key '{key}'. Please enter the corresponding label text: ")
    #         print(f"No label found for key {key}:   \n")

    import datetime

    def select_options():
        # Find input elements on the page
        input_elements = driver.find_elements(By.XPATH, '//input[@type!="hidden"]|//select[@style!="display:none"]')

        try:
            # try:
                # resume_button = driver.find_element(By.XPATH, "//button[contains(text(),'Attach')] | //a[contains(text(),'Attach')]")
            resume_button = driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ATTACH')] | //a[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ATTACH')]")
            # except:

            file_path = r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf"
            resume_button.send_keys(file_path)
            print(' Added file Attachment of Resume  ')
        except:
            print(' No file Attachment Found of Resume   ')



        # Iterate over the input elements
        import pdb;pdb.set_trace()
        for input_element in input_elements:
                # Try to find the label associated with the input element
            try:
                label = input_element.find_element(By.XPATH, './preceding::label[1]')
                label_text = label.text
            except:
                # If label not found, retrieve the text of the input element itself
                label_text = None

            # Determine the type of input element
            input_type = input_element.get_attribute('type')

            response = None
            
            if label_text:
                # Suppose input type starts with 'email', that's why 'or' case is placed here
                if (input_type == 'text') or input_type.lower() in [i.lower() for i in label_text.split()]:
                    print("TEXT OPTIONS")
                    import pdb;pdb.set_trace()

                    # Check if the label_text starts with or contains any key in my_info
                    for key in my_info:
                        if key and (key.lower() in (label_text.lower() if label_text else '')) :
                            # Check if the key already has a value assigned
                            if my_info.get(key) is not None:
                                response = my_info.get(key)
                            else:
                                if 'date' in input_type.lower():
                                    # Prompt the user to enter the date value
                                    date_input = input(f"Enter the date for '{label_text}' (YYYY-MM-DD): ")
                                    try:
                                        # Validate the date format
                                        datetime.datetime.strptime(date_input, "%Y-%m-%d")
                                        response = date_input
                                    except ValueError:
                                        print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
                                else:
                                    # Prompt the user to enter the value
                                    response = input(f"{label_text}\t: ")

                            # Enter the response in the input element
                            child_input = input_element.find_element(By.CSS_SELECTOR, 'input')
                            child_input.send_keys(response)
                            break

                    else:
                        if 'date' in input_type.lower():
                            # Prompt the user to enter the date value
                            date_input = input(f"Enter the date for '{label_text}' (YYYY-MM-DD): ")
                            try:
                                # Validate the date format
                                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                                response = date_input
                            except ValueError:
                                print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
                        else:
                            # If no match found, prompt the user to type a response
                            response = input(f"Input for '{label_text}'\t: ")

                        # Enter the response in the input element
                        input_element.send_keys(response)
                        child_input = input_element.find_element(By.CSS_SELECTOR, 'input')
                        child_input.send_keys(response)


                elif input_type == 'select-one' :
                    
                    print("SELECTED OPTIONS")
                    
                    import pdb;pdb.set_trace()
                    # Get the available options for the select element
                    options = input_element.find_elements(By.XPATH, './option')
                    
                    # Display the label and available options to the user
                    if label_text is None:
                        parent_element = input_element.find_element(By.XPATH, '..')
                        parent_text = parent_element.text
                        print("Parent Text:", parent_text)
                    else:
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
                if input_id and 'resume' in input_id.lower() or input_name and 'resume' in input_name.lower():
                    attribute_name = 'resume'
                    file_path = r"C:\Users\TusharMalhan\Documents\Tushar's_Resume.pdf"
                else:
                    attribute_name = input_id or input_name
                    file_path = input(f"Enter the file path for {attribute_name}: \t {label_text} ")

                # Set the file path for the file input element
                input_element.send_keys(file_path)

                sleep(3)
                if 'Success' in driver.page_source or "Uploaded"  in driver.page_source :
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

    select_options()


    import pdb;pdb.set_trace()



# Call the function to initialize the information
get_web()

