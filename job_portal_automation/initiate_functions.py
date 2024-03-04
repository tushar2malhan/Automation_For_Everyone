# '''
#         Description:  job Application Automation
#         Date:         30/06/2023
#         Status:       WIP
#         Author:       Tushar Malhan
# '''


# """ 

#     Config.ini  -> stores personal info for each user
#     Config.json -> stores classname attributes for the portal 
# """

# import os
# import csv
# import json
# import datetime
# import re
# import sys
# import pandas as pd
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from datetime import datetime
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
# import joblib


# from selenium.common.exceptions import ElementNotVisibleException
# from selenium.webdriver.support import expected_conditions
# from selenium.common.exceptions import TimeoutException

# # Import the variables from the initiating_variables module
# import initiating_variables
# question_mappings = initiating_variables.question_mappings
# ctc_expectations = initiating_variables.ctc_expectations
# location_to_city_type_gid = initiating_variables.location_to_city_type_gid
# experience = initiating_variables.experience
# job_titles = initiating_variables.job_titles
# location = initiating_variables.location
# job_age = initiating_variables.job_age
# exclude_keywords = initiating_variables.exclude_keywords
# my_info = initiating_variables.my_info

# driver = initiating_variables.driver
# page_404_error = initiating_variables.page_404_error
# contains_captcha_text = initiating_variables.contains_captcha_text
# successfull_response = initiating_variables.successfull_response
# get_element_xpath = initiating_variables.get_element_xpath
# click_apply_button = initiating_variables.click_apply_button
# is_career_section_unavailable = initiating_variables.is_career_section_unavailable
# accept_cookies = initiating_variables.accept_cookies
# wait = initiating_variables.wait
# login_portal = initiating_variables.login_portal
# click_element_or_js = initiating_variables.click_element_or_js
# chatbot_questionnaire = initiating_variables.chatbot_questionnaire
# resume_file_path = initiating_variables.resume_file_path
# photo_pic_path = initiating_variables.photo_pic_path

    
# def filling_questionnaire(company_name, job_data):
  
#     """
#     Filling up the Questionnaire if Initiated
#     by the Portal 
#     """
    
#     try:
#         try:
#             try:
#                 try:
#                     sleep(3)
#                     qus_form = driver.find_element(By.NAME, "qusForm")
#                 except:
#                     qus_form = driver.find_element(By.NAME, "qupForm")
                
#                 print(f"\nQuestionnaire form found to manually apply for company {company_name} ")
#                 questions = qus_form.find_elements(By.CLASS_NAME, "row.txtL")
#                 if not questions:
#                     # questions = qus_form.find_elements(By.CLASS_NAME, "row")
#                     return 1 
                    
#                 question_texts = []
 
#                 unanswered_questions = []
#                 sleep(1)
#                 for question in questions:
#                     print("\n Now Kindly Answer these questions to proceed ahead !")
#                     try:
#                         question_text = question.text.split('\n')[0]
#                         question_texts.append(question_text)
#                         print('\n',question_text,end='\n')
#                         try:
#                             input_element = question.find_element(By.TAG_NAME, "input")
#                         except:
#                             input_element = question.find_element(By.TAG_NAME, "select")

#                         input_type = input_element.get_attribute("type")
                        
                        
#                         if input_type == "text":
#                             matched_key = next((key for key in question_mappings if key in question_text.lower()), None)
#                             user_input = question_mappings.get(matched_key)
#                             if not user_input:
#                                 user_input = input(f"\t: ")
#                             input_element = question.find_element(By.TAG_NAME, "input")
#                             while True:
#                                 input_element.clear()  
#                                 input_element.send_keys(user_input)
                                
#                                 if len(user_input) > 100:
#                                     error_message = "\n\t: You have exceeded the maximum limit of 100 characters"
#                                     user_input = input(f"{error_message}\tPlease type again (under 100 characters):\t" )
#                                 else:
#                                     break 
                            
#                             print('\n\t: Response sent:\t', user_input,'\n')
#                             user_input_text = user_input
                    
#                         elif input_type == "date":
#                             if "date" in question_text.lower():
#                                 user_input = "1999-03-02" 
#                             else:
#                                 user_input = input(f"Enter in format (YYYY-MM-DD): ")
#                             input_element.send_keys(user_input)
#                             user_input_text = user_input
                                            
#                         elif input_type == "checkbox":
#                             while True:
#                                 user_input_text = []
#                                 options = question.find_elements(By.TAG_NAME, "input")
                                
#                                 for index, option_label in enumerate(options):
#                                     label = option_label.find_element(By.XPATH, "../label")
#                                     print(f"\t{index+1}. {label.text}")
                                
#                                 user_input = input("\n\tSelect the options you want to choose (numeric values separated by commas): ")
#                                 try:
#                                     selected_options = [int(option_index.strip()) for option_index in user_input.split(",")]
#                                 except:
#                                     print("\n\tApologies, Only integer values are allowed.\n")
#                                     continue
                                
#                                 if not selected_options:
#                                     selected_options.append(1)
#                                     print("\tNo option selected. Selecting the first option by default.")

#                                 for option_index in selected_options:
#                                     if option_index > 0 and option_index <= len(options) :
#                                         option = options[option_index - 1]
#                                         if not option.is_selected():
#                                             click_element_or_js(option)
                                           
