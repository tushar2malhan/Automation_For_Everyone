

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import math
import glob
import os
import pandas as pd
from datetime import datetime, timedelta
import shutil
import requests
import json
from pathlib import Path
import gspread
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
#from oauth2client.service_account import ServiceAccountCredentials
from dateutil import parser
from selenium.webdriver.common.keys import Keys
from PostFun import PostFun
import chromedriver_autoinstaller
import pyotp
from IRFun import IRFun
import autoit
import pyautogui
import zipfile
from tkinter import  messagebox  
import numpy as np

### OCR
import os
from datetime import datetime
import pandas as pd
from time import sleep
import os
from datetime import datetime
import pandas as pd
import cv2
import re
import time 
import os
import shutil
from PIL import Image
from io import BytesIO
import numpy as np
import urllib.request

### Email sending Imports 
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import xlwings as xw

from amazoncaptcha import AmazonCaptcha
import os
import re 
from datetime import datetime, timedelta 
import os
from datetime import datetime, timedelta

## DB setup
import pandas as pd
from datetime import datetime
import pytz
import sys
import re
from PostFun import PostFun



class RPA_Amazon_Dangerous_Goods_Appeal:
    
    def __init__(self):
        """
            Initializing all the variables
        """
        self.RPAID = 38
        self.CountryID =0
        self.ID = 0
        self.IsComplete =0
        self.PLID =0
        self.Status =0
        self.ProcessLog =''
        self.arr = []   
        self.IDList=[]
        self.body=''
        self.gsheetData=[]
        self.gsheetUpdate= []
        self._ASIN = ""
        self._ManualLog =  ""
        self.post = PostFun() 
        self.ir = IRFun()
        self.DownloadLocation = str(os.path.join(Path.home(), "Downloads\\"))
        self.asins_directory_path = self.DownloadLocation +'reports' 
        self.case_status_ = ''
        self.StartDate = datetime.now()
        self.minutes = 4
        self.current_asins_list = []
        self.StageData = []
        self.masterData = []
        self.excluded_asins = []
        self.Gsheet_Data_current_row = []
        self.final_name_file = None
        self.missing_MSDS_file_asins = []
        self.missing_MSDS_Lab_Report_file_asins = []
        self.DG_Products = []
        self.Non_DG_Products = []


        self.asins_MSDS_expired = []
        self.asins_Lab_expired = []

    def __del__(self):
        self.IDList=[]
        self.ID = -1
        del self
        print('Destructor called')       
 
    def openbrowser(self, flag):
        try:
          
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument("--mute-audio")            
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])


            
            try:
                chromedriver_autoinstaller.install(cwd=True)
            except Exception as err:                 
                print("chromedriver_autoinstaller ",str(err)) 
                self.post.ProcessErrorLog(self, 3, "CD " + str(err))

            #self.driver = webdriver.Chrome(chrome_options=chrome_options)            
            self.driver = webdriver.Chrome( executable_path='driver\chromedriver.exe',  chrome_options=chrome_options)  
            

            #self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
            #self.driver = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=chrome_options)           
            if flag ==1 :
                self.driver.get("https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n&initialSessionID=131-0804803-7281043&ld=SCUSWPDirect")            
            else:
                self.driver.get("https://www.amazon.com")

            print("openbrowser","Browser prepared successfully!") 
            #messagebox.showinfo("Init", "Browser prepared successfully!")
            self.post.ProcessErrorLog(self, 1, "CD Open Sucessfully")
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "CD " + str(err)) 

    def filllogin(self ):
        try:            
            emailid='gya.ads.portfolio.ai.01@gmail.com'
            password='`A3Rmqm/DHBJWF}B'

            time.sleep(3)
            self.driver.find_element_by_id("ap_email").send_keys(emailid)    
            time.sleep(3)
            self.driver.find_element_by_id("ap_password").send_keys(password)    
            time.sleep(3)
            self.driver.find_element_by_id("signInSubmit").click()

            self.otplogin()

            time.sleep(5)
            query='btns = document.querySelectorAll(".picker-button");'            
            query=query + 'for (let i = 0; i < btns.length; i++) { if (btns[i].textContent.trim() == "STI EU" ) {btns[i].click();} };'            
            self.driver.execute_script(query)

            time.sleep(5)
            query='list = document.querySelector("#picker-container > div > div.picker-body > div > div:nth-child(3) > div");'
            query=query + 'btns = list.getElementsByClassName("picker-button");'
            query=query + 'for (let i = 0; i < btns.length; i++) { if (btns[i].textContent.trim() == "United States" ) {btns[i].click();} };'
            #query=query + 'btns[12].click();'
            self.driver.execute_script(query)

            time.sleep(2)
            self.driver.execute_script('document.querySelector("#picker-container > div > div.picker-footer > div > button").click();')
            time.sleep(3)

            pt = self.ir.FindScreenshotPatch('never', self.driver.title )
            if pt !=[]:
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(pt[0]['x'] , pt[0]['y'] )    
                time.sleep(1)
                pyautogui.click()
                time.sleep(2)
                pyautogui.moveTo(1600, 10)
            else:
                print('never image not found')
                
            time.sleep(5)

            self.starttime = datetime.now()
            print("filllogin","Login successfully!") 
            self.post.ProcessErrorLog(self, 1, "Login successfully!") 
        except Exception as err:                 
            print("filllogin",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Login " + str(err)) 
            sys.exit()

    def otplogin(self ):
        try:

            time.sleep(5)
            # image = Image.open("QRCode\\3.png")
            # qr_code = pyzbar.decode(image)[0]
            # data= qr_code.data.decode("utf-8")
            # type = qr_code.type
            # text = f"{type}-->, {data}"
            # text = url_query_parameter(data, 'secret')
            text = 'LFNPECCHNTZQ6FRVZZRQHOH6CSERSLP45ACVZX6OYU63BZHALUKQ'
            totp = pyotp.TOTP(text)
            print(totp.now())
            self.driver.find_element_by_id("auth-mfa-otpcode").send_keys(totp.now()) 
            time.sleep(1)
            self.driver.find_element_by_id("auth-signin-button").click()
            
            
            print("otplogin","Login successfully!") 
            self.post.ProcessErrorLog(self, 1, "OTP successfully!")
        except Exception as err:                 
            print("otplogin",str(err)) 
            self.post.ProcessErrorLog(self, 2, "OTP " + str(err)) 
            sys.exit()

    def insert_update_data_Stage_(self, data, Status = 0, asin = None):
        """
            Updated / Inserts : public."DG_Appeal_Update"
        """
        try:
            
            if not asin:
                asin = self._ASIN

            jsondata = data
            jsondata['Job_Log_ID'] = str(self.ID)                                                                   
            jsondata['Product_ID'] = str(self._PK_ID)
            jsondata['Stage_ID'] = str(self.Stage_ID)
            if not Status:
                Status = 0   ### means we inserted a new entry if Status is not set
                print(f'Data Inserted Successfully for asin {self._ASIN} for Product ID =  {self._PK_ID}')
           
            jsondata = {key: value for key, value in jsondata.items() if value is not None}
            
            para = {    
                    "data" : {"userid":2, 'source': jsondata, "ID": Status , "table": "DG_Appeal_Update" },
                    "type":"Insert" }
            jsondata = self.post.PostApiParaJson(para)
            
            return jsondata

        except Exception as e:
            content = f"Error updating data in table: {e}"
            print(content)
            self.post.ProcessErrorLog(self, 2, f" Error updating data in table: {e}")
            return False

    def readStageTable(self):
        """
            First   step: Read master Table and return self.gsheetData
        """

        try:

            para = {
                "data": { "role": 1, "userid": 2, "table": "DG_Appeal"},
                "type": "Select"
            }
            post = PostFun()
            jsondata = self.post.PostApiParaJson(para)
            self.StageData = pd.DataFrame(jsondata['data'])
            self.post.ProcessErrorLog(self, 1, "Stage Sucessfully loaded")
            
            
            return self.StageData            
        
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Stage " + str(err)) 

    def readMasterTable(self):

        
        try:

            para = {
                "data": { "role": 1, "userid": 2, "table": "Product_Master"},
                "type": "Select"
            }
            post = PostFun()
            jsondata = self.post.PostApiParaJson(para)
            self.masterData = pd.DataFrame(jsondata['data'])
            self.post.ProcessErrorLog(self, 1, "gsheet Sucessfully loaded")
            
            
            return self.masterData            
        
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "gsheet " + str(err)) 

    def GET_ASINS(self):
        
        ### Amazon Portal
        self.driver.get('https://sellercentral.amazon.com/reportcentral/FBA_HAZMAT_INVENTORY/1')
        time.sleep(5)
        req_btn=self.driver.find_elements(By.CLASS_NAME,'download-report-page-kat-button-primary')
        if req_btn: req_btn = req_btn[0]
        req_btn.click()
        time.sleep(3)
        first_row = self.driver.find_element(By.XPATH, "//kat-table-body/kat-table-row[1]")
        last_column_cell = first_row.find_element(By.XPATH, "./kat-table-cell[last()]")
        file_download = None
        print("Wait until file download button is checked to be clicked..."); self.post.ProcessErrorLog(self, 1, f' Wait until file download button is checked to be clicked.. ')
        try:
            download_button = WebDriverWait(last_column_cell, 60).until( EC.presence_of_element_located((By.XPATH, "./kat-button[@label='Download']")) )
            download_button.click()
            print("Download button Clicked.")
            file_download = True
            self.post.ProcessErrorLog(self, 1, f'File Downloaded Successfully  ');print(f'File Downloaded Successfully   ')
            self._ManualLog = 'File Downloaded Successfully'
        except:
            print("Timed out waiting for Download button.")
            file_download = False
            self._ManualLog = "Issue In File Download "
            return False

        ### File Extraction  from Download location
        time.sleep(7)
        DownloadLocation = self.DownloadLocation
        files = os.listdir(DownloadLocation)
        all_csv_files = [i for i in (files) if i.endswith('.csv')]
        if all_csv_files and file_download:
            print(f'Finding File in Downloaded Section   '); self.post.ProcessErrorLog(self, 1, f'Finding File in Downloaded Section  ')
            for downloaded_file in all_csv_files:
                downloaded_file_name = downloaded_file.split('.csv')[0]
                file_name = fr"{DownloadLocation}{downloaded_file}"
                # print('file_name', file_name)
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_name))
                time_difference_minutes = (datetime.now() - file_creation_time).total_seconds() / 60

                if file_creation_time and  time_difference_minutes <= self.minutes:
                    try:
                        print(f'File Found !', file_name)
                        print(f"File creation time: {file_creation_time} was downloaded {round(time_difference_minutes)} minutes back,Case is true as compared to the time limit of {self.minutes} minutes.")
                        self.post.ProcessErrorLog(self, 1, f'File creation time: {file_creation_time} was downloaded{round(time_difference_minutes)} minutes back, Case is true as compared to the time limit of {self.minutes} minutes. ')
                        break
                    except Exception as e:
                        print(f"Error processing file {downloaded_file}: {e}")
                        self._ManualLog = "Error processing download csv file"
                        return False
                else:
                    print(f"No, csv file {file_name} it doesn't match with sheet {file_name} . Continue to the next file.")
                    continue

        if file_name and file_download:
            
            try:
                current_data = pd.read_csv(file_name, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    current_data = pd.read_csv(file_name, encoding='latin-1')
                except UnicodeDecodeError:
                    print("Unable to decode the file using 'utf-8' or 'latin-1' encoding.")
                    self._ManualLog = 'Issue in decoding csv file'
                    return False

            num_columns  = len(current_data.columns)
            length_template = len(current_data)
            
            if 'ASIN' in current_data.columns:

                self.current_asins_list = current_data['ASIN'].tolist()
                
                print(f'Number of columns in current_data: {num_columns}')
                print(f'Length of current Asins in DG: {length_template}')
                self.post.ProcessErrorLog(self, 1, f'Thus Copied the list of ASINs in self.current_asins_list Successfully  ')
                print(f'Thus Copied the list of ASINs in self.current_asins_list Successfully   ')
                self._ManualLog = "Got Asins List"
                return self.current_asins_list
                
            else:
                print('Column "ASIN" not found in current_data')
                self._ManualLog = 'Column "ASIN" not found in current_data'
                self.post.ProcessErrorLog(self, 1,self._ManualLog)
                return False
        else:
            print('No csv file downloaded yet')
            self._ManualLog = "No csv file downloaded yet"
            return False
      
    def loadASIN(self):
        try:
            ### Loading Asins in DB and self.IDList

            self.arr = []

            self.current_asins_list = self.GET_ASINS()
            
            
            if  not self.current_asins_list:
                self.post.ProcessErrorLog(self, 1, f'Csv file containing ASINs are empty or Download Button issue')
                print(f'self.current_asins_list variable is empty or Download Button issue, check loadASIN method... ')
                self._ManualLog = 'CSV file containing ASINs are empty'
                return False
            
            self.current_asins_list = list(set(self.current_asins_list))
            
            self.readStageTable()
            self.readMasterTable()
            
            
            asins_not_in_master = [c_asin for c_asin in self.current_asins_list if c_asin not in self.masterData['ASIN'].tolist()]
            

            
            self.excluded_asins = self.masterData[(self.masterData['SellableType'] !=  1) & (self.masterData['CountryID'] == 1)]['ASIN'].tolist()
            excluded_asins_str = ' '.join(list(set(self.excluded_asins)))
            self.post.ProcessErrorLog(self, 1, f'Current Non Sell ASINs = {excluded_asins_str}')

            
            ### Not creating any case for these asins, as they are Non Sell !
            self.post.ProcessErrorLog(self, 1, f'Current Non Sell asins  = {(len(list(set(self.excluded_asins))))} ')
            print(f'Current Non Sell asins  = {(len(list(set(self.excluded_asins))))}  ')

            # Calculate the variable to be deducted
            deducted_count = len(set(self.excluded_asins)) + len(set(asins_not_in_master))
            print('\nTotal dedicated count', deducted_count)
            
            ### Ignore the asins to be sent User to add them up 
            asins_not_in_master =  [asin for asin in asins_not_in_master if asin not in ["B0CM96ZRP3", "B077DQLMFD"]]
            if asins_not_in_master and datetime.now().weekday() == 0:
                self.post.ProcessErrorLog(self, 1, f'ASIN s {asins_not_in_master} not exist in PRODUCT MASTER table ')
                print(f'\nASINs  {asins_not_in_master} not exist  in PRODUCT MASTER table ')
                self._ManualLog  = f"These asins coming from amazon portal {str(asins_not_in_master)}  not exists in Master Table"
                
                body = f"""
                <br>
                Hi Javis,
                <br><br>
                This is to inform you that, These asins  {str(' '.join( asins_not_in_master ))} <br> cannot be added in DG Appeal System <br>
                To Add ASINs in DG Appeal System - please add the Above ASINs in Product Master List <br><br>

                Link - http://20.124.105.108/productmasterlist<br><br>

                Thanks """
                self.inform_users_via_mail(f"DG APPEAL: ASIN do not exists in Product Master ", body  )

            self.current_asins_list = list(set(self.current_asins_list) - set(self.excluded_asins)  - set(asins_not_in_master))

            # Update the logs and print statements
            self.post.ProcessErrorLog(self, 1, f'Now we run the asins for the count of {len(set(self.current_asins_list)) }\nSince, {len(set(self.excluded_asins))} ASINS are excluded and {len(asins_not_in_master)} of them are not present in the master Table. ')
            print(f'\nNow we run the asins for the count of {len(set(self.current_asins_list)) }, since, {len(set(self.excluded_asins))} ASINS are excluded and {len(asins_not_in_master)} of them are not present in the master Table. ')
            
            
            self.issues = []

            _master_asin = "None"
            for asin in self.current_asins_list:
                try:
                    current_row = self.masterData[self.masterData['ASIN'] == asin] 
                    _master_asin = current_row['ASIN'].iloc[0]
                    _master_ID = current_row["ID"].iloc[0]
                    
                    if _master_ID in self.StageData['Product_ID'].tolist():
                        self.post.ProcessErrorLog(self, 1, f'Case is On Going for this ASIN: {_master_asin}, Product ID: {_master_ID}  set it in the Stage Table ')
                        print(f'\nCase is On Going for this ASIN: {_master_asin}, Product ID: {_master_ID} - set it in the Stage Table ')
                    
                    elif not self.StageData.empty :
                        jsondata = {
                            "Product_ID" : str(_master_ID),
                            'DG_Class': "DG",
                            'Job_Log_ID': self.ID,
                            'Monitor_Status': 'On Going' }
                        
                        para = {    
                                "data" : {"userid":2, 'source': jsondata,  "table": "DG_Appeal" },
                                "type":"Insert" }
                        jsondata = self.post.PostApiParaJson(para)
                        print(jsondata.get('data'))
                        id_ = jsondata.get('data')
                        self.post.ProcessErrorLog(self, 1, f'Inserted New Entry for ASIN {_master_asin} with ID - {id_} in stage table.   ')
                        print(f'Inserted New Entry for ASIN {_master_asin} with  ID - {id_} in stage table.  ')

                except Exception as e:
                    self.post.ProcessErrorLog(self, 1, f'Issue in Inserting Records\n  ');print(f'Issue in Inserting Records\n  ')
                    print("Check this ASIN", _master_asin )
                    self.issues.append(_master_asin)
                    continue

            self.readStageTable()      
            
            self.gsheetData = pd.merge(self.StageData, self.masterData, how='left', left_on='Product_ID', right_on='ID')
            
                
            for asin_id in self.StageData['Product_ID'].tolist():   
                
                asin = self.masterData[self.masterData['ID'] == asin_id]['ASIN'].iloc[0]  #self.StageData['ASIN'].iloc[0]

                if asin not in self.current_asins_list:
                    self.Non_DG_Products.append(asin)
                else:
                    self.DG_Products.append(asin)
        


            for indices, row in enumerate(self.Non_DG_Products + self.DG_Products):
                self.arr.append( str(row).strip())  

        
            self.arr.append('')
            self.arr = set(self.arr)

            self.arr.remove('')
            self.arr = sorted(self.arr)
            
              
            self.ID = self.post.ProcessUpdate(self)
            self.IDList = self.post.ProcessLogUpdate(self)
           
            print("loadASIN","ASIN prepared successfully!") 
            self._ManualLog= 'ASIN prepared successfully'
            self.post.ProcessErrorLog(self, 1, "KeyList Prepared Sucessfully")
            return True
        except Exception as err:                 
            print("loadASIN",str(err)) 
            self.post.ProcessErrorLog(self, 2, "KeyList " + str(err)) ; self._ManualLog= 'Load ASIN method error'
            return False

    def upload_document(self, document):
        
        try:
            self.driver.get('https://sellercentral.amazon.com/fba/compliance-dashboard/index.html?mons_sel_mkid=amzn1.mp.o.ATVPDKIKX0DER&mons_sel_mcid=amzn1.merchant.o.A31LSP1L7F6XJ2&mons_sel_persist=true&stck=NA')
            time.sleep(5)
            self.driver.find_element(By.ID,'proactive-upload-link').click()
            time.sleep(2)
            self.driver.find_element(By.ID,'asinInput').send_keys(self._ASIN)
            time.sleep(3)
            
            ### select the document
            self.driver.find_element(By.XPATH, "//kat-button[@label='Choose file']").click()
            time.sleep(3)
            ### send the file
            import autoit
            autoit.win_activate(self.driver.title)
            sleep(4)            
            dialog_window_title="Open"
            try:
                lbl = autoit.win_get_state(dialog_window_title)
                if lbl !=5:
                    autoit.win_active(dialog_window_title)
                    sleep(5)
                    # print('gonna send the file of Resume from the local system') 
                    lbl = autoit.control_send(dialog_window_title, "Edit1", document)
                    print('Edit', lbl)
                    sleep(2)
                    lbl = autoit.control_click(dialog_window_title, "Button1")
                    print('Sent', lbl)
            except:
                self.post.ProcessErrorLog(self, 1, f'Document not uploaded correctly  ');print(f'Document not uploaded correctly  ')
                return False
            
            self.driver.find_element(By.XPATH, "//kat-dropdown[@placeholder='Specify document language']").click()
            time.sleep(2)
            
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.ENTER )
            actions.perform()


            ### upload the doc
            self.driver.find_element(By.XPATH, "//kat-button[@label='Upload']").click()
            time.sleep(5)
            return True
        
        except Exception as e:
            self.post.ProcessErrorLog(self, 1, f'Exception in document upload, {e} ');print(f'Exception in document upload, {e} ')
            self._ManualLog = 'Issue in Document upload'
            return False

    def seller_support_case(self, asin, file_path, report_type=None, subject = None ):

        try:    
            

            self.driver.get("https://sellercentral.amazon.com/home?mons_sel_dir_mcid=amzn1.merchant.d.ADVSOBI7NLBGFP3CTZPHOFNEOKCA&mons_sel_mkid=A1F83G8C2ARO7P&mons_sel_dir_paid=amzn1.pa.d.ACK2GASJ5Y6PL7M4KUAMRCL7EO2A&ignore_selection_changed=true&mons_redirect=change_domain")
            sleep(3)

            #self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.get("https://sellercentral.amazon.com/help/hub/support/INTENT_CTI_PSS")
            sleep(5)
            
            # if asin:
            print("\nTxT for DG APPEAL \n")

            if report_type == 'Partial':
                txt ="Dear Seller Support,, \n\n"
                txt = txt + f"My ASIN {asin} is supposed to be NON-DG, however it currently has been classified as DG. \n"
                txt = txt + f"Highly appreciated that could you please assist to have this investigated into for reclassification.\n"
                txt = txt + f'I herewith enclose my "SDS"  for your perusal.'
                txt = txt + "\n\nRegards, \n"
                txt = txt + "Alex"
                print(txt)
                self.post.ProcessErrorLog(self, 1, txt)
            else:
                txt ="Dear Seller Support,, \n\n"
                txt = txt + f"My ASIN {asin} is supposed to be NON-DG, however it currently has been classified as DG. \n"
                txt = txt + f"Highly appreciated that could you please assist to have this investigated into for reclassification.\n"
                txt = txt + f'I herewith enclose my "SDS" included the "Identification and Classification Report for Air Transport of goods" for your perusal.'
                txt = txt + "\nRegards, \n"
                txt = txt + "Alex"
                print(txt)
                self.post.ProcessErrorLog(self, 1, txt)

    

            
            #Not listed issue btn
            self.driver.execute_script("window.scrollBy(0, 1000)") 
            self.driver.execute_script('document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div > div > div > div > div > div:nth-child(2) > div > div > div > div.button-options > kat-button").shadowRoot.querySelector("button").click()')
            sleep(2)


            #Or, send text 
            self.driver.execute_script('document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div > kat-textarea").shadowRoot.querySelector("#katal-id-19").focus()')
            actions = ActionChains(self.driver)
            actions.send_keys(txt)
            actions.perform()
            print(txt)
            print('Text Inserted ')
            self.post.ProcessErrorLog(self, 1, f'Text Inserted ')
            sleep(2)
            self.driver.execute_script("window.scrollBy(0, 1000)") 

            #Continue btn
            self.driver.execute_script("window.scrollBy(0, 1000)") 
            continue_button_script = '''
                var mainFrame = document.querySelector("#mons-body-container").contentWindow;
                var continueButtonSelector = "#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div.button-options > kat-button";
                var continueButton = mainFrame.document.querySelector(continueButtonSelector);
                continueButton.click();
            '''
            self.driver.execute_script("window.scrollBy(0, 1000)") 
            self.driver.execute_script( continue_button_script)
            time.sleep(5)
            self.driver.execute_script("window.scrollBy(0, 1000)") 
            
            try:
                ## issus not listed
                self.driver.execute_script( 'document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div > div > div > div > div.button-options > kat-button:nth-child(4) > div").click()')
                time.sleep(2)
                self.driver.execute_script("window.scrollBy(0, 1000)") 
            except: ...
            
            try:
                ## Account related
                self.driver.execute_script( 'document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div > div > div:nth-child(2) > div > div.button-options > kat-button:nth-child(1) > div > div").click()' )
                time.sleep(5)
                self.driver.execute_script("window.scrollBy(0, 1000)") 
            except: ...


            sleep(2)

            ### setting up the short description
            try:          
                query = ' iframepath = document.querySelector("#mons-body-container");'
                query = query + f' iframepath.contentWindow.document.querySelector("#root > div > form > div > div:nth-child(2) > kat-input").shadowRoot.querySelector("#input-1").value = "{subject}";'                      
                # query=query + ' console.log(iframepath.contentWindow.document.querySelector("#send-email-button"));'
                self.driver.execute_script(query) 
                sleep(5)
            except: 
                for _ in range(2):
                    time.sleep(1)
                    actions = ActionChains(self.driver) 
                    actions.send_keys(Keys.TAB )
                    actions.perform()
                
                actions = ActionChains(self.driver) 
                actions.send_keys(f"{subject}" )
                actions.perform()
                sleep(5)
            

            self.driver.execute_script("window.scrollBy(0, 1000)") 


            ### click on email
            for _ in range(1):
                time.sleep(2)
                actions = ActionChains(self.driver) 
                actions.send_keys(Keys.TAB )
                actions.perform()
            
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.ENTER )
            actions.perform()

            self.driver.execute_script("window.scrollBy(0, 1000)") 


            ### Add attachments to the case
            time.sleep(5)
            
            pt = self.ir.FindScreenshotPatch('addattachments', self.driver.title )
            if pt !=[]:
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(pt[0]['x'] , pt[0]['y'] ) 
                pyautogui.click()
                time.sleep(1)
                pyautogui.moveTo(1700, 10)
            else:
                print('addattachments image not found')
                self.post.ProcessErrorLog(self, 1, f'addattachments image not found')
                self._ManualLog = self._ManualLog + '. ' + 'addattachments image not found'
                # return False

            dialog_window_title="Open"
            lbl = autoit.win_get_state(dialog_window_title)
            if lbl !=5:
                autoit.win_active(dialog_window_title)
                time.sleep(2)
                lbl = autoit.control_send(dialog_window_title, "Edit1", file_path)
                print('Edit ', lbl)
                self.post.ProcessErrorLog(self, 1, f'Edit ')
                time.sleep(2)
                lbl = autoit.control_click(dialog_window_title, "Button1")
                print('Button1 ', lbl)
                self.post.ProcessErrorLog(self, 1, f'Button1 ')
                print(file_path,' Image added')
                time.sleep(5)

            sleep(5)
            self.driver.execute_script("window.scrollBy(0, 1000)") 

        
            ### send button 
            for _ in range(1):
                time.sleep(1)
                actions = ActionChains(self.driver) 
                actions.send_keys(Keys.TAB )
                actions.perform()
            
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.ENTER )
            actions.perform()  
            self.driver.execute_script("window.scrollBy(0, 1000)") 
        
            #### get case id
            time.sleep(10)
            caseid = 'caseid = document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div > div.meld-case-created-outer-container > div > div > p:nth-child(2) > a").textContent; '
            caseid += 'return caseid ;'
            caseid = self.driver.execute_script(caseid)
            print(caseid)
            self.post.ProcessErrorLog(self, 1, f" case id = {caseid } ")
            _ManualLog = caseid
            self._ManualLog = caseid

        
            return _ManualLog
        
        except Exception as err:  
            print('seller_support_case  issue ',str(err))
            self.post.ProcessErrorLog(self, 2, f"  seller_support_case issue  {err}")
            _ManualLog = "Error Case Log PSS"
            return False
   
    def generate_email_html(self,  seller_support_case_id , asin ):
            
            """
                Html template for Dangerous goods
            """
            try:
                
                
                body = f"""Dear Issue Assistance Team,<br><br>
                <br>
                Please take note that the following ASIN is incorrectly classified as Dangerous Goods. <br>
                Attached the SDS and safety transportation certification for your reference and perusal. <br>
                Please be informed that the certification is included in the Page 8-12 and definitely showed that the below ASIN is not restricted for the transportation.<br>
                <br>
                ASIN  -  {asin}
                <br>
                Regards,<br>
                Jarvis
                <br><br>
                """

                issue_details_content_1 = 'Uploaded SDS with Safety Transportation Certification to Amazon system'
                issue_details_content_2 = 'Wrongly classified as DG'
                issue_details_content_3 = 'Open case with Seller Support with attachment'
                issue_details_content_4 = 'Unable to assist as request is not in their Scope'
                desired_result_line_1 = '1.        ASIN to be resumed to Normal FBA and classified as Non Dangerous Goods (DG)'
                is_apeal_related_doc = 'Yes - Certification Incldued'

                issue_details_content = f"""

                <span><span>1.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;
                </span></span></span><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"> {issue_details_content_1} <br>{issue_details_content_2}
                </span></span></p>

        
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"><span>2.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">{issue_details_content_3} <br>{issue_details_content_4} </span></span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black"><br>
                <br>
                <span> ID – </span>{seller_support_case_id} </span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"></span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
            
                """

                
                related_case_content = f"""
                <span> Seller Support Case ID:  </span>{seller_support_case_id}<span></span></span></p>
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;</span></span></p> """

                    

                html = f"""
                {body}
                <table border="0" cellspacing="0" cellpadding="0" width="777" style="width:583.0pt;border-collapse:collapse">
                <tbody>
                <tr style="height:17.25pt">
                    <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;background:#3b3838;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                        <p><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:white">Issue Submission Email Form</span></b></p>
                    </td>
                    <td width="457" style="width:343.0pt;border:solid #a3a3a3 1.0pt;border-left:none;background:#3b3838;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                        <p><span lang="JA" style="font-size:11.0pt;color:black">&nbsp;</span></p>
                    </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Subject/Headline</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Incorrect DG Classification of ASINs</span></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Merchant Token</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;A31LSP1L7F6XJ2</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Contact Name</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><span style="color:black">Javis Ching</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Seller Email</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt;box-sizing:border-box;word-break:break-word">
                <p><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><a href="mailto:javis.ching@sti-aromas.com" target="_blank">javis.ching@sti-aromas.com</a></span><u><span style="font-family:&quot;Arial&quot;,sans-serif;color:#0563c1"></span></u></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Seller Phone Number</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">+852 56164670</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></p>
                </td>
                </tr>
                <tr style="height:39.75pt">
                <td width="320" style="width:240.0pt;border-top:none;border-left:solid #a3a3a3 1.0pt;border-bottom:none;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:39.75pt">
                
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Issue Details:</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" rowspan="2" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:39.75pt">
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in">

                {issue_details_content}


                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph;text-indent:0in">
                <span>&nbsp;</span></p>
                <p style="margin-left:.5in;text-indent:0in"><span><span style="font-family:&quot;Arial&quot;,sans-serif">&nbsp;</span></span></p>
                <p style="margin-left:.25in;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif">&nbsp;</span></span></p>
                <p style="margin-left:.25in;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif">&nbsp;</span></span></p>
                </td>
                </tr>
                <tr style="height:39.75pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:39.75pt">
                <p><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">What steps/actions have been taken so far?</span></span><span style="font-size:11.0pt;color:black"></span></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">What is your desired result?</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                
                <p style="margin-left:.5in"><span><span><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;
                </span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">{desired_result_line_1}</span></span></p>
                <p style="margin-left:.5in;text-indent:0in"><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;</span></span></p>
                
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in">
                <span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"><span><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;
                </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"> <span>ASIN List: <br>{asin} </span>  </span></span></p>
                <p style="margin-left:.5in;text-indent:0in"><span><span style="font-size:11.0pt">&nbsp;</span></span></p>
                
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Related case(s) (if applicable)</span></b></span><b></b></p>
                </td>

                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                {related_case_content}
                
                </td>
                
                </tr>
                <tr style="height:16.5pt">
                <td width="320" style="width:240.0pt;border-top:none;border-left:solid #a3a3a3 1.0pt;border-bottom:none;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:16.5pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Is the appeal or related documents attached?</span></b></span><b></b></p>
                </td>
                <td width="457" rowspan="2" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:16.5pt">
                <p><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"> {is_apeal_related_doc} </span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"><br>
                </p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">(if applicable)</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></p>
                </td>
                </tr>
                <tr style="height:17.25pt">
                <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"> Account Manager Email </span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
                </td>
                <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
                <p><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><a href="mailto:anramrod@amazon.com" target="_blank"> anramrod@amazon.com </a></span></p>
                </td>
                </tr>
                </tbody>
                </table>
                
                <br><br>
            
                """
                
                return html


            except Exception as e:
                print('Issue in Creating HTML Template ', e)
                self.post.ProcessErrorLog(self, 2, f"  Issue in Creating HTML Template {e}  ")

    def send_email_SAS(self, asin, subject, file_path=None, file = None , seller_support_case_id = None,  sas_manager = False):
        """
            Send email with Wrong Category node
        """
        text_sas_manager = f"""
Hi Andres,\n
Attached the SDS included the air approval certification a for your perusal and review. ASIN: {asin}.\n
Seller Support Case {seller_support_case_id}. Highly appreciated please coordinate with DG team and seek for their approval.\n
Thanks, 
Rebecca
"""
        try:
            today =  date.today()
            #body = "This is an email with attachment sent from Python"
            sender_email = "rebecca.dark@sti-aromas.com"
            
            cc_email = []
            if sas_manager:
                receiver_email = 'anramrod@amazon.com'
                
                cc_email = ['mlopezif@amazon.com', "rebecca.dark@sti-aromas.com", "gaurav.k.gosain@sti-aromas.com", 'lizzypan@sti-aromas.com']
            else:
                receiver_email ="sas-issue-assistance@amazon.com" 
            password = '#Gya12341'
            

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email) if isinstance(receiver_email, list) else receiver_email
            message["Cc"] = ", ".join(cc_email) if isinstance(cc_email, list)  else cc_email
            message["Subject"] = subject

            if sas_manager:
                text = text_sas_manager
                part1 = MIMEText(text, "plain")
                message.attach(part1)
            else:
                email_html = self.generate_email_html( seller_support_case_id, asin  )
                part1 = MIMEText(email_html, "html")
                message.attach(part1)

            ### we SEND THE Images DIR Here containing all the Images
            if file_path:
                for filename in os.listdir(file_path):
                    file_path_dir = os.path.join(file_path, filename)
                    
                    if os.path.isfile(file_path_dir):
                        with open(file_path_dir, 'rb') as attachment:
                            part2 = MIMEBase('application', 'octet-stream')
                            part2.set_payload(attachment.read())
                            encoders.encode_base64(part2)
                            part2.add_header('Content-Disposition', f'attachment; filename={filename}')
                            message.attach(part2)
            else:
                ### We send and attach single file here !
                filename = os.path.basename(file)
                with open(file, 'rb') as attachment:
                    part2 = MIMEBase('application', 'octet-stream')
                    part2.set_payload(attachment.read())
                    encoders.encode_base64(part2)
                    part2.add_header('Content-Disposition', f'attachment; filename= {filename}')
                    message.attach(part2)


                    
            text = message.as_string()
            session = smtplib.SMTP('smtp-legacy.office365.com', 587)
            session.starttls()
            session.login(sender_email, password)
            session.sendmail(sender_email, receiver_email, text)
            session.quit()
            print('Email Sent Successfully\n')
            self.post.ProcessErrorLog(self, 1, " Email Sent Successfully ")
            return subject
        
        except Exception as err:  
            print(" Error Sending  Mail - Wrong Category Node ",str(err)) 
            self.post.ProcessErrorLog(self, 2, f"  Error Send Mail - Wrong Category Node  - SAS_issue_assistance ")
            return False

    def recheck_email_case(self, asin, subject = None ):

        try:
            self._ManualLog = ''
            self.driver.get("https://sellercentral.amazon.com/cu/case-lobby?ref=xx_caselog_count_home")
            sleep(3)
            
            table = self.driver.find_element(by = By.XPATH, value='//*[@role="rowgroup"]')
            tablerows = table.find_elements(by = By.XPATH, value='//*[@role="row"]')
            searchcaseid = tablerows[0].find_element(by = By.XPATH, value='//*[@type="search"]')
            asin = asin 
            searchcaseid.send_keys(asin)#############
            sleep(2)
            searchbtn = tablerows[0].find_elements(by = By.XPATH, value='//*[@label="Go"]')
            searchbtn[0].click()
            sleep(2)
            
            # short_description_texts = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-search-results-panel-shortDescription')
            
            ### Go through all the subjects while searching for the case ID
            creation_date_shown = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-search-results-panel-creationDate')

            
            ### noting down the subject's date time 
            date_str = ' '.join(subject.split('-')[-4:-1]).strip()
            date_obj = datetime.strptime(date_str.strip(), '%Y %m %d')
            date_of_case_id = date_obj.strftime('%B %d, %Y')
            date_of_case_id_obj = datetime.strptime(date_of_case_id, '%B %d, %Y')    
            keyword = "Attached the SDS and safety transportation certification for your reference and perusal"

            ### getting all the rows of subjects for the subject
            all_cases_view_button = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-view-case-button')
            
          
            ### comparsion check where loop through each subject and check which subject's date match with our subject's date
            current_window_handle = self.driver.current_window_handle
            case_id_number = ''
            if all_cases_view_button:
                for view_button_, creation_date in zip(all_cases_view_button, creation_date_shown):
                    timeline_creation_date = creation_date.text.split('at')[0].strip()
                    date_text_obj = datetime.strptime(timeline_creation_date, '%B %d, %Y') 
                    
                    time.sleep(3)
                    if date_text_obj >= date_of_case_id_obj:
                        print(f' For ASIN: {asin} Date of text shown in screen is ', date_text_obj, ' >= ', 'date of case id object', date_of_case_id_obj)
                        view_button_.send_keys(Keys.CONTROL + Keys.RETURN)
                        time.sleep(3)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(5)

                        see_more_buttons = [self.driver.find_elements(By.CLASS_NAME, 'link')[-1]]
                        for button in see_more_buttons:
                            try:
                                if button.text.split('\n')[1].endswith('more'):
                                    self.driver.execute_script("arguments[0].click();", button)
                                time.sleep(2)
                            except Exception as e:
                                print(f"Error clicking 'See More' button: {e}")
                        time.sleep(3)
                       
                        if (keyword in self.driver.page_source )   :
                            print("subject present")
                            case_id_number = [i for i in self.driver.find_elements(By.CLASS_NAME,'text-secondary') if i.text]
                            if case_id_number:
                                case_id_number = case_id_number[0].text.split('ID')[1].strip()
                                print('case_id_number', case_id_number)
                                print(f'Got Case ID - {case_id_number} by Rechecking Email Case\n')
                                self.post.ProcessErrorLog(self, 1, f"Got Case ID - {case_id_number} by Rechecking Email Case ")
                                self.driver.close()
                                self.driver.switch_to.window(current_window_handle)
                                return case_id_number   
                            
                        print('Couldnt find the subject in the view case')
                        print('No case_id_number found matching as no subject found in the body .\n')
                        self.post.ProcessErrorLog(self, 1, 'No case_id_number found matching our scenerios.')
                        self.driver.close()
                        self.driver.switch_to.window(current_window_handle)
                        continue
                    else:
                        print(0)
                        self.driver.switch_to.window(current_window_handle)
                        self.post.ProcessErrorLog(self, 1, f'Time not matched with case id creation and shown  ')
                        print(f'Time not matched with case id creation and shown   ') ### self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                print('No reply from Amazon yet, Date of subject Not presented in Creation Date in portal')
                self.post.ProcessErrorLog(self, 1, 'No reply from Amazon yet, Date of subject Not presented in Creation Date in portal ')
                return False

        except Exception as err:  
            self._ManualLog = ""
            print("Error in Release",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Error in Release email case - recheck_email_case() " + str(err)) 
            return False

    def update_case_id(self, create_data, subject , SAS_IA_Case_ID, multiple_entries_update = False ):
        """
            Updating Email body subject with case id number once we get it from portal
            - By Default = it will update single entry 
            
            - for multiple entries -
                
                list(self.gsheetData_job_log[self.gsheetData_job_log['SAS - IA'].astype(str).str.startswith('DG')]['ASIN'].items())

        """
        try:
                print('\tUpdating  the SAS - IA Subject \n')


                asin = self._ASIN
            
                print(f"Checking Case ID - {subject} in all_cases_table => DG_Appeal_Stage for the ASIN   ")
                self.post.ProcessErrorLog(self,1,f"Checking Case ID - {subject} in all_cases_table => DG_Appeal_Stage for the ASIN   ")
                
                body = self.recheck_email_case(asin, subject)
                
                if not body:
                    print(f"\nAsin {asin} Body not found for the email subject from portal\n")
                    self.post.ProcessErrorLog(self,1,f"Asin {asin} Body not found for the email subject from portal")
                    return False
                
                print(f"Asin {asin} Body found from the email subject from amazon portal, will update the cell.")
                self.post.ProcessErrorLog(self,1,f"Asin {asin} Body found from the email subject")

                data = create_data( SAS_IA_Case_ID = body )
                self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)

                self.post.ProcessErrorLog(self, 1, f'DB entry inserted successfully for asin {asin} for the SAS case ID  ')
                print(f'DB entry inserted successfully for asin {asin} for the SAS case ID   ')
                return body
            
        except:
            self.post.ProcessErrorLog(self,1,'Issue in Updating SAS body email subject')
            self._ManualLog = "Issue in Updating Email body"

    def check_case_status_(self, id ):
        try:
            if not id: print('no id given')
            self.driver.get(f'https://sellercentral.amazon.com/cu/case-dashboard/view-case?ref=sc_cd_lobby_vc_v3&ie=UTF&caseID={id}')
            time.sleep(5)
            reply_btn = self.driver.find_elements(By.CLASS_NAME,'view-case-reply-buttons-container')
            if len(reply_btn) <=0:
                self.case_status_ = 'Cancelled'
                return "Cancelled"
            else:
                self.post.ProcessErrorLog(self, 1, f' Case - its On-going ...');print(f' Case - its On-going ...  ')
                print('')
                self.case_status_ = 'On Going'
                return self.case_status_
        except Exception as e:
            self.post.ProcessErrorLog(self, 1, f'Issue in checking status of the ID  ');print(f'Issue in checking status of the ID')
            return "error"

    def update_form_content(self,asin,   seller_support_case_number ):
        """
            new template is master excel form 
            which will be updated and send for each asin
        """
        try:
            new_template = f"{self.DownloadLocation}SAS_Core_Issue_Assistance_Form_DG_appeal.xlsx"
            wb_source_new_template = xw.Book(new_template)
            sheet_source_new_template = wb_source_new_template.sheets['Sheet1']  

            SAS_CONTENT = ''
            RELATED_CASE_CONTENT = f'Seller Support Case ID: {seller_support_case_number} '
            
            sheet_source_new_template.range('B7').value = f"""
1.    Open case with Seller Support
Unable to assist as request is not in their Scope

ID - {seller_support_case_number}

{SAS_CONTENT}

"""
        
            sheet_source_new_template.range('B9').value = f"""
1.    Uploaded SDS with Safety Transportation Certification to Amazon system Wrongly classified as DG
2.    Hazard Identification Report also confirms that the ASIN to be resumed to Normal FBA and classified as Non Dangerous Goods (DG) ASIN: {asin} """
        
            sheet_source_new_template.range('B10').value = f"{RELATED_CASE_CONTENT}"

            excel_updated_path = f"{self.asins_directory_path}\\{self._ASIN}_asin_report\\SAS_{asin}_Core_Issue_Assistance_Form_DG_appeal.xlsx"
            wb_source_new_template.save(excel_updated_path)
            wb_source_new_template.app.quit()
        
            return excel_updated_path
        
        except Exception as e:
            print('Issue in Creating Form, will retry later...')
            self.post.ProcessErrorLog(self,1, 'Issue in Creating Form, will retry later... ')
            return False
    
    def inform_users_via_mail(self, subject, body):

        """
            Informing Users via Mail 
        """
        
        today =  date.today()
        sender_email = "rebecca.dark@sti-aromas.com"

        receiver_email = "javis.ching@sti-aromas.com"
        cc_email = ["rebecca.dark@sti-aromas.com", "gaurav.k.gosain@sti-aromas.com", "lizzypan@sti-aromas.com"]
        
        ### Test
        # cc_email = []
        # receiver_email = "gyalabs.it29@gmail.com"
        
        
        password = '#Gya12341'
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Cc"] = ", ".join(cc_email) if isinstance(cc_email, list) else cc_email

        text = body

        message["Subject"] = subject
        part1 = MIMEText(text, "html")
        message.attach(part1)
               
        text = message.as_string()
        session = smtplib.SMTP('smtp-legacy.office365.com', 587)
        session.starttls()
        session.login(sender_email, password)
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
        print('Informed User via email \n')
        self.post.ProcessErrorLog(self, 1, f"  Informed User via email  ")

        return subject

    def getdatafromamazon(self):        

          
        try: 
            self.IsComplete = 0
            self.ID =  self.post.ProcessUpdate(self)   
      
            # self.IDList = self.IDList[20:]
            time.sleep(5)
            for indices, row in self.IDList.iterrows(): 
                
                try:  
                    
                    if ((self.StartDate + timedelta(hours=5)) <  datetime.now()):
                        self.post.ProcessErrorLog(self, 1, "Job Time Over")
                        return       
                            
                    if int(row['Status'])!=0:
                        continue

                    self._ASIN = row['Process_Name']
                    self._ASIN = self._ASIN.strip()
                    """  IF Data not updated, run the merge of self.gsheetData again !!!  -> self.readStageTable(); self.gsheetData = pd.merge(self.StageData, self.masterData, how='left', left_on='Product_ID', right_on='ID')   """
                    # self._ASIN = "B09PRBHZ26"
                    #     time.sleep(3)
                    self.Gsheet_Data_current_row = self.gsheetData[(self.gsheetData['ASIN_x'] == self._ASIN) ]
                    self.Stage_ID = self.Gsheet_Data_current_row["ID_x"].iloc[0]
                    self._PK_ID = self.Gsheet_Data_current_row['Product_ID'].iloc[0]
                    Product_Brand_Name = self.Gsheet_Data_current_row['Product_Name_x'].values[0]
                    self.post.ProcessErrorLog(self, 1, f'Working on Stage ID = {self.Stage_ID} of asin {self._ASIN} ')
                    print(f'Working on Stage ID = {self.Stage_ID}  of asin {self._ASIN}; can check it in Table public."DG_Appeal_Stage" where "ID" = {self.Stage_ID}   ')
                    self.case_status_ = ''
                    

                    timestamp_columns = ['Start_Date', 'End_Date', 'Time_Document_Upload', 
                                         'Time_Final_Document_Upload', 'Time_Upload_Document', 
                                         'Time_Seller_Support_Case', 'Time_SAS_Manager_Final', 'Time_SAS_IA']

                    for column in timestamp_columns:
                        if pd.api.types.is_numeric_dtype(self.Gsheet_Data_current_row[column]):
                            self.Gsheet_Data_current_row[column] = pd.to_datetime(self.Gsheet_Data_current_row[column], unit='ms', errors='coerce').dt.strftime('%Y-%m-%d %H:%M')

                    
                    def get_last_non_null_value(column_name):
                        try:
                            
                            column_series = self.Gsheet_Data_current_row[column_name]

                            last_valid_index = column_series.last_valid_index()

                            if last_valid_index is not None:
                                return column_series[last_valid_index]

                            return None
                        except Exception as e:
                            return None

                    Time_Document_Upload = get_last_non_null_value('Time_Document_Upload')
                    Partial_Document_Upload = get_last_non_null_value('Partial_Document_Upload')
                    
                    Time_Final_Document_Upload = get_last_non_null_value('Time_Final_Document_Upload')
                    Final_Document_Upload = get_last_non_null_value('Final_Document_Upload')                    
                    Final_Document_Validities = get_last_non_null_value('Final_Document_Validities')
                    
                    Time_Upload_Document = get_last_non_null_value('Time_Upload_Document')
                    Upload_Document = get_last_non_null_value('Upload_Document')
                    
                    Time_Seller_Support_Case = get_last_non_null_value('Time_Seller_Support_Case')
                    Seller_Support_Case_ID = get_last_non_null_value('Seller_Support_Case_ID')

                    Time_SAS_IA = get_last_non_null_value('Time_SAS_IA')
                    SAS_IA_Subject = get_last_non_null_value('SAS_IA_Subject')
                    SAS_IA_Case_ID = get_last_non_null_value('SAS_IA_Case_ID')

                    Time_SAS_Manager_Final = get_last_non_null_value('Time_SAS_Manager_Final')
                    SAS_Manager_Subject_Final = get_last_non_null_value('SAS_Manager_Subject_Final')
                    SAS_Manager_Case_ID_Final = get_last_non_null_value('SAS_Manager_Case_ID_Final')

                    result_ = None

                    current_date = datetime.now()
                    
                    if not Partial_Document_Upload:
                        self.missing_MSDS_file_asins.append(self._ASIN)
                    else:
                        ### MSDS validity upto 2 years
                        if Time_Document_Upload:
                            date_string = Time_Document_Upload
                            date_format = '%Y-%m-%d %H:%M'
                            date_object = datetime.strptime(date_string, date_format)
                            two_year_ago = current_date - timedelta(days=730)
                            if date_object < two_year_ago:
                                print("The date of the file is 1 year ago, Thus expired. informing the team.")
                                self.post.ProcessErrorLog(self, 1, 'The date of the file is 1 year ago, Thus expired. informing the team.')
                                self.asins_MSDS_expired.append(self._ASIN)


                    if not Final_Document_Upload :
                        self.missing_MSDS_Lab_Report_file_asins.append(self._ASIN)
                    
                    else:                        
                        ### Lab Report & MSDS validity upto 1 year
                        if Time_Final_Document_Upload:
                            date_string = Time_Final_Document_Upload
                            date_format = '%Y-%m-%d %H:%M'
                            date_object = datetime.strptime(date_string, date_format)
                            one_year_ago = current_date - timedelta(days=365)
                            if date_object < one_year_ago:
                                print("The date of the file is 1 year ago, Thus expired. informing the team.")
                                self.post.ProcessErrorLog(self, 1, 'The date of the file is 1 year ago, Thus expired. informing the team.')
                                self.asins_Lab_expired.append(self._ASIN)
                        
                            
                    
                    
                    stage_number = 0
                    first_stage = [ Upload_Document , Seller_Support_Case_ID]
                    second_stage = [  SAS_IA_Subject ]
                    third_stage = [ SAS_Manager_Subject_Final ]

                    if all(stage for stage in first_stage):
                        stage_number = 1
                    if all(stage  for stage in second_stage):
                        stage_number = 2
                    if all(stage for stage in third_stage):
                        stage_number = 3
                    

                    			
           
                        
                    initial_date = Time_Seller_Support_Case
                    if  initial_date:
                        
                        start_date_asin = datetime.strptime(initial_date, '%Y-%m-%d %H:%M') 
                        days_difference = str((datetime.now() - start_date_asin).days)
                        days_difference = '1' if days_difference == "0" else days_difference
                    else:
                        days_difference = '1'

                    if self._ASIN in self.Non_DG_Products:
                        
                        
                        case_id_number = None
                        if SAS_IA_Subject and not SAS_IA_Case_ID:
                            case_id_number = self.update_case_id(create_data ,SAS_IA_Subject, SAS_IA_Case_ID)
                        
                        ### Checking current Status of SAS Case ID
                        if SAS_IA_Case_ID or case_id_number:
                            SAS_IA_Case_ID = SAS_IA_Case_ID or case_id_number
                            try:
                                SAS_IA_Case_ID = int(SAS_IA_Case_ID)
                                result = self.check_case_status_(SAS_IA_Case_ID)
                                if result == 'error':
                                    self.post.ProcessErrorLog(self, 1, f'Result of checking case status not confirmed, will check later in next run...  ')
                                    print(f'Result of checking case status not confirmed, will check later in next run...   ')
                                    continue
                                print('result__Case_status  = \t', self.case_status_)
                                self.post.ProcessErrorLog(self, 1, f'Result of case id is {self.case_status_} ')
                                print(f'Result of case id is {self.case_status_}  ')
                            except Exception as e:
                                print('SAS IA ID is not int yet will check later...')
                                self.post.ProcessErrorLog(self, 1, f'SAS IA - ID is not int yet will check later..  ')
                    
                        
                        self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} has been removed from the Status of DG , converted to NON Dg as its not found it the current list of amazon portal ')
                        print(f'ASIN {self._ASIN} has been removed from the Status of DG , converted to NON Dg as its not found it the current list of amazon portal  ')


                        data = {    
                            'DG_Class': "Non DG",
                            'Job_Log_ID': self.ID,
                            "Monitor_Status": 'Completed',
                            'Stage': stage_number,
                            }
                        
                        if self.Gsheet_Data_current_row["Monitor_Status"].iloc[0] != "Completed":
                            data['Days'] = days_difference 
                        
                        ID__ =  self.insert_update_data_Stage_(data, Status = 1)
                        
                        print(f'Non Dangerous Goods asin {self._ASIN}  marked,  proceeding ahead with other asins')
                        self.post.ProcessErrorLog(self, 1, f'Dangerous Goods asin {self._ASIN} marked, proceeding ahead with other asins')
                   
                        
                        row['Status']=1
                        row['Process_Log']= '' 
                        self.updateRPAProcessLog(row)
                        continue
                    
                    
                    # brand_names = ['KUKKA', 'Gya Tea', 'Gya Labs', 'H`ana']
                    # def extract_brand_and_product(product_brand_name, brand_names):
                    #     for brand_name in brand_names:
                    #         pattern = re.compile(f'\\b{re.escape(brand_name)}\\b', flags=re.IGNORECASE)
                    #         if re.search(pattern, product_brand_name):
                    #             brand = brand_name
                    #             product = re.sub(pattern, '', product_brand_name).strip()
                    #             return brand, product
                    #     return None, product_brand_name
                    # brand, Product = extract_brand_and_product(Product_Brand_Name, brand_names)
                    # print(f'\nProduct Name: {Product}')
                    # print(f'Brand Name: {brand}')



                    self.post.ProcessErrorLog(self, 1, f' ASIN {self._ASIN} yet to be converted to NON DG, current status = DG  ')
                    print(f'ASIN {self._ASIN} yet to be converted to NON DG, current status = DG   ')
                    self.post.ProcessErrorLog(self, 1, f'Going for asin {self._ASIN}  ');print(f'\nGoing for asin {self._ASIN} \n ')
                    
                    
                    ### dict for create_data method
                    def create_data(**kwargs):
                        data = {}
                        data["Monitor_Status" ] = 'On Going'
                        data['Days'] = days_difference
                        data["DG_Class"] = 'DG'
                        for key, value in kwargs.items():
                            data[key] = value
                        return data

                    ### Storing The file in local Directory
                    result_file_found_path = None

                    def file_found_path():
                        
                        file_found = False      

                        if  Partial_Document_Upload or Final_Document_Upload :
                            
                            name_file = None
                            if Final_Document_Upload:
                                self.final_name_file = f"{self._ASIN}_F.pdf"
                                name_file = f"{self._ASIN}_F.pdf"
                            else:
                                name_file = f"{self._ASIN}_P.pdf"
                            
                            self.post.ProcessErrorLog(self, 1, f' File status of asin {self._ASIN} is marked True, file is found  ')
                            print(f'File status of asin {self._ASIN} is marked True, file is found   ')
                            
                            
                            self.post.ProcessErrorLog(self, 1, f'In master sheet, Lab report status is marked Yes, lets check for the file ');print(f'In master sheet, Lab report status is marked Yes, lets check for the file  ')
                            
                            try:
                                if not os.path.exists(self.asins_directory_path+f'\\{self._ASIN}_asin_report'):
                                    os.makedirs(self.asins_directory_path+f'\\{self._ASIN}_asin_report')

                                _FileName = f"http://20.124.105.108/static/assets/media/DG_appeal/{name_file}"
                                time.sleep(0.5) 
                                file_found = urllib.request.urlretrieve(_FileName , os.path.join(self.asins_directory_path+f'\\{self._ASIN}_asin_report', name_file)  )
                                file_found = file_found[0]
                                self.post.ProcessErrorLog(self, 1, f'File Found !')
                                print(f'File Found ! {file_found} ')

                                time.sleep(3)

                                 
                                if file_found:
                                    self.post.ProcessErrorLog(self, 1, f'DG Lab Report File found for Asin {self._ASIN} '); 
                                    print(f'DG Lab Report File found for Asin {self._ASIN} ')
                                    return os.path.join(self.asins_directory_path+f'\\{self._ASIN}_asin_report', name_file)  
                                else:
                                    self.post.ProcessErrorLog(self, 1, f'File not present in drive ');print(f'\nFile not present in drive  ')
                                    return False
                                

                            except Exception as e: 
                                self.post.ProcessErrorLog(self, 1, f'Lab Report File not found for the asin {self._ASIN} | Error: {e}')
                                print(f'Lab Report File not found for the asin {self._ASIN} | Error: {e}')
                                return False

                        else:
                            self.post.ProcessErrorLog(self, 1, f'File not Marked "Yes" in master sheet, Thus, Wont find it in drive ')
                            print(f'File not Marked "Yes" in master sheet, Thus, Wont find it in drive   ')
                            self.post.ProcessErrorLog(self, 1, f'File not marked True in any of the columns Partial or Final  !  ');print(f'File not marked True in any of the columns Partial or Final  !   ')
                       
                
                    result_file_found_path = file_found_path()
                    parent_directory = os.path.dirname(result_file_found_path) if result_file_found_path else None

                   
                    ### Upload Documents with both Partial and Final Case
                    Document_ = None
                    Document_Type = None

                    
                      

                    if Final_Document_Upload:
                        
                        Document_ = Final_Document_Upload
                        Document_Type = 'Final'
                        Subject_Context = "MSDS & Lab Report"

                        if not Upload_Document or str(Upload_Document).startswith('Partial') :
                            
                            print(f"Uploading {Document_Type} Document")
                            self.post.ProcessErrorLog(self, 1, f'Uploading {Document_Type} Document')
                            
                            result = self.upload_document(result_file_found_path)
                            
                            if result: 

                                print(f'Uploaded Document - {Document_} ')
                                self.post.ProcessErrorLog(self, 1, f'Uploaded Document - {Document_} ')

                                data = create_data(Time_Upload_Document = datetime.today().strftime("%Y-%m-%d"), 
                                                   Upload_Document = Document_Type + '_Uploaded' )
                                result_ = self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)
                                self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for Final Upload , {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for Final Upload , {str(result_)} for ASIN {self._ASIN} ')
                                time.sleep(2)
                                
                                print('Document Uploaded Succesfully, loggin in DB')
                                self.post.ProcessErrorLog(self, 1, f' Document Logged in DB successfully  ')

                            else: 
                                self.post.ProcessErrorLog(self, 1, f'Document Failed - {Document_} -  couldnt Upload it, as result of upload_document method failed')
                                print(f"Document Failed - {Document_} -  couldnt Upload it, as result of upload_document method failed")
                        else:
                            self.post.ProcessErrorLog(self, 1, f'Document Already - {Document_Type}  exists')
                            print(f"Document Already - {Document_Type}  exists")
                                         
                    elif Partial_Document_Upload:
                        Document_ = Partial_Document_Upload
                        Document_Type = 'Partial'
                        Subject_Context = "MSDS"
                        if not Upload_Document:
                            
                            print(f"\nUploading {Document_Type} Document")
                            self.post.ProcessErrorLog(self, 1, f'Uploading {Document_Type} Document')

                            result = self.upload_document(result_file_found_path)
                            
                            if result: 
                                print(f'Uploaded Document - {Document_} ')
                                self.post.ProcessErrorLog(self, 1, f'Document {Document_} Uploaded')

                                data = create_data(Time_Upload_Document = datetime.today().strftime("%Y-%m-%d"), Upload_Document = Document_Type + '_Uploaded' )
                                result_ = self.insert_update_data_Stage_(data , asin = self._ASIN, Status = 1)
                                Upload_Document = True
                                self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for Partial Upload , {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for Partial Upload , {str(result_)} for ASIN {self._ASIN} ')
                                
                                print('Document Uploaded Succesfully, loggin in DB  | | Upload Document Stage 1 clear ')
                                self.post.ProcessErrorLog(self, 1, f' Document Logged in DB successfully  | | Upload Document Stage 1 clear   ')
                            
                            else: 
                                self.post.ProcessErrorLog(self, 1, f'Document Failed - {Document_} -  couldnt Upload it, as result of upload_document method failed')
                                print(f'Document Failed - {Document_} -  couldnt Upload it, as result of upload_document method failed')
                        
                        else:
                            print(f"Previously Document - {Document_Type} exists in Amazon portal |  | Upload Document Stage 1 clear")
                            self.post.ProcessErrorLog(self, 1, f'Previously Document {Document_Type} exists in Amazon portal |  | Upload Document Stage 1 clear  ')    
                    
                    else:
                        print("No document to upload\n")
                        self.post.ProcessErrorLog(self, 1, f' No document exists to upload for the ASIN ')
                    
                    _Seller_Support_Case_ID_ = None
                    

                    ### Seller support Case either with  Partial or Final Document
                    if result_file_found_path:
                        if not Seller_Support_Case_ID or Seller_Support_Case_ID.startswith("Failed") and  Upload_Document    :
                                                            
                            self.post.ProcessErrorLog(self, 1, 'Immediately Starting with Seller Support Case ')
                            print('Immediately Starting with Seller Support Case\n')
                            
                            subject = f'DG Appeal - {Subject_Context} - {Product_Brand_Name} - {self._ASIN} - {datetime.today().strftime("%Y-%m-%d")} - SS'
                            print("Subject\t", subject)
                            _Seller_Support_Case_ID_ = self.seller_support_case(self._ASIN , file_path = result_file_found_path ,
                                                                            report_type = Document_Type, subject = subject )   
                            
                            data = create_data(Time_Seller_Support_Case = datetime.today().strftime("%Y-%m-%d"), 
                                            Seller_Support_Case_ID = _Seller_Support_Case_ID_ 
                                            if _Seller_Support_Case_ID_ else 'Failed_'+str(subject))
                            Seller_Support_Case_ID = _Seller_Support_Case_ID_
                            result_ = self.insert_update_data_Stage_(data , asin = self._ASIN, Status = 1)
                            self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for Seller support case , {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for Seller support case , {str(result_)} for ASIN {self._ASIN} ')
                            
                            self.post.ProcessErrorLog(self, 1, f'Got the Seller Support Case ID - {_Seller_Support_Case_ID_}, will use it to send SAS cases | | Stage 2.1 Cleared  ')
                            print(f'Got the Seller Support Case ID - {_Seller_Support_Case_ID_}, will use it to send SAS cases | | Stage 2.1 Cleared \n')
                        else:
                            self.post.ProcessErrorLog(self, 1, f'Seller Support case ID already created for asin {self._ASIN} - {Seller_Support_Case_ID}'    )
                            print(f'Seller Support case ID already created for asin {self._ASIN} - {Seller_Support_Case_ID} '   ) 
                            _Seller_Support_Case_ID_ = Seller_Support_Case_ID            
                    else:
                        self.post.ProcessErrorLog(self, 1, f'No partial or final file found with the ASIN...  ');print(f'No partial or final file found with the ASIN...  ')
                    
                    case_id_number = None
                    if SAS_IA_Subject and not SAS_IA_Case_ID:
                        case_id_number = self.update_case_id(create_data ,SAS_IA_Subject, SAS_IA_Case_ID)

                    ### Checking current Status of SAS Case ID
                    if SAS_IA_Case_ID or case_id_number:
                        SAS_IA_Case_ID = SAS_IA_Case_ID or case_id_number
                        try:
                            SAS_IA_Case_ID = int(SAS_IA_Case_ID)
                            result = self.check_case_status_(SAS_IA_Case_ID)
                            if result == 'error':
                                self.post.ProcessErrorLog(self, 1, f'Result of checking case status not confirmed, will check later in next run...  ')
                                print(f'Result of checking case status not confirmed, will check later in next run...   ')
                                continue
                            print('result__Case_status  = \t', self.case_status_)
                            self.post.ProcessErrorLog(self, 1, f'Result of case id is {self.case_status_} ')
                            print(f'Result of case id is {self.case_status_}  ')
                        except Exception as e:
                            print('SAS IA ID is not int yet will check later...')
                            self.post.ProcessErrorLog(self, 1, f'SAS IA - ID is not int yet will check later..  ')
                     


                    if result_file_found_path  and _Seller_Support_Case_ID_ and Seller_Support_Case_ID and not _Seller_Support_Case_ID_.startswith('Failed')  :
                        
                        if len(os.listdir(self.asins_directory_path+f'\\{self._ASIN}_asin_report')) >= 1:
                            

                            if not SAS_IA_Subject   :
                                
                                excel_file_path = self.update_form_content(self._ASIN,  _Seller_Support_Case_ID_   )

                                if excel_file_path:

                                    self.post.ProcessErrorLog(self, 1, 'Immediately Starting with SAS-IA Case ')
                                    print('Immediately Starting with SAS-IA Case\n')
                                    
                                    subject = f'DG Appeal - {Subject_Context} - {Product_Brand_Name} - {self._ASIN} - {datetime.today().strftime("%Y-%m-%d")} - IA'                          
                                    result_of_email = self.send_email_SAS(self._ASIN, subject, file_path = self.asins_directory_path+f'\\{self._ASIN}_asin_report', 
                                                        seller_support_case_id = _Seller_Support_Case_ID_ )
                                    time.sleep(1.5)    

                                    if result_of_email:
                                        
                                        data = create_data( Time_SAS_IA = datetime.today().strftime("%Y-%m-%d") , SAS_IA_Subject = subject )
                                        result_ = self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)
                                        self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for MSDS SAS - IA, {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for MSDS SAS - IA, {str(result_)} for ASIN {self._ASIN} ')
                                        SAS_IA_Subject = subject
                                        print(f'Created and sent the SAS Case as for the ASIN {self._ASIN} | | Stage 2.2 Sending SAS - IA cleared !! ')
                                        self.post.ProcessErrorLog(self, 1, f"Created and sent the SAS Case as for the ASIN {self._ASIN} | | Stage 2.2 Sending SAS - IA cleared  ")
                                    
                                    else:

                                        self._ManualLog = 'Failed SAS-IA'
                                        data = create_data( Time_SAS_IA = datetime.today().strftime("%Y-%m-%d") , SAS_IA_Subject = subject, SAS_IA_Case_ID = self._ManualLog )
                                        self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)

                                        print(f"Issue in Sending SAS-IA for asin {self._ASIN} !!  ")
                                        self.post.ProcessErrorLog(self, 2, f"RPA Issue in Sending SAS for asin {self._ASIN}  ")
                                
                                else:
                                    self.post.ProcessErrorLog(self, 1, f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path !! ")  
                                    print(f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path")
                            
                            ###  Re-SEND SAS-IA-case after 48 hours if no reply
                            if not self.case_status_ and SAS_IA_Subject and Time_SAS_IA:
                                
                                time_last_sas_sent = datetime.strptime ( Time_SAS_IA , '%Y-%m-%d %H:%M')  
                                current_datetime = datetime.now()
                                time_difference = current_datetime -  time_last_sas_sent
                                threshold = timedelta(hours = 48)
                                re_send_condition = time_difference > threshold  

                                if re_send_condition:
                                    
                                    self.post.ProcessErrorLog(self, 1, 'Time difference Exceeded Threshold of 24 hours from the previous SAS,  Again Creating SAS for the same. ')
                                    print('Time difference Exceeded Threshold of 24 hours from the previous SAS,  Again Creating SAS for the same.')    

                                    excel_file_path = self.update_form_content(self._ASIN,  _Seller_Support_Case_ID_   )
                                    if excel_file_path:

                                        self.post.ProcessErrorLog(self, 1, 'Re-send SAS-IA Case ')
                                        print('Re-send SAS-IA Case\n')
                                        
                                        subject = f'DG Appeal - {Subject_Context} - {Product_Brand_Name} - {self._ASIN} - {datetime.today().strftime("%Y-%m-%d")} - IA'                          
                                        result_of_email = self.send_email_SAS(self._ASIN, subject, file_path = self.asins_directory_path+f'\\{self._ASIN}_asin_report', 
                                                            seller_support_case_id = _Seller_Support_Case_ID_ )
                                        time.sleep(1.5)    

                                        if result_of_email:
                                            
                                            data = create_data( Time_SAS_IA = datetime.today().strftime("%Y-%m-%d") , SAS_IA_Subject = subject )
                                            result_ = self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)
                                            self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for MSDS SAS - IA, {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for MSDS SAS - IA, {str(result_)} for ASIN {self._ASIN} ')
                                            
                                            print(f'Created and sent the SAS Case as for the ASIN {self._ASIN} | | Stage 2.2 Sending SAS - IA cleared !! ')
                                            self.post.ProcessErrorLog(self, 1, f"Created and sent the SAS Case as for the ASIN {self._ASIN} | | Stage 2.2 Sending SAS - IA cleared  ")
                                        
                                        else:

                                            self._ManualLog = 'Failed SAS-IA'

                                            print(f"Issue in Re-send Sending SAS-IA for asin {self._ASIN} !!  ")
                                            self.post.ProcessErrorLog(self, 2, f"RPA Issue in Re-send Sending SAS for asin {self._ASIN}  ")
                                    
                                    else:
                                        self.post.ProcessErrorLog(self, 1, f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path !! ")  
                                        print(f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path")

                                else:
                                    self.post.ProcessErrorLog(self, 1, 'Time difference of resending SAS  case not exceeded yet! ')
                                    print('Time difference of resending SAS  case not exceeded yet!\n')    
                                
                            ### SAS MANAGER FINAL DOCUMENT - Sending Mail to with seller support case ID and final document upload file 
                            if Final_Document_Upload and  not SAS_Manager_Subject_Final  and self.final_name_file  :
                                

                                self.post.ProcessErrorLog(self, 1, 'Immediately Starting with SAS-Manager Final Case ')
                                print('Immediately Starting with SAS-Manager Final Case\n')
                                try:
                                    final_file = [os.path.join(parent_directory, i)  for i in os.listdir(parent_directory) if i.endswith('_F.pdf')][0]
                                except:
                                    return 'File issue, check if final MSDS file exists'

                                subject = f'DG Appeal - SAS Manager - {Subject_Context} - {Product_Brand_Name} - {self._ASIN} - {datetime.today().strftime("%Y-%m-%d")}'
                                result_of_email = self.send_email_SAS(self._ASIN, subject, file = final_file, 
                                                    seller_support_case_id = _Seller_Support_Case_ID_, sas_manager = True )
                                time.sleep(1.5)    
                                if result_of_email:
                                    SAS_Manager_Subject_Final = subject
                                    data = create_data(Time_SAS_Manager_Final = datetime.today().strftime("%Y-%m-%d"), 
                                                    SAS_Manager_Subject_Final = subject, SAS_Manager_Case_ID_Final = _Seller_Support_Case_ID_ )
                                    result_ = self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)
                                    self.post.ProcessErrorLog(self, 1, f'DB Updated successfully for Final Lab Report SAS - IA,  {str(result_)} for ASIN {self._ASIN}');print(f'DB Updated successfully for Final Lab Report SAS - IA,  {str(result_)} for ASIN {self._ASIN} ')
                                    
                                    print(f'SAS - Manager Case sent as for FINAL DOCUMENT for the ASIN {self._ASIN} | | Stage 3 Sending SAS - Manager Partial cleared !!')
                                    self.post.ProcessErrorLog(self, 2, f' SAS - Manager Case sent as for FINAL DOCUMENT for the ASIN {self._ASIN} | | Stage 3 Sending SAS - Manager Partial cleared !! ')
                            
                                else:

                                    self._ManualLog = 'Failed SAS-Manager FINAL'
                                    self.post.ProcessErrorLog(self, 2, f' SAS - Manager Case FAILED  for the ASIN {self._ASIN} ')
                                    print(f'SAS - Manager Case FAILED  for the ASIN {self._ASIN} !! ')
                        
                        else:
                            self.post.ProcessErrorLog(self, 1, f'Documents not found, wont be proceeding ahead  ');print(f'Documents not found, wont be proceeding ahead  ')
                    
                    print("SAS-IA Email Subject", SAS_IA_Subject, "SAS-IA Case_ID", SAS_IA_Case_ID)
                    stage_number = 0
                    first_stage = [ Upload_Document , Seller_Support_Case_ID]
                    second_stage = [  SAS_IA_Subject ]
                    third_stage = [ SAS_Manager_Subject_Final ]

                    if all(stage for stage in first_stage):
                        stage_number = 1
                    if all(stage  for stage in second_stage):
                        stage_number = 2
                    if all(stage for stage in third_stage):
                        stage_number = 3


                    self.post.ProcessErrorLog(self, 1, f"RPA Job LOG Sheet updated for ASIN {self._ASIN}  ")
                    print(f'RPA Job LOG Sheet updated for ASIN {self._ASIN} ')
                    data = create_data( Days = days_difference , Stage = stage_number)
                    data['Days'] = data['Days'][0] if isinstance(data.get('Days'), (list, tuple)) and data['Days'] else data['Days']
                    self.insert_update_data_Stage_(data, asin = self._ASIN, Status = 1)
                    time.sleep(1)
                    row['Status']=1
                    row['Process_Log']= '' 
                    self.updateRPAProcessLog(row)
                    print("Complete", self._ASIN) 
                    print('Current Case of the ASIN\n', self.StageData[self.StageData['ID'] == self.Stage_ID].values)
                except Exception as err: 
                    print("Exception  ", self._ASIN, str(err)) 
                    time.sleep(2)
                    row['Status']=2
                    row['Process_Log']= str(err)
                    self.updateRPAProcessLog(row)   
                    self.post.ProcessErrorLog(self, 1, "Exception " + self._ASIN +' ' + str(err) )
                    self._ManualLog = "ERROR" + str(err)
                    country_list=['US']
           
            
            ### Send consildated mail for all missing MSDS report
            if (self.missing_MSDS_file_asins  or self.missing_MSDS_Lab_Report_file_asins) and datetime.now().weekday() == 0:
                
                starting_body = f"""
                    <div> <br>
                    Hi Javis,
                    <br><br>
                    These ASINs are missing MSDS & Lab Reports <br><br>
                    </div> """
                
                ending_body = f"""
                    <div> <br><br>
                    Would appreciate, if you can please help with the Lab Reports and 
                    upload the same in the DG Appeal System
                    <br><br>
                    Link to DG Appeal System - http://20.124.105.108/dgappeal/<br>

                    Thanks                     
                    <br><br> </div>"""
          
                def generate_email_html_user_info(msds_missing_list, lab_report_missing_list, gsheetData):
                    """
                    Generates an HTML table with the missing MSDS and Lab Report information for each ASIN.

                    Args:
                        msds_missing_list: A list of ASINs that are missing MSDS information.
                        lab_report_missing_list: A list of ASINs that are missing Lab Report information.
                        gsheetData: A pandas dataframe containing relevant product information.

                    Returns:
                        The generated HTML string.
                    """

                    combined_asin_dict = {asin: [False, False] for asin in set(msds_missing_list + lab_report_missing_list)}
                    for asin in msds_missing_list:
                        combined_asin_dict[asin][0] = True
                    for asin in lab_report_missing_list:
                        combined_asin_dict[asin][1] = True

                    bg = 'background-color: yellow;'

                    l_template = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Dangerous Goods Issue Assistance</title>
                        <style>
                            table th {{
                            {bg}
                            }}
                        </style>
                        </head>
                        <body>
                        {starting_body}
                        <table border="1">
                            <tr>
                            <th>Sr.No</th>
                            <th>ASINs</th>
                            <th>Product Name</th>
                            <th>MSDS</th>
                            <th>MSDS & Lab Report</th>
                            </tr>
                            {"".join([
                            f"<tr>"
                            f"<td>{i+1}</td>"
                            f"<td>{asin}</td>"
                            f"<td>{gsheetData[(gsheetData['ASIN_x'] == asin)]['Product_Name_x'].values[0] if asin in gsheetData['ASIN_x'].values else ''}</td>"
                            f"<td>{'Required' if status[0] else ''}</td>"
                            f"<td>{'Required' if status[1] else ''}</td>"
                            f"</tr>"
                            for i, (asin, status) in enumerate(combined_asin_dict.items())
                            ])}
                        </table>
                        {ending_body}
                        </body>
                        </html>
                        """

                    return l_template

                
                html = generate_email_html_user_info(
                    self.missing_MSDS_file_asins, self.missing_MSDS_Lab_Report_file_asins, self.gsheetData
                )


                self.inform_users_via_mail(f"DG Appeal: Unavailable MSDS & Lab Report for ASINs", html )

            print("getdatafromamazon","ASIN VL prepared successfully!")   
            self.post.ProcessErrorLog(self, 1, "Processed Sucessfully")

            self.IsComplete = 1

            self.ID =  self.post.ProcessUpdate(self ) 

        except Exception as err:  
            print("getdatafromamazonlast",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Processing failed in complete code " + str(err))

    def updateRPAProcessLog(self, row):        
        self.PLID = int(row['ID']) 
        self.Status = int(row['Status'])
        self.ProcessLog = str(row['Process_Log']).replace("'","''") 
        self.post.ProcessLogUpdate(self)
    
    def sendmessage(self):     
        try:
            
            self.body=''   
            if self.gsheetUpdate == None  :
                self.updategooglesheet(1,0)   
            
            gsheetRows = self.gsheetUpdate.get_all_records()
            gsheetRows = pd.DataFrame.from_dict(gsheetRows)
            gsheetRows['Date'] = pd.to_datetime(gsheetRows['Date']).dt.date

            gsheetRowsTmp = gsheetRows[gsheetRows['Job ID']==self.ID]
            
            df = pd.DataFrame(columns=["Date"])
            start_date =  min(gsheetRows['Date']) 
            end_date = max(gsheetRows['Date'])
            delta = timedelta(days=1)
            while start_date <= end_date:
                #df = df.append({'Date': start_date.strftime("%Y-%m-%d")}, ignore_index = True)
                rowdata = {'Date': start_date.strftime("%Y-%m-%d")}
                df = pd.concat([pd.DataFrame([rowdata], columns=df.columns), df], ignore_index=True)
                start_date += delta

            df['Date'] = pd.to_datetime(df['Date'])
            df  = df[df['Date'].isin(gsheetRows['Date'])]


            gsheetGroup = gsheetRows.groupby(["Country","ASIN"])
            for row in gsheetGroup:
                #print(row[0][0], row[0][1])
                tmp =  gsheetRows[(gsheetRows['Country']==row[0][0]) & (gsheetRows['ASIN']==row[0][1])]
                _max = df[~df['Date'].isin(tmp['Date'])]
                if len(_max)>0 :
                    _max = max(df[~df['Date'].isin(tmp['Date'])]['Date'])
                else:
                    _max = (datetime.today()).strftime('%Y-%m-%d')

                gsheetRows.loc[(gsheetRows['Country']==row[0][0]) & (gsheetRows['ASIN']==row[0][1]),'Start'] = _max
                

            gsheetRows = gsheetRows.groupby(["Country","ASIN","Product Name"]).agg({'Date': ['max'],'Start': ['max']}).reset_index()
            gsheetRows['Days'] = (pd.to_datetime(gsheetRows['Date']['max']).dt.date - (pd.to_datetime(gsheetRows['Start']['max']).dt.date + timedelta( days=1)))/np.timedelta64(1, 'D') 
            gsheetRows['Days']= gsheetRows['Days'].astype(int)
            gsheetRows = gsheetRows[gsheetRows['Days']>7]
         
            
            if len(gsheetRows)==0:
                self.post.ProcessErrorLog(self, 1, "Slack 0 Message Sucessfully")
                return True


            self.body="\nHi <@UTY9FNURE>,\nCategory Node ASIN's mismatched on Amazon\n\n"
            self.body= self.body + "Require your manual intervention for Mismatched ASIN's count : " + str(len(gsheetRows)) + "\n\n"
            for indices, row in gsheetRows.iterrows(): 
                if row['Country'][0]==1:
                    text = '<' + 'https://www.amazon.com/dp/' + str(row['ASIN'][0]) + '|' + 'US' + ' | ' + str(row['ASIN'][0]) + ' | ' + str(row['Product Name'][0]) + ' | '  + str(row['Days'][0])   + " days >\n"  
                elif row['Country'][0]==4:    
                    text = '<' + 'https://www.amazon.de/dp/' + str(row['ASIN'][0]) + '|' + 'DE' + ' | ' + str(row['ASIN'][0]) + ' | ' + str(row['Product Name'][0]) + ' | '  + str(row['Days'][0])   + " days >\n"  
                elif row['Country'][0]==5:    
                    text = '<' + 'https://www.amazon.co.uk/dp/' + str(row['ASIN'][0]) + '|' + 'UK' + ' | ' + str(row['ASIN'][0]) + ' | ' + str(row['Product Name'][0]) + ' | '  + str(row['Days'][0])   + " days >\n"  
                self.body = self.body + text

            self.body = self.body + "\n\nSystem Generated Messages\n\n\n"    
            
   
            if self.body !="":
                self.post.body = self.body
                #self.post.body = "This is Test message ignore \n" + self.body
                self.post.sendslackmessage()




            _Auto = gsheetRowsTmp[gsheetRowsTmp['Automatic ID'].apply(str).str.contains("Error")==True]
            _Manual = gsheetRowsTmp[gsheetRowsTmp['Manual ID'].apply(str).str.contains("Error")==True]
            if  len(_Auto)>=5 or len(_Manual)>=5:
                self.body="\nHi <@U02EJQ1U36V>, <@U01DANSBRT5>, <@U03MS1S5HFY>\nCategory Node ASIN's Error on Amazon\n\n"
                self.body= self.body + "Require your manual intervention for Cases \n\n"
                if len(_Auto)>=5:
                    self.body= self.body + "Error on  Automatic Cases \n"

                if len(_Manual)>=5:
                    self.body= self.body + "Error on  Manual Cases \n"

                self.body = self.body + "\n\nSystem Generated Messages\n\n\n"  
                self.post.body = self.body
                self.post.sendslackmessage()


            self.post.ProcessErrorLog(self, 1, "Slack Message Sucessfully")
            return True
        except Exception as err:  
            print(err)
            self.post.ProcessErrorLog(self, 2, "Slack Message " + str(err)) 
            return False

    def signout(self):
        try:
            time.sleep(2)
            self.driver.get('https://advertising.amazon.com/cm/campaigns?entityId=ENTITY1TUNS1T5BI3UY')
            time.sleep(5)
            x = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="topBar"]/div[3]/span[4]/button')))
            x.click()
            time.sleep(2)
            x = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="AACChromePortal"]/div/div[2]/div/div/div/div[7]/a')))
            x.click()
            self.post.ProcessErrorLog(self, 1, "Signout Sucessfully")
        except Exception as err:  
            self.driver.get('https://www.amazon.com/ap/signin')
            self.post.ProcessErrorLog(self, 2, "Signout " + str(err))

    def CountryURL(self, _CountryID):
        #return ["https://www.amazon.com/dp/","https://www.amazon.com/dp/"]
        if _CountryID ==1:
            return ["https://www.amazon.com/dp/","https://sellercentral.amazon.com/help/hub/support/describe"]
        elif _CountryID ==2:
            return ["https://www.amazon.ca/dp/","https://advertising.amazon.ca/cm/campaigns?entityId=ENTITY2Z4NIGXQGF8NY"]
        elif _CountryID ==3:    
            return ["https://www.amazon.com.mx/dp/",'']
        elif _CountryID ==4: 
            return ["https://www.amazon.de/dp/","https://sellercentral.amazon.de/help/hub/support/describe"]
        if _CountryID ==5:
            return ["https://www.amazon.co.uk/dp/", "https://sellercentral.amazon.co.uk/help/hub/support/describe"]                    
        else:
            return ""

    def ImageCaptcha(self):        
        time.sleep(1)
        title = self.driver.title
        captcha = self.driver.find_elements(by=By.LINK_TEXT, value='Try different image')
        if title=='Server Busy' or len(captcha)>0:   
            self.driver.refresh()
            time.sleep(1)
            img = self.driver.find_element( by = By.TAG_NAME  ,value= 'img')
            link = img.get_attribute('src')
            captcha = AmazonCaptcha.fromlink(link)
            solution = captcha.solve()
            print(solution)
            elems = self.driver.find_element(by=By.ID, value='captchacharacters')  
            elems.send_keys(solution)
            elems = self.driver.find_element(by=By.TAG_NAME, value='button')    
            elems.click()
            time.sleep(2)
            title = self.driver.title
            captcha =  self.driver.find_elements(by=By.LINK_TEXT, value='Try different image')
            if title=='Server Busy' or len(captcha)>0:
                return True
            else:
                return False 
        else:
           return False 
        
    def ProcessStart(self,CountryID, RPAPID):

 

        try:
            # self.test_final_db()
            CloseCount = 5
            CurrentCount = 0

            self.CountryID= CountryID
            self.ID = RPAPID
            self.IsComplete =0
            self.PLID =0
            self.Status =0
            self.ProcessLog =''
            self.arr = []   
            self.IDList=[]

            print("Amazon Dangerous goods Appeal ", str(CountryID), str (RPAPID))  
           
            
            

            time.sleep(5)
            self.openbrowser(1)                
            time.sleep(5)
            try:
                self.ImageCaptcha()
            except: ...
            time.sleep(5)
            self.filllogin()
            time.sleep(5)
            #self.IDList =  self.IDList[self.IDList['Process_Name'].isin(['1|B075MBKTTY'])]

            
            if self.ID == 0:
                result_loadasin = self.loadASIN()
                if not result_loadasin: return False
            else:
                self.gsheetData = self.readStageTable()
            
            self.IDList = self.post.ProcessLogGetLast(self)

            print("Amazon Dangerous goods Appeal", str(CountryID), str (RPAPID))  
            

            while len(self.IDList.loc[self.IDList['Status']==0]) != 0:
                
                print('Current Count ', str(CurrentCount))            
                
                if CurrentCount == CloseCount:
                    print('App Close')
                    break

                if ((self.StartDate + timedelta(hours=5)) <  datetime.now()):
                    self.post.ProcessErrorLog(self, 1, "Job Time Over")
                    break 


                CurrentCount= CurrentCount + 1



                self.getdatafromamazon()
                time.sleep(5)
                self.signout()
                time.sleep(5)
                self.driver.close()
                self.driver.quit()
                time.sleep(5)
                self.IDList = self.post.ProcessLogGetLast(self)
                time.sleep(60)
            
            if len(self.IDList.loc[self.IDList['Status']==0]) == 0:
                # self.sendmessage()
                ...
     


            self.post.ProcessErrorLog(self, 1, "ProcessStart Sucessfully Completed !")
            
        except Exception as err:  
            print(err)
            self.post.ProcessErrorLog(self, 2, "ProcessStart " + str(err)) 



''' 
Run specific Asins from self.IDList

    CLIENT_SECRET_FILE = 'GoogleCredentials\client_sheet.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://drive.google.com/drive/folders/']
        
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    results = service.files().list(
        q=f"'1mTUSetJb_ZmESRAhv4hgvomDTVyh2bl1' in parents",    
        pageSize=1000, 
        fields="nextPageToken, files(id, name, mimeType, parents, trashed)"
    ).execute()
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload 
    request = service.files().get_media(fileId="1mTUSetJb_ZmESRAhv4hgvomDTVyh2bl1") 
    fh = io.BytesIO() 
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800) 
    done = False
    
    try: 
        # Download the data in chunks 
        while not done: 
            status, done = downloader.next_chunk() 

        fh.seek(0) 
            
        # Write the received data to the file 
        with open(file_name, 'wb') as f: 
            shutil.copyfileobj(fh, f) 

        print("File Downloaded") 
        # Return True if file Downloaded successfully 
        return True
    except: 
        
        # Return False if something went wrong 
        print("Something went wrong.") 
        return False

    
    self.IDList = self.post.ProcessLogGetLast(self)

    ### Specific asins 
    
    my_asin_list =  f"""B09PRD3RX5""".split(',')
    
    self.IDList['Process_Name'] = [i  if index < len(my_asin_list) else '' for index, i in enumerate(my_asin_list)] + [''] * (len(self.IDList) - len(my_asin_list))

    self.IDList.iloc[0]
    self.IDList['Process_Name'].tolist()
    self.IDList = self.IDList[47:]

    ### for multiple asins
    entries  = {num[1]: num[2] for num in self.IDList["Process_Name"].str.split("|")} 
    self.IDList['Process_Name'] = ['1|' + i + f'|{entries.get(i)}' if index < len(my_asin_list) else '' for index, i in enumerate(my_asin_list)] + [''] * (len(self.IDList) - len(my_asin_list))
    
    ### ASINS not marked yes but lab report present

    # get items code from top of it .
    df = self.gsheetData
    asins_with_lab_report = [i.split('.pdf')[0].split('-')[2] for i in items['name']]
    not_marked_yes = df.loc[df['ASIN'].isin(asins_with_lab_report) & (df['Lab Report'] != 'yes'), 'ASIN'].tolist()
    print(not_marked_yes)

'''




