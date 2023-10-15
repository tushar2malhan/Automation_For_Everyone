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
        import pdb;pdb.set_trace()
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