#                                             text = options[option_index-1].text.strip()
                                            
#                                             if text is None or text =='':
#                                                 label_text = option.find_element(By.XPATH, "../label").text
#                                                 user_input_text.append(label_text)
#                                             else:
#                                                 user_input_text.append(text)
#                                             print(f"\tOption {option_index}.   {' '.join(user_input_text)}\t selected.")     
#                                     else:
#                                         print("\n\tInvalid option selected...\n")
#                                         print('\n\n',question_text,end='\n')
#                                         continue
                                        
                                
#                                 # Break the loop if the user input is correct
#                                 break

#                         elif input_type == "select-one":
                            
#                             while True:
#                                 dropdown = question.find_element(By.TAG_NAME, "select")
#                                 options = dropdown.find_elements(By.TAG_NAME, "option")
#                                 user_input_text = options[1].text
                                
#                                 for index, option in enumerate(options):
#                                     if index == 0:
#                                         continue  # Skip the "Select" option
#                                     print(f"\t{index}. {option.text}")
                                
#                                 user_input = input("\n\tSelect an option (numeric value): ")
                                
#                                 try:
#                                     user_input = int(user_input)
#                                 except ValueError:
#                                     print("\n\n\tInvalid input. Please enter a numeric value.\n")
#                                     print('\n\n',question_text,end='\n')
#                                     continue
                                
#                                 if user_input > 0 and user_input <= len(options)-1:
#                                     selected_option = options[user_input]
#                                     selected_option.click()
#                                     text = selected_option.text.strip()
                                    
#                                     if text:
#                                         user_input_text = text
#                                     else:
#                                         label = selected_option.find_element(By.XPATH, "../label")
#                                         user_input_text = label.text
#                                     print(f"\n\tSelected option: {user_input} - {user_input_text}\n")  # Print selected option with index
#                                 else:
#                                     print("\n\tInvalid option selected....\n")
#                                     print('\n\n',question_text,end='\n')
#                                     continue
                                
#                                 # Break the loop if the user input is correct
#                                 break

#                         elif input_type == "radio":
                            
                            
#                             while True:
#                                 radio_options = question.find_elements(By.TAG_NAME, "input")
#                                 options_displayed = False
#                                 user_input_text = ""
#                                 for index, option in enumerate(radio_options):
#                                     option_label = option.find_element(By.XPATH, "../label")
#                                     if not options_displayed:
#                                         options_displayed = True
#                                     print(f"\t{index+1}. {option_label.text}")
                                
#                                 user_input = input("\n\tSelect an option (numeric value): ")
                                
#                                 try:
#                                     user_input = int(user_input)
#                                 except ValueError:
#                                     print("\n\n\tInvalid input. Please enter a numeric value.\n")
#                                     print('\n\n',question_text,end='\n')
#                                     continue
                                
#                                 if user_input > 0 and user_input <= len(radio_options):
#                                     selected_option = radio_options[user_input - 1]
#                                     selected_option.click()
                                    
#                                     label_text = selected_option.find_element(By.XPATH, "../label").text
#                                     if label_text.strip():
#                                         user_input_text = label_text
#                                     else:
#                                         user_input_text = option_label.text
#                                     print(f"\tOption.   {user_input_text}\t selected.\n")
#                                 else:
#                                     print("\n\tInvalid option selected....\n")
#                                     print('\n\n',question_text,end='\n')
#                                     continue
                                
#                                 # Break the loop if the user input is correct
#                                 break

#                         job_data.append(['', '', '', '', '', '', question_text, input_type, user_input_text])
                        
                        
            
#                     except Exception as e:
                        
#                         print(f'Error found from input type {input_type}\n', e,'\n')
                        

#                     ### Check if the input element is empty after entering the answer
#                     if not input_element.get_attribute("value"):
#                         unanswered_questions.append(question_text)

#                 ### From the above questions asked, may be some questions were left unanswered, completing them ‼️
#                 if unanswered_questions:
#                     print("The following questions are left unanswered:")
#                     for unanswered_question in unanswered_questions:
#                         print(unanswered_question)
                    
#                     for unanswered_question in unanswered_questions:
#                         user_input = input(f"{unanswered_question}: ")
#                         input_element = qus_form.find_element(By.XPATH, f"//*[text()='{unanswered_question}']/following-sibling::input")
#                         input_element.send_keys(user_input)
                
#                 try:
#                     ### Every question from Questionnaire was sent successfully
#                     sleep(1)
#                     submit_button = driver.find_element(By.ID, "qusSubmit")
#                     submit_button.click()
#                     return True
                
#                 except:
                    
#                     print('No Submit button found\n')
#                     return 0
            
#             except Exception as e :
#                 # import pdb; pdb.set_trace()
#                 # print(e)
#                 print(f"No Questionnaire form found for company {company_name}.\n")
#                 return page_404_error()
                
#         except:
            
#             qus_form = driver.find_element(By.ID, "qupSubmit").click()
#             print('If Questionnaire fails, we submit the latest updates and move ahead\n')
#             import pdb; pdb.set_trace()
#             return 0
#     except:
        
#         print("\bNo  Questionnaire found \n")
#         import pdb; pdb.set_trace()
#         return 1

