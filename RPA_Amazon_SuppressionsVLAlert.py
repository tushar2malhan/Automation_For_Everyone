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
import os
import io
import sys
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import gspread
from gspread.cell import Cell
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
#from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.keys import Keys
from PostFun import PostFun
import chromedriver_autoinstaller
import pyotp
import autoit
import xlwings as xw
from selenium.webdriver.common.alert import Alert
import numpy as np
import shutil
from time import sleep
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from CommonFun import CommonFun
from amazoncaptcha import AmazonCaptcha
import datetime as dt
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload
import openpyxl
from email.mime.base import MIMEBase
from email import encoders


import psutil
import os


class RPA_Amazon_SuppressionsVLAlert:
       
    def __init__(self):
        self.RPAID = 10
        self.CountryID =0
        self.ID =0
        self.IsComplete =0
        self.PLID =0
        self.Status =0
        self.ProcessLog =''
        self.arr = []   
        self.IDList=[]
        self.body=''
        self.gsheetData=[]
        self.gsheetUpdate= []  
        self.MissingASINs=[]
        self.ExtraASINs=[]
        self.DeleteASINs=[]
        self.ParentASINs=[]
        self.VLList = []
        self.ParentASINDelete = '' 
        self.ParentASINUpload = ''
        self.ParentTrueFalse = {}
        self.Brsheet =[]


        """
            All the variables which are common to be 
            used for any brand are initiated here,
        
        """ 
        
        """ 
            rest all specific ones, are created 
            in ProcessStart function()
        """

        
        # set the brand and other variable , below in process start modify them according to brand
        self.VL_Name = ''
        self.file_name_google_drive = ''
        self.Missing_variation_path = ''
        self._brand_file_name = ''


        self.DownloadLocation = str(os.path.join(Path.home(), "Downloads\\"))
        self.SFTPLocation = str(os.path.join(Path.home(), "Downloads\\")) + "VL Alert\\" 
 

        
        ## parent with or without sku file
        self.Parent_without_SKU_file_path = ''
        ## Missing asins active and inActive historical data check file
        self.file_matching_historical_data = ''
        self.file_unmatching_historical_data = ''
        self.VL_upload_file =  ''

        self._ParentASIN = ""
        self._ASINNode =  ""
        self._ASINCategory =  ""
        self._NodeError = ""
        self._ManualLog =  ""
        # self.keys_with_matching_values = {}
        self.child_asin_skus = {}
        self.mapped_parent_child_items = {}
        self.mapp_relisted_items = {}
        
        # subject names for extra asins
        self.SAS_IO_Subject = ''
        self.SAS_IA_Subject = ''
        
        # subject names for  parent with sku asins
        self.SAS_IO_with_parent_sku = ''
        self.SAS_IA_with_parent_sku = ''
        
        # parent without sku asins
        self.SAS_IO_without_parent_sku = ''
        self.SAS_IA_without_parent_sku = ''
        
        # subject names for missing parent sku asins - matching
        self._Missing_case_SAS_IO_Matching = ''
        self._Missing_case_SAS_IA_Matching = ''

        # subject names for missing parent sku asins - unmatching
        self._Missing_case_SAS_IO_UnMatching = ''
        self._Missing_case_SAS_IA_UnMatching = ''

        # time period  for SAS case 
        self.Sas_create_time = 4

        # time period to inform user
        self.threshold_inform_user_time = 48

        # Reading Master sheet
        self.Master_sheet = ''
        self.false_parent_child_skus = []
        
        self.list_of_no_historical_bg_asins = {}
        self.post = PostFun() 
        self.commonfun = CommonFun()
        self.today = datetime.today()

        self.parent_product_name = None

    def __del__(self):
        self.IDList=[]
        self.ID = -1
        print('Destructor called')       
        del self
           
    def openbrowser(self):
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
            self.driver = webdriver.Chrome( "driver/chromedriver.exe", chrome_options=chrome_options)
            

            #self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
            #self.driver = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=chrome_options)           
            
            self.driver.get("https://sellercentral.amazon.com/signin?ref_=scus_soa_wp_signin_n&initialSessionID=131-0804803-7281043&ld=SCUSWPDirect")            
            

            print("openbrowser","Browser prepared successfully!") 
            #messagebox.showinfo("Init", "Browser prepared successfully!")
            self.post.ProcessErrorLog(self, 1, "CD Open Successfully")
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "CD " + str(err)) 

    def filllogin(self ):
        try:            
            emailid ='gya.ads.portfolio.ai.01@gmail.com'
            password ='`A3Rmqm/DHBJWF}B'

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

            print("filllogin","Login successfully!") 
            self.post.ProcessErrorLog(self, 1, "Login successfully!") 
        except Exception as err:                 
            print("filllogin",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Login " + str(err)) 

    def otplogin(self ):
        try:

            time.sleep(5)          
            text = 'LFNPECCHNTZQ6FRVZZRQHOH6CSERSLP45ACVZX6OYU63BZHALUKQ'
            # text = 'DAKNTK2ZDVBDJ2UMFVCKEEGC7UIGFUAOHD7CMXO4ASMBMSEXTR7A'
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

    def DownloadGoogleFile(self):
        #self._DefaultName = 'HEO030M14_PARENT'
        filename =  self.file_name_google_drive
        _filename = [ filename ]
        time.sleep(2)

        try:
           
            CLIENT_SECRET_FILE = 'GoogleCredentials\client_drive.json'
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']
                
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

            results = service.files().list(
                q=f"'1QxvMKKLtqj0lwDwzVnVewUs1X4VR4QRK' in parents",    
                pageSize=1000, 
                fields="nextPageToken, files(id, name, mimeType, parents, trashed)"
            ).execute()
            items = results.get('files', [])
            items = pd.DataFrame(items)  
            items = items[ ((items['name'].isin(_filename)) & (items['trashed'] == False)) ]

            if os.path.exists(self.Missing_variation_path + _filename[0])==True:
                os.remove(self.Missing_variation_path + _filename[0])

            if len(items)==1:
                for _indices, _filedetails in items.iterrows(): 
                    request = service.files().get_media(fileId = _filedetails['id'])
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))
                    dfilespath = self.Missing_variation_path + _filedetails['name']

                    if 1==1:
                        with io.open(dfilespath, "wb") as f:        
                            fh.seek(0)
                            f.write(fh.read())
                    else:
                        with io.open(dfilespath, "wb") as f:        
                            fh.seek(0)
                            f.write(fh.read())
            else:                
                self.post.ProcessErrorLog(self, 2, "Error DownloadGoogleFile files count not match " + filename + ' ' + str(len(items))) 
                return False
            
            time.sleep(2)            
            self.post.ProcessErrorLog(self, 1, "File Downloaded from google drive") 
            return dfilespath  
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error DownloadGoogleFile " + filename + ' ' + str(err)) 
            self._ManualLog = 'Error in Download Google File'
            return False 

    def untick_all_countries(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 900)")
            time.sleep(2)
            radio_America = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_AMERICAS")
            if radio_America.get_attribute('checked') == None:
                print(radio_America.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_America).perform()
                radio_America.click()
            time.sleep(2)
            radio_Europe = self.driver.find_element(by = By.ID, value='AGS_DB_LISTINGS_EU')
            if radio_Europe.get_attribute('checked') == None:
                print(radio_Europe.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Europe).perform()
                radio_Europe.click()
            time.sleep(2)
            radio_Japan = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_JP")
            if radio_Japan.get_attribute('checked') == None:
                print(radio_Japan.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Japan).perform()
                radio_Japan.click()
            time.sleep(2)
            radio_Australia = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_AU")
            if radio_Australia.get_attribute('checked') == None:
                print(radio_Australia.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Australia).perform()
                radio_Australia.click()
            time.sleep(2)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_America).perform()
            radio_America.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Europe).perform()
            radio_Europe.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Japan).perform()
            radio_Japan.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Australia).perform()
            radio_Australia.click()
            time.sleep(2)
            return True

        except Exception as e:    
            self.post.ProcessErrorLog(self, 2, "Untick Code error" ) 
            self._ManualLog = 'Issue in unticking countries while downloading latest template from amazon portal '
            return False 
    
    def close_excel_files(self):

        excel_processes = [process for process in psutil.process_iter(attrs=['pid', 'name']) if 'excel' in process.info['name'].lower()]

        for process in excel_processes:
            try:
                psutil.Process(process.info['pid']).terminate()
                print(f"Closed Excel process with PID: {process.info['pid']}")
            except Exception as e:
                print(f"Error closing Excel process: {e}")

    def DownloadTemplateFile(self):
        
        """ Getting the latest template from amazon 
            and storing it in Template Directory
        """

        try:
            
            try:
                time.sleep(3)
                new_filename = self.Missing_variation_path + "file_with_values_sku.xlsx"
                source_file = self.Missing_variation_path + self.file_name_google_drive
                ### Closes all excel file
                self.close_excel_files()
        
                if os.path.isfile(new_filename):
                    os.remove(new_filename)

                if os.path.isfile(source_file):
                    os.rename(source_file, new_filename)


                time.sleep(5)
              
                node_keywords = ['Essential Oil Singles', 'ESSENTIAL_OIL']
                fileList = os.listdir(self.DownloadLocation)
                
                ### get driver url 
                self.driver.get('https://sellercentral.amazon.com/listing/cards/add-product?style=standalone')

                time.sleep(3)
                try:
                    ### dont show again button
                    jspath = 'document.querySelector("#dont-ask-again-checkbox").shadowRoot.querySelector("div.checkbox").click();'
                    self.driver.execute_script(jspath)
                    ### ok got it button 
                    jspath = 'document.querySelector("#ok-got-it-btn").click();'
                    self.driver.execute_script(jspath)
                    time.sleep(3)
                except:
                    self.post.ProcessErrorLog(self, 1, f'Dont show again button not shown');print(f'Dont show again button not shown ')

                ## input given 
                self.driver.find_elements(By.CSS_SELECTOR, 'kat-input')[0].send_keys('Essential Oils')
                time.sleep(3)

                ### click search
                jspath = 'document.querySelector(\'[data-testid="search-button"]\').click();'
                self.driver.execute_script(jspath)
                time.sleep(3)

                
                js_path = 'document.querySelector("#view-all-link").click();'
                self.driver.execute_script(js_path)
                time.sleep(3)


                ### untick oil-sets and oil-blends

                # Assuming you have the parent element
                parent_element = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[3]/div/kat-tabs/kat-tab[1]/div/div/div[2]/div[1]/div/div[2]/kat-box[2]/div/kat-modal/div[2]/kat-box[2]/div/div/div/div[1]/div/kat-checkbox')

                # JavaScript code to find and untick the child checkbox within the shadow root
                script = """
                    const parent = arguments[0];
                    const shadowRoot = parent.shadowRoot;
                    const child = shadowRoot.querySelector('div[part="checkbox-check"]');
                    child.click();
                """

                # Execute the script to untick the child checkbox
                self.driver.execute_script(script, parent_element)
                time.sleep(2)

                ########################
                parent_element = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[3]/div/kat-tabs/kat-tab[1]/div/div/div[2]/div[1]/div/div[2]/kat-box[2]/div/kat-modal/div[2]/kat-box[2]/div/div/div/div[3]/div/kat-checkbox')

                # JavaScript code to find and untick the child checkbox within the shadow root
                script = """
                    const parent = arguments[0];
                    const shadowRoot = parent.shadowRoot;
                    const child = shadowRoot.querySelector('div[part="checkbox-check"]');
                    child.click();
                """

                # Execute the script to untick the child checkbox
                self.driver.execute_script(script, parent_element)
                time.sleep(2)

                ### continue button
                self.driver.find_elements (by= By.XPATH,value= '//*[@data-testid="modal-continue-button"]')[0].send_keys(Keys.ENTER)
                time.sleep(1)

                ### select button 
                self.driver.find_elements (by= By.XPATH,value= '//*[@data-testid="select-button"]')[0].send_keys(Keys.ENTER)
                time.sleep(1)

                ### generate spreadsheet
                self.driver.find_elements (by= By.XPATH,value= '//*[@kat-aria-behavior="tooltip"]')[0].click()
                time.sleep(1)
                
                self._ManualLog = 'File Downloaded'
            except  Exception as e :
                self.post.ProcessErrorLog(self, 1, f'download template failed due to issue - {e}');print(f'download template failed due to issue - {e} ')
                self._ManualLog = 'Download failed'    
                
                body = f"""
Hi,

For Brand {self.VL_Name}'s -  Latest template, Couldnt be downloaded 
due to element changes, Kindly wait until we fix that... 

Thanks
                """
                self.inform_users_via_mail(self._ManualLog, body)
                return False
     
            filename = node_keywords[1]
            print('Self of manual log = ',self._ManualLog)
            self.post.ProcessErrorLog(self, 1, str(self._ManualLog) + ' about to move the file')
            if self._ManualLog == 'File Downloaded':
                #Move download file to Template VL Alert folder
                print(f'Gonna move the file {filename} to destination')
                self.post.ProcessErrorLog(self, 1, f"Gonna move the file {filename} to destination") 
                time.sleep(15)
                fileList = os.listdir(self.DownloadLocation)
                for file in fileList:
                    if filename in file and '.xlsm' in file:
                        shutil.move( os.path.join(self.DownloadLocation, filename+'.xlsm') , os.path.join(self.Missing_variation_path, 'Latest_Template.xlsm')   )
                        print('File moved to Template Directory')
                        self.post.ProcessErrorLog(self, 1, "File Downloaded from Amazon template drive") 
                        self.post.ProcessErrorLog(self, 1, "File moved to Template Directory")
                        self._ManualLog = ''
                        return True
            
        except Exception as e:
            print('Error', e)
            self.post.ProcessErrorLog(self, 1, f"Issue in Downloading Latest Template {e}, returning back... ")
            self._ManualLog = 'Error in Download Template'
            return False

    def move_content_from_drive_to_template(self):
        
        try:

            old_template  = self.Missing_variation_path + f"file_with_values_sku.xlsx"
            new_template = self.VL_upload_file
            time.sleep(2)

            self.post.ProcessErrorLog(self, 1, "Now Comparing both the sheets with their column count and their names")

            wb_source_old_template= xw.Book(old_template)
            sheet_source_old_template = wb_source_old_template.sheets['Template']  
            column_range = sheet_source_old_template.range('A3:ZZ2')
            column_range.column_width = 12
            row_range = sheet_source_old_template.range('3:10000')
            row_range.row_height = 15
            length_old_template = sheet_source_old_template.range(1,1).end('down').row
            old_template_num_columns = sheet_source_old_template.api.UsedRange.Columns.Count
            column_names_old = sheet_source_old_template.range('A3').expand('right').value


            time.sleep(5)
            wb_source_new_template= xw.Book(new_template)
            sheet_source_new_template = wb_source_new_template.sheets['Template']  
            column_range = sheet_source_new_template.range('A3:ZZ2')
            column_range.column_width = 12
            row_range = sheet_source_new_template.range('3:10000')
            row_range.row_height = 15
            length_new_template = sheet_source_new_template.range(1,1).end('down').row
            new_template_num_columns = sheet_source_new_template.api.UsedRange.Columns.Count
            column_names_new = sheet_source_new_template.range('A3').expand('right').value

            time.sleep(2)
            if not old_template_num_columns == new_template_num_columns:
                self.post.ProcessErrorLog( self, 2, "old template column COUNT not match did not with new template  " ) 
                self._ManualLog = 'Column COUNT NOT match did not with new template  '
                print('Column COUNT NOT match did not with new template')
                self.sendmessage()
                return False
            
            elif  not column_names_old == column_names_new:
                self.post.ProcessErrorLog(self, 2, "Column names of old and new templates do not match")
                self._ManualLog = 'Column names of old and new  template did not match with new template  '
                print('Column names of old and new  template did not match with new template')
                self.sendmessage()
                return False
            
            
            for row_num in range(4, length_old_template + 1):
                data_row = sheet_source_old_template.range(f"A{row_num}:ZZ{row_num}").value
                sheet_source_new_template.range(f"A{row_num}:ZZ{row_num}").value = data_row

            
            wb_source_new_template.save()
            wb_source_new_template.close()
            wb_source_old_template.save()
            wb_source_old_template.app.quit()
            print(f"Data copied successfully to Latest_ {self.VL_upload_file}" )
            self.post.ProcessErrorLog(self,1,f"Data copied successfully to Latest_ {self.VL_upload_file}" )
            return True
        
        except Exception as e:             
            self.post.ProcessErrorLog( self, 2, f"Error DownloadGoogleFile files count not match  {e}" ) 
            self._ManualLog = 'Templates dont match, Error in moving content from source to destination'
            return False

    def ReadUpdateGoogleSheet(self, flag):

        try:            
            cellsASIN=[]
            
            if flag == 0:

                googleAPI = 'GoogleCredentials\client_sheet.json'
                scope = ['https://www.googleapis.com/auth/drive']
                credentials = service_account.Credentials.from_service_account_file(googleAPI)
                scopedCreds = credentials.with_scopes(scope)
                gc = gspread.Client(auth=scopedCreds)
                gc.session = AuthorizedSession(scopedCreds)     
                self.gsheetUpdate = gc.open(self._brand_file_name).worksheet("VL Data")
                self.gsheetUpdateLog = gc.open(self._brand_file_name).worksheet("VL Log")
                
                # self.gsheetData = self.gsheetUpdate.get_all_records()
                # self.gsheetData = pd.DataFrame.from_dict(self.gsheetData)
                #self.gsheetData =  self.gsheetData[self.gsheetData['Status']=='Yes']
                data_values = self.gsheetUpdate.get_all_values()
                headers = data_values[0]
                self.gsheetData = pd.DataFrame(data_values[1:], columns=headers)


                self.brandsheet = gc.open('Amazon Category Path Suppression & Case ID RPA').worksheet("Node Path")
                self.Brsheet = self.brandsheet.get_all_records()
                self.Brsheet = pd.DataFrame.from_dict(self.Brsheet)

                self.gsheet_job_log_Update = gc.open(self._brand_file_name).worksheet("Job Log")
                
                # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
                # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)
                
                data_values = self.gsheet_job_log_Update.get_all_values()
                headers = data_values[0]
                self.gsheetData_job_log = pd.DataFrame(data_values[1:], columns=headers)

               
                self.post.ProcessErrorLog(self, 1, "gsheet open update Sucessfully")

                return self.gsheetData
            
            elif flag == 1:
                ...
                # time.sleep(2)
                # _missing = self.gsheetData.columns.get_loc('List of Missing ASINs')  + 1
                # _extra = self.gsheetData.columns.get_loc('List of Extra ASINs')  + 1
                # _catalog = self.gsheetData.columns.get_loc('Number of Deleted ASINs')  + 1

                # for _index, _row in self.gsheetData.iterrows():                    
                #     if _row['Child ASIN VL List'] in self.MissingASINs :
                #         cellsASIN.append(Cell(row = _index + 2, col = _missing, value =  'Yes' ))
                #     else:
                #         cellsASIN.append(Cell(row = _index + 2, col = _missing, value =  '' ))

                #     if _index > len(self.ExtraASINs)-1:
                #         cellsASIN.append(Cell(row = _index + 2, col = _extra, value =  '' ))

                # for _index in range(len(self.ExtraASINs)):   
                #     cellsASIN.append(Cell(row = _index + 2, col = _extra, value =  self.ExtraASINs[_index] ))
                

                # for _index in range(len(self.ExtraASINs)): 
                #     if  self.ExtraASINs[_index] in self.DeleteASINs :
                #         cellsASIN.append(Cell(row = _index + 2, col = _catalog, value =  'Deleted' ))
                #     else:
                #         cellsASIN.append(Cell(row = _index + 2, col = _catalog, value =  'Not in Catalog' ))
                
                    
                
                # googleAPI = 'GoogleCredentials\client_sheet.json'
                # scope = ['https://www.googleapis.com/auth/drive']
                # credentials = service_account.Credentials.from_service_account_file(googleAPI)
                # scopedCreds = credentials.with_scopes(scope)
                # gc = gspread.Client(auth=scopedCreds)
                # gc.session = AuthorizedSession(scopedCreds)     
                # self.gsheetUpdate = gc.open(self._brand_file_name).worksheet("VL Data")
                # self.gsheetUpdateLog = gc.open(self._brand_file_name).worksheet("VL Log")
                # self.gsheetUpdate.update_cells(cellsASIN) 


                # _Delete, _Upload = '', ''
                # if len(self.DeleteASINs)>0:
                #     _Delete, _Upload = 'Deleted', 'Uploaded'
                # insertRow = [datetime.today().strftime('%Y-%m-%d  %H:%M'), self.ID, self.CountryID ,  ",".join(self.ParentASINs) , ",".join(self.MissingASINs), ",".join(self.DeleteASINs), _Delete, _Upload, self._ManualLog ]
                # self.gsheetUpdateLog.append_row(insertRow)
                
                # time.sleep(2)
                # self.post.ProcessErrorLog(self, 1, "gsheet append row Sucessfully")

            elif flag == 2:
                
                _LiveParentASIN = self.gsheetData.columns.get_loc('Live Parent ASIN')  + 1

                cellsASIN = []
                for _index, _row in self.gsheetData.iterrows():
                    cellsASIN.append(Cell(row = _index + 2, col = _LiveParentASIN, value =  _row['Live Parent ASIN'] ))


                googleAPI = 'GoogleCredentials\client_sheet.json'
                scope = ['https://www.googleapis.com/auth/drive']
                credentials = service_account.Credentials.from_service_account_file(googleAPI)
                scopedCreds = credentials.with_scopes(scope)
                gc = gspread.Client(auth=scopedCreds)
                gc.session = AuthorizedSession(scopedCreds)     
                self.gsheetUpdate = gc.open(self._brand_file_name).worksheet("VL Data")
                self.gsheetUpdateLog = gc.open(self._brand_file_name).worksheet("VL Log")
                self.gsheetUpdate.update_cells(cellsASIN) 

                self.ParentASINDelete, self.ParentASINUpload 
                if self._ManualLog =='' and len(self.ExtraASINs)>0 and  len(self.DeleteASINs)>0 :
                    self.ParentASINDelete, self.ParentASINUpload  = 'Deleted','Uploaded'
                # if self._ManualLog =='' and len(self.ExtraASINs)>0 and  len(self.DeleteASINs)==0 :
                #     self.ParentASINDelete, self.ParentASINUpload  = 'Already Deleted','Already Uploaded'

                if len(self.MissingASINs)>0 and len(self.MissingASINs) == len(self.gsheetData['Child ASIN VL List'].unique()) :
                    self._ManualLog = 'System recalibrating, wait for next job run.'

                
                self.gsheetData_ = self.gsheetUpdateLog.get_all_records()
                self.gsheetData__log = pd.DataFrame.from_dict(self.gsheetData_)     

                non_updated_missing_asins = []                                   
                total_missing_asins = self.gsheetData__log[self.gsheetData__log['Activities Log - Add\nMissing ASIN(s)'] !=''][-1:]['Activities Log - Add\nMissing ASIN(s)'].values.tolist()
                non_updated_missing_asins = [i for i in self.MissingASINs if i not in total_missing_asins and i]

                non_updated_extra_asins = []
                total_extra_asins = self.gsheetData__log[self.gsheetData__log['Activities Log - Delete \nExtra ASIN(s)'] !=''][-1:]['Activities Log - Delete \nExtra ASIN(s)'].values.tolist()   
                non_updated_extra_asins = [i for i in self.DeleteASINs if i not in total_extra_asins and i]

                if not self.ParentTrueFalse:
                    self.ParentTrueFalse['ParentTrue'] = ''
                    self.ParentTrueFalse['ParentFalse'] = ''

                insertRow = [ datetime.today().strftime('%Y-%m-%d  %H:%M'), self.ID, self.CountryID, 
                             self.ParentTrueFalse['ParentTrue'], self.ParentTrueFalse['ParentFalse'], 
                             'Matching' if self.ParentTrueFalse['ParentTrue'] != '' else 'Not Matching', self._ManualLog, 
                             ", ".join(non_updated_missing_asins), 
                             ", ".join(non_updated_extra_asins) if self.ExtraASINs and len(self.ExtraASINs)>0  else '', 
                            self.ParentASINDelete, self.ParentASINUpload ,'', len(self.MissingASINs), len(self.ExtraASINs), ",".join(self.ExtraASINs),
                            self.SAS_IO_Subject, self.SAS_IA_Subject, 
                            self.SAS_IA_with_parent_sku, self.SAS_IO_with_parent_sku, 
                            self.SAS_IO_without_parent_sku, self.SAS_IA_without_parent_sku,
                            self._Missing_case_SAS_IO_Matching, self._Missing_case_SAS_IA_Matching,
                            self._Missing_case_SAS_IO_UnMatching, self._Missing_case_SAS_IA_UnMatching
                            ]
                self.gsheetUpdateLog.append_row(insertRow)


                   
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "ReadUpdateGoogleSheet - gsheet log Issue = It's not read  " + str(err)) 
 
    def loadASIN(self):
        try:
            
            self.arr=[]
            self.gsheetData = self.ReadUpdateGoogleSheet(0)
            for row in self.gsheetData['Parent for System Verification'].unique():
                self.arr.append( '1|'+ str(row).strip())  
            
            
            self.arr.append('')
            self.arr = set(self.arr)

            self.arr.remove('')
            self.arr = sorted(self.arr)
            
              
            self.ID = self.post.ProcessUpdate(self)
            self.IDList = self.post.ProcessLogUpdate(self)
           
                    
            print("loadASIN","ASIN prepared successfully!") 
            self.post.ProcessErrorLog(self, 1, "KeyList Prepared Sucessfully")
        except Exception as err:                 
            print("loadASIN",str(err)) 
            self.post.ProcessErrorLog(self, 2, "KeyList " + str(err)) 

    def updateRPAProcessLog(self, row):        
        self.PLID = int(row['ID']) 
        self.Status = int(row['Status'])
        self.ProcessLog = str(row['Process_Log']).replace("'","''") 
        self.post.ProcessLogUpdate(self)
    
    def CountrySelection(self,cntry):
        try:
            self.driver.execute_script("window.scrollTo(0, 900)")
            time.sleep(2)
            radio_America = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_AMERICAS")
            if radio_America.get_attribute('checked') == None:
                print(radio_America.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_America).perform()
                radio_America.click()
            time.sleep(2)
            radio_Europe = self.driver.find_element(by = By.ID, value='AGS_DB_LISTINGS_EU')
            if radio_Europe.get_attribute('checked') == None:
                print(radio_Europe.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Europe).perform()
                radio_Europe.click()
            time.sleep(2)
            radio_Japan = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_JP")
            if radio_Japan.get_attribute('checked') == None:
                print(radio_Japan.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Japan).perform()
                radio_Japan.click()
            time.sleep(2)
            radio_Australia = self.driver.find_element(by = By.ID, value="AGS_DB_LISTINGS_AU")
            if radio_Australia.get_attribute('checked') == None:
                print(radio_Australia.get_attribute('checked'))
                actions = ActionChains(self.driver)
                actions.move_to_element(radio_Australia).perform()
                radio_Australia.click()
            time.sleep(2)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_America).perform()
            radio_America.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Europe).perform()
            radio_Europe.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Japan).perform()
            radio_Japan.click()
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element(radio_Australia).perform()
            radio_Australia.click()
            time.sleep(2)
            con = self.driver.find_elements(by=By.CLASS_NAME,value="a-container")
            cc = con[1].find_elements(by=By.CLASS_NAME,value="a-row")
            if cntry == 'EU':
                for i in cc:
                    if i.text == 'Amazon.co.uk':
                        i.click()
            if cntry == 'JP':
                for i in cc:
                    if i.text == 'Amazon.co.jp':
                        i.click()
            if cntry == 'AU':
                for i in cc:
                    if i.text == 'Amazon.com.au':
                        i.click()
        except Exception as err:  
            print("radiobtn :",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Processing " + str(err))
    
    def UpdteSKUInDB(self,_ASIN, full_net_SKU,_sku,UPC_EAN,price,_CountryID):
        try:
            para = {
                "data" : {"userid":2, "ASIN": _ASIN, "CountryID":self.CountryID, "table": "Product_Master_Details_ByID" },
                "type":"Select"
            }
            post = PostFun()
            ddlRPAList = post.PostApiParaJson(para)
            for val in ddlRPAList['data']['input']:
                if val['GroupName'] !='Info':
                    for valupdate in val['data']:
                        if valupdate['TitleName']=='CountryID':
                            valupdate['data']['value'] =  ''
                            valupdate['data']['updatedvalue'] = _CountryID
                        elif valupdate['TitleName']=='SKU':
                            valupdate['data']['value'] =  ''
                            valupdate['data']['updatedvalue'] = _sku
                        elif valupdate['TitleName']=='FNSKU':
                            valupdate['data']['value'] =  ''
                            valupdate['data']['updatedvalue'] = full_net_SKU
                        elif valupdate['TitleName']=='EAN':
                            valupdate['data']['value'] =  ''
                            valupdate['data']['updatedvalue'] = UPC_EAN
                        elif valupdate['TitleName']=='Price':
                            valupdate['data']['value'] =  ''
                            valupdate['data']['updatedvalue'] = price
            para = {
                        "data" : {"userid":2, "source": ddlRPAList , "table": "Product_Master_Details_ByID" },
                        "type":"Insert"
                    }
            post = PostFun()
            ddlRPAList = post.PostApiParaJson(para)
            print(ddlRPAList)
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error SKU DB " + str(err)) 
            self._ManualLog = ''

    def VLStatus(self,FileName):
        try:

            if len(self.DeleteASINs)>0:
                cellsASIN=[]
                gsheetLog =  self.gsheetData_job_log.iloc[-1] 
                index = gsheetLog.shape[0]+1

                _Date = self.gsheetData_job_log.columns.get_loc('Time Extra Delete Upload')  + 1
                _Upload = self.gsheetData_job_log.columns.get_loc('Extra Upload')  + 1
                _Delete = self.gsheetData_job_log.columns.get_loc('Extra Delete')  + 1
                cellsASIN.append(Cell(row = index + 2, col = _Date, value =  datetime.today().strftime('%Y-%m-%d %H:%M')))
                cellsASIN.append(Cell(row = index + 2, col = _Upload, value =  'Upload' ))
                cellsASIN.append(Cell(row = index + 2, col = _Delete, value =  'Delete' ))                    
                self.gsheet_job_log_Update.update_cells(cellsASIN) 
                time.sleep(2)


            self.post.ProcessErrorLog(self, 1, "Checking upload status") 
            time.sleep(5)
            pageStatus = False
            icount = 0
            while pageStatus == False  :                             
                if icount >= 1 :
                    pageStatus = True
                time.sleep(20)   
                icount += 1
                self.driver.get(self.CountryURL(self.CountryID,4))
                time.sleep(2)
                keylist =  self.driver.find_elements (by= By.XPATH,value= '//*[@id="submission-status-table"]/table/tbody/tr')
                #print(len(keylist))  
                for rowkey in keylist:
                    td = rowkey.find_elements(By.TAG_NAME, "td")                     
                    if len(td)> 0:  
                        #print(td[0].text,td[3].text)
                        if FileName in td[0].text :
                            if 'Done' in td[3].get_attribute('innerHTML') or 'Action required' in td[3].get_attribute('innerHTML'):                            
                                pageStatus = True
                                self.post.ProcessErrorLog(self, 1, "Upload Status Done") 
                                self._ManualLog = ''
                                return True
        
        
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error VLStatus " + str(err)) 
            self._ManualLog = ''
  
    def sendmessage(self):     
        try:
            
            self.body=''   
                   
        #             True Parent: 1 (ASIN - )
        # False Parent: 1 (ASIN - ABCDE, XYGH)
        # Extra SKUS: 3 Deleted (ASIN - )

            if (self.ParentTrueFalse['ParentTrue']!=''  or self.ParentTrueFalse['ParentFalse']!='' or len(self.ExtraASINs)>0  ) :
                self.body="\nHi <@U01CXGPU8KV>, Hi <@UTZUMGHT7> VL Alert Message\n\n"

                if self.ParentTrueFalse['ParentTrue']!='':
                    self.body = self.body + f'{self.VL_Name} True Parent: ( '+ self.ParentTrueFalse['ParentTrue'] +' )\n'

                if self.ParentTrueFalse['ParentFalse']!='':
                    self.body = self.body + f'{self.VL_Name} False Parent: ( '+ self.ParentTrueFalse['ParentFalse'] +' )\n'

                if len(self.ExtraASINs)>0:                    
                    self.body = self.body + f'{self.VL_Name} Extra ASIN: ( ' +  str(",".join(self.ExtraASINs)) + " )\n"
                
                

                # if len(self.MissingASINs)>0:                    
                #     self.body = self.body + 'Total count of Child ASINs Missing in VL portal: ' +  str(len(self.MissingASINs)) + "\n"
                #     self.body = self.body + ','.join(self.MissingASINs)

                    

                # if len(self.ParentASINs)>0:                    
                #     self.body = self.body + 'Total count of Parent ASIN in VL portal: ' +  str(len(self.ParentASINs)) + "\n"
                #     self.body = self.body + ','.join(self.ParentASINs)

                self.body = self.body + "\n\nSystem Generated Messages\n\n\n"    
                
    
                if self.body !="":
                    self.post.body = self.body
                    #self.post.body = "This is Test message ignore \n" + self.body
                    self.post.sendslackmessage()

                self.post.ProcessErrorLog(self, 1, "Slack Message Sucessfully")
            else:
                self.post.ProcessErrorLog(self, 1, "Slack No error Message Sucessfully")

            return True
        except Exception as err:  
            print(str(err))
            self.post.ProcessErrorLog(self, 2, "Slack Message error " + str(err)) 
            return False

    def signout(self):
        try:
            time.sleep(2)
            self.driver.get('https://advertising.amazon.com/cm/campaigns?entityId=ENTITY1TUNS1T5BI3UY')
            time.sleep(5)
            
            elems = self.driver.find_elements_by_xpath('//*[@data-takt-id="FIT_LAUNCH_MODAL_desktop_fox-bis-ucm-launch-modal_close-button"]')
            if len(elems)>0:
                elems[0].click()
                time.sleep(2)

            x = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="topBar"]/div[3]/span[4]/button')))
            x.click()
            time.sleep(2)
            x = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Sign out')))
            x.click()
            self.post.ProcessErrorLog(self, 1, "Signout Sucessfully")
            print( "Signout Sucessfully")
        except Exception as err:  
            self.post.ProcessErrorLog(self, 2, "Signout " + str(err))

    def CountryURL(self, _CountryID, _type):
        # 1 Download Excel Template
        # 2 Manage Inventory
        # 3 Upload Excel File
        # 3 Upload Stauts
        # 5 EBC Screen
        url = self.commonfun.CountryURL(_CountryID)
        if _type == 1 and _CountryID == 1 :
                url = url + 'listing/product-template?preferredContributor=A6IJWM3CPIGTQ&mons_sel_mcid=A31LSP1L7F6XJ2&mons_sel_mkid=ATVPDKIKX0DER'
        elif _type == 1 and _CountryID == 5 :
                url = url + 'listing/product-template?preferredContributor=A6IJWM3CPIGTQ&mons_sel_mcid=A146DED07RLPHY&mons_sel_mkid=A1F83G8C2ARO7P'    
        elif _type == 1 and _CountryID == 14 :
                url = url + 'listing/product-template?preferredContributor=A3QFFQUV0CNYV4&mons_sel_mcid=A3QFFQUV0CNYV4&mons_sel_mkid=A19VAU5U5O7RUS'    
        elif _type == 2 :
            url = url +  'inventory/ref=xx_invmgr_dnav_xx'    
        elif _type == 3:
            url = url +  'listing/upload?ref_=xx_upload_tnav_status'
        elif _type == 4:
            url = url +  'listing/status?ref_=xx_status_tnav_status'
        elif _type == 5:
            url = url +  "enhanced-content/content-manager"                    
        return url

    def ImageCaptcha(self):        
        time.sleep(1)
        title = self.driver.title
        captcha = self.driver.find_elements(by=By.LINK_TEXT, value='Try different image')
        if title=='Server Busy' or len(captcha)>0:   
            # self.driver.refresh()
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

    def FindVLData(self, ASINList, parent = False):
        
        try:

            mapped_parent_child = {}
            

            self.driver.get("https://sellercentral.amazon.com/listing/varwiz?ref=ag_varwiz_xx_invmgr")
            time.sleep(2)

            if parent:
                for i in range(2):
                    variation_wizard_length  = self.driver.find_elements(By.ID, 'varwizard_accordion')
                    time.sleep(2)

                if len(variation_wizard_length) <= 0:
                    print(f"Page didn't load within ~ seconds  in {i} attempt Error:")
                    self.post.ProcessErrorLog(self, 2, "Page Unsuccessful in Loading " )  
                    return 'PAGE NOT LOADED' 
                else:
                    print(f"Page loaded successfully for checking from parent asin! ")
                    self.post.ProcessErrorLog(self, 1, "Page Successful in Loading for checking from parent asin! " )  
                    

            for _ASIN in ASINList:
                
                _childli,_parentli = [],[]

                self.driver.refresh()
                time.sleep(2)            
                element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'varwizard_accordion')))
                element.click()
                time.sleep(5)

                element = element.find_elements(by= By.TAG_NAME,value='a')[0]
                element.click()
                time.sleep(5)

                element = self.driver.find_element(by=By.ID,value='varwiz-search-text')            
                element.send_keys(_ASIN) 
                time.sleep(3)

                try:
                    if WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-0"]/span/input'))):
                        element = element.find_element(by= By.XPATH,value='//*[@id="a-autoid-0"]/span/input')
                        if element.is_enabled():
                            element.click()
                            time.sleep(15)
                except:
                    self.post.ProcessErrorLog(self, 2, f"Variation Wizard element  button not clickable  " )  
                    return False
                
                if parent:
                    for _ in range(2):
                        time.sleep(2)
                        tables = self.driver.find_elements(by=By.TAG_NAME,value='tbody')
                        tab=tables[0]
                        if tab.text != '':
                            print(f"Table of rows loaded successfully! Checked {_+1} ")
                            self.post.ProcessErrorLog(self, 1, f"Table of rows Successful in Loading Checked {_+1} " ) 
                            
                        else:
                            print(f"Table of rows didn't load within ~ seconds  Error:")
                            self.post.ProcessErrorLog(self, 2, f"Table of rows Unsuccessful in Loading Checked {_+1} " )  
                            return "PAGE NOT LOADED"    
                
                
                paging = self.driver.find_elements(by=By.CLASS_NAME,value='a-pagination')
                
                if len(paging)==0:
                    tables = self.driver.find_elements(by=By.TAG_NAME,value='tbody')
                    tab=tables[0]
                    keylist = tab.find_elements(by=By.TAG_NAME,value='tr')
                    for rowkey in keylist:           
                        if rowkey.get_attribute('id') !='head-row':
                            td = rowkey.find_elements(By.TAG_NAME, "td")   
                            if len(td)>0 and td[0].text=='child':
                                _childli.append (td[1].text)
                            elif len(td)>0 and td[0].text=='parent':
                                _parentli.append (td[1].text)
                                #self._parent_skus[td[1].text] = td[2].text
                            
                            if len(td)>0 and (td[0].text=='parent' or td[0].text=='child'):
                                rowdata = { 'RequestASIN': _ASIN,'Type':td[0].text, 'ASIN':td[1].text, 'SKU': td[2].text}
                                self.VLList = pd.concat([pd.DataFrame([rowdata], columns=self.VLList.columns), self.VLList], ignore_index=True)


                    time.sleep(2)
                else:

                    paging = paging[0].find_elements(by=By.TAG_NAME,value='a')
                    
                    for page in paging: 
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].scrollIntoView();", page)
                        time.sleep(1)
                        page.click()
                        time.sleep(4)
                        
                        tables = self.driver.find_elements(by=By.TAG_NAME,value='tbody')
                        tab=tables[0]
                        keylist = tab.find_elements(by=By.TAG_NAME,value='tr')
                        
                        for rowkey in keylist:           
                            if rowkey.get_attribute('id') !='head-row':
                                td = rowkey.find_elements(By.TAG_NAME, "td")   
                                if len(td)>0 and td[0].text=='child':
                                    _childli.append(td[1].text)
                                elif not td:
                                    _childli.append(_ASIN)
                                elif len(td)>0 and td[0].text=='parent':
                                    _parentli.append (td[1].text)
                                    #self._parent_skus[td[1].text] = td[2].text
                        
                                if len(td)>0 and (td[0].text=='parent' or td[0].text=='child'):
                                    rowdata = {'RequestASIN': _ASIN, 'Type':td[0].text, 'ASIN':td[1].text, 'SKU': td[2].text}
                                    self.VLList = pd.concat([pd.DataFrame([rowdata], columns=self.VLList.columns), self.VLList], ignore_index=True)


                        time.sleep(2)

                
                _childli = list(set(_childli))
                _parentli = list(set(_parentli))
                mapped_parent_child[(''.join(_parentli))] = _childli

            return mapped_parent_child
            
        except Exception as err:  
            print("FindVLData Error ", str(err))
            self.post.ProcessErrorLog(self, 2, "FindVLData Method Error " + str(err)) 
            return  [],[]

    def AddDefaultLastRowinJobLog(self):

        # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
        # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)
        current_row = self.gsheetData_job_log.index[-1]
        # self.gsheetData_job_log = self.gsheetData_job_log.astype(str)
        # self.gsheet_job_log_Update.append_row(self.gsheetData_job_log.iloc[current_row].values.tolist())

        
        previous_row_values = self.gsheetData_job_log.iloc[current_row].values.tolist()
        # data_values = self.gsheet_job_log_Update.get_all_values()
        # headers = data_values[0]
        # self.gsheet_job_log_Update = pd.DataFrame(data_values[1:], columns=headers)

               
        
        cellsASIN=[]
        Date = self.gsheetData_job_log.columns.get_loc('Date')  + 1
        Job_ID = self.gsheetData_job_log.columns.get_loc('Job ID')  + 1
        Country = self.gsheetData_job_log.columns.get_loc('Country')  + 1
        True_Parent_ASIN = self.gsheetData_job_log.columns.get_loc('True Parent ASIN')  + 1
        
        ### current row + 3 == we are adding to the next row  DONT CHANGE IT 

        cellsASIN.append(Cell(row = current_row + 3, col = Date , value = datetime.now().strftime('%Y-%m-%d %H:%M') ))
        cellsASIN.append(Cell(row = current_row + 3, col = Job_ID , value =  self.ID ))
        cellsASIN.append(Cell(row = current_row + 3, col = Country , value =  self.CountryID ))
        cellsASIN.append(Cell(row = current_row + 3, col = True_Parent_ASIN , value =  'Job Running' ))
        
        self.gsheet_job_log_Update.update_cells(cellsASIN)

        time.sleep(5)
        # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
        # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)

    def getdatafromamazon(self):            
        
        try: 
            self.IsComplete = 0
            self.ID =  self.post.ProcessUpdate(self)   

            time.sleep(5)
            for indices, row in self.IDList.iterrows(): 
                
                try:    
                   
                    if int(row['Status'])!=0:
                        continue

                    
                    _CountryID =int(row['Process_Name'].split('|')[0])
                    self._ParentASIN = row['Process_Name'].split('|')[1]
                    self.post.ProcessErrorLog(self, 1,  'Logs Added !');print(f'Logs Added !')
                    # self._ParentASIN = "B09JNKFV7T"
                    # _CountryID = 1
                    print('Parent ',self._ParentASIN) 
                    if self._ParentASIN == '': 
                        self.post.ProcessErrorLog(self, 1, f' In VL data found child without any parent, Missing asins will be found ! ')
                        print(f'In VL data found child without any parent, Missing asins will be found !   ')
                        continue

                    self.ReadUpdateGoogleSheet(0)
                    self.AddDefaultLastRowinJobLog()
                    self.post.ProcessErrorLog(self, 1, "Added Default Last Row in JobLog from the previous sheet "  )

                    self.post.ProcessErrorLog(self, 1, "Starting with VL Check Variation CHECKPOINT ")
                    country_list=['US']
                    if self.VLCheckAddVariation()==False:        
                        if self.CreateSKUList()==False : 
                            self.ReadUpdateGoogleSheet(2)
                            row['Status'] = 1
                            row['Process_Log'] = '' 
                            self.updateRPAProcessLog(row)
                            print("Complete", self._ParentASIN) 
                            continue
                        if self.DownloadTemplateType(country_list)==False : 
                            self.ReadUpdateGoogleSheet(2)
                            row['Status'] = 1
                            row['Process_Log'] = '' 
                            self.updateRPAProcessLog(row)
                            print("Complete", self._ParentASIN) 
                            continue                        
                        if self.CreateTemplateForUploadType(country_list) ==False : 
                            self.ReadUpdateGoogleSheet(2)
                            row['Status'] = 1
                            row['Process_Log'] = '' 
                            self.updateRPAProcessLog(row)
                            print("Complete", self._ParentASIN) 
                            continue
                        ### for READING , we dont append numeric 2 to the last row ,while updating entries we do !!
                        if self.UploadVLFileType(country_list)==False : 
                            self.ReadUpdateGoogleSheet(2)
                            row['Status'] = 1
                            row['Process_Log'] = '' 
                            self.updateRPAProcessLog(row)
                            print("Complete", self._ParentASIN) 
                            continue
                        self._ManualLog = ''
                        self.ReadUpdateGoogleSheet(2)
                    else:
                        self.ReadUpdateGoogleSheet(2)
                        if not [i for i in self.mapped_parent_child_items]:
                            self._ManualLog = 'No parent Child mapping found'
                            print('Exception in VLCheckAddVariation  as table did not loaded successfully to capture parent child items from any of the case ')
                            self.post.ProcessErrorLog(self, 2, "Exception in VLCheckAddVariation  a4s table did not loaded successfully to capture parent child items from any of the case  " )
                            self.ParentTrueFalse['ParentTrue'] = ''
                            self.ParentTrueFalse['ParentFalse'] = ''
                            ### no true parent found - will send the message in slack
                            self.sendmessage()


                    time.sleep(2)
                    row['Status']=1
                    row['Process_Log']= '' 
                    self.updateRPAProcessLog(row)
                    print("Complete", self._ParentASIN) 


                except Exception as err: 
                    print("Exception", self._ParentASIN, str(err)) 
                    time.sleep(2)
                    row['Status']=2
                    row['Process_Log']= str(err)
                    self.updateRPAProcessLog(row)   
                    self.post.ProcessErrorLog(self, 1, "Exception " + self._ParentASIN +' ' + str(err) )

                    country_list=['US']
           
        
            print('\nself.MissingASINs\t', self.MissingASINs)
            print('self.ExtraASINs\t\t', self.ExtraASINs)
            self.post.ProcessErrorLog(self, 1, f"self.MissingASINs{self.MissingASINs} , self.ExtraASINs {self.ExtraASINs}  ")
            

            self.post.ProcessErrorLog(self, 1, f"Outcome before: {str(self.ParentTrueFalse)} " )
            self.check_product_name()
            self.Create_ExtraChildASINDelete_Support_SAS_Case()
            self.relisting_items()
            self.Missing_asins_Support_SAS_case()
            self.update_sas_caseid()
            self.post.ProcessErrorLog(self, 1, f"Outcome After: {str(self.ParentTrueFalse)} " )
            
            # self.sendmessage()
            ### If Everything sorted, Updated Job Log sheet with positive message
            if len(self.ExtraASINs)==0 and len(self.MissingASINs) == 0 and self.ParentTrueFalse['ParentTrue'] !='' and self.ParentTrueFalse['ParentFalse']=='':
                cellsASIN=[]  
                current_row = self.gsheetData_job_log.index[-1]         
                for i in range(5, len(self.gsheetData_job_log.columns)):    
                    cellsASIN.append(Cell(row = current_row + 2, col = i , value =  '' ))                
                self.gsheet_job_log_Update.update_cells(cellsASIN) 
                self.post.ProcessErrorLog(self, 1, "Updated Google Sheet- all successfull , everything upto track")

            
            ### Update the VL Log sheet with Updated values
            cellsASIN=[]  
            update_rows = [ 
                        self.ParentTrueFalse['ParentTrue'], self.ParentTrueFalse['ParentFalse'], 
                            'Matching' if self.ParentTrueFalse['ParentTrue'] != '' else 'Not Matching', self._ManualLog
                            , ",".join(self.MissingASINs), ",".join(self.DeleteASINs) if self.ExtraASINs and len(self.DeleteASINs)>0  else '', 
                        self.ParentASINDelete, self.ParentASINUpload ,'', len(self.MissingASINs), len(self.ExtraASINs), ",".join(self.ExtraASINs),
                        self.SAS_IO_Subject, self.SAS_IA_Subject, 
                        self.SAS_IA_with_parent_sku, self.SAS_IO_with_parent_sku, 
                        self.SAS_IO_without_parent_sku, self.SAS_IA_without_parent_sku,
                        self._Missing_case_SAS_IO_Matching, self._Missing_case_SAS_IA_Matching,
                        self._Missing_case_SAS_IO_UnMatching, self._Missing_case_SAS_IA_UnMatching  ]
            current_row = self.gsheetData__log.index[-1]      
            for i in range(len(update_rows)):    
                cellsASIN.append(Cell(row = current_row + 3, col = i+4 , value =  update_rows[i]  ))                
            self.gsheetUpdateLog.update_cells(cellsASIN) 
            self.post.ProcessErrorLog(self, 1, "Updated VL LOG Google Sheet\n")


                

            print("getdatafromamazon",f"ASIN VL {self.VL_Name} prepared successfully!")   
            self.post.ProcessErrorLog(self, 1, "Processing Sucessfully")
            self.IsComplete=1
            self.ID =  self.post.ProcessUpdate(self ) 

        except Exception as err:  
            print("getdatafromamazonlast",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Processing failed in complete code " + str(err))

    def check_product_name(self):

        if self.ParentTrueFalse['ParentTrue'] or self.ParentTrueFalse["ParentFalse"]:
            
            parent = self.ParentTrueFalse['ParentTrue'] or self.ParentTrueFalse["ParentFalse"]

            self.driver.get("https://sellercentral.amazon.com/listing/varwiz?ref=ag_varwiz_xx_invmgr")
            time.sleep(2)

            
            self.driver.refresh()
            time.sleep(2)            
            element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'varwizard_accordion')))
            element.click()
            time.sleep(5)

            element = element.find_elements(by= By.TAG_NAME,value='a')[0]
            element.click()
            time.sleep(5)

            element = self.driver.find_element(by=By.ID,value='varwiz-search-text')            
            element.send_keys(parent) 
            time.sleep(3)
            
            try:
                if WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-0"]/span/input'))):
                    element = element.find_element(by= By.XPATH,value='//*[@id="a-autoid-0"]/span/input')
                    if element.is_enabled():
                        element.click()
                        time.sleep(15)
            except:
                self.post.ProcessErrorLog(self, 2, f"Variation Wizard element  button not clickable  " )  
                return False
	    
            tables = self.driver.find_elements(by=By.TAG_NAME,value='tbody')
            tab=tables[0]
            self.parent_product_name = tab.find_elements(By.ID, f'{parent}-item_name')[0].text.strip()


            self.find_parent_vl(parent)
            checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
            mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
            if not checkbundle[0].text.startswith('You currently have no listings'): 
                for each_product in mtrowlis:
                    id = each_product.get_attribute('id')
                    name = each_product.find_element(by = By.ID, value=id + '-title')
                    product_name = name.text.split('\n')[0]
                    name = name.text.split('\n')[2]
                    print(name)

                    if self.parent_product_name in product_name:
                        print('Product name is present in manage inventory')
                        self.post.ProcessErrorLog(self, 1, "Product name is present in manage inventory")
                    else:
                        
                        body = f"""
Hi,

For Brand {self.VL_Name}'s - {parent} - parent's Product name do not match.

The product name shown in Add inventory page - {self.parent_product_name}

and product name shown in manage inventory - {product_name}


Thanks
                        """
                        self.inform_users_via_mail(f"Product Name don't match of ASIN {parent} in {self.VL_Name}" , body, product_name=True)



    
    def relisting_items(self):
        
        try:
            Re_listed = []
            non_listed = []
            Total_ExtraAsins = []
            Vl_Remaining = []
            deleted_asins_to_be_relisted = []
            Total_Re_listed = []
            Previous_re_listed_total = []
            
            # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
            # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)
            
            data_values = self.gsheet_job_log_Update.get_all_values()
            headers = data_values[0]
            self.gsheetData_job_log = pd.DataFrame(data_values[1:], columns=headers)
            
            
            current_row = self.gsheetData_job_log.index[-1]

            
            ## current asins got from portal  == self.ExtrAsins
            ExtraAsins = self.ExtraASINs
    

            if self.gsheetData_job_log['ExtraAsins from VL'].iloc[current_row] == '':
                    Total_ExtraAsins += ExtraAsins
            else:
                Total_ExtraAsins = self.gsheetData_job_log['Total_ExtraAsins'].iloc[current_row].split(' ')
                ## len(self.gsheetData_job_log['Total_ExtraAsins'].iloc[current_row].split(' '))
                Total_ExtraAsins += [i for i in ExtraAsins if i not in Total_ExtraAsins]
                ## len(Total_ExtraAsins), len(ExtraAsins)
            
            parent_skus =  ''
            if not self.ExtraASINs:
                parent_skus = ' '.join(self.VLList[self.VLList['Type'] == 'parent']['ASIN'] )
            else:
                if len(self.VLList[(self.VLList['Type'] == 'child') & (self.VLList['ASIN'].isin(ExtraAsins))])>0:
                    parent_skus = self.VLList[(self.VLList['Type'] == 'child') & (self.VLList['ASIN'].isin(ExtraAsins))]['RequestASIN'].iloc[0]


            if len(Total_ExtraAsins)>0:
            
                # previous_row = current_row - 1 
                
                ### len(self.gsheetData_job_log['Vl_Remaining'].iloc[current_row].split(' '))
                
                previous_row_extra_asins = ' '.join(Total_ExtraAsins)
                if  self.gsheetData_job_log['Vl_Remaining'].iloc[current_row] == '':
                    remaining_count_not_listed = ExtraAsins 
                else:
                    remaining_count_not_listed = ExtraAsins  + self.gsheetData_job_log['Vl_Remaining'].iloc[current_row].split(' ')
                remaining_count_not_listed = list(set(remaining_count_not_listed))
                
                if remaining_count_not_listed:
                    deleted_asins_to_be_relisted = [asin for asin in previous_row_extra_asins.split(' ') if asin  in remaining_count_not_listed]
                    """
                    deleted_asins_to_be_relisted =   TOTAL ALL PREVIOUS ASINS - Extra asins from portal + Previous Vl remaning
                    """
                ## len(previous_row_extra_asins.split(' '))
            asins = list(set(deleted_asins_to_be_relisted) - set(self.ExtraASINs))
            asins = [asin for asin in asins if asin]
            # provide country id and asin for next line of code

            asin = ''

            if asins:

                ## RELISTING FUNCION CALLED for remaining Asins ~
                print("\nInitiating Relisting of all the Asins\n")
                self.post.ProcessErrorLog(self, 1, "Initiating Relisting of all the Asins")
                self.driver.get("https://sellercentral.amazon.com/home?mons_sel_dir_mcid=amzn1.merchant.d.AB3CG5MPUM7PZ3IPCJOCSA5JEM5A&mons_sel_mkid=ATVPDKIKX0DER&mons_sel_dir_paid=amzn1.pa.d.ACK2GASJ5Y6PL7M4KUAMRCL7EO2A&ignore_selection_changed=true")
                time.sleep(3)
                self.driver.get('https://sellercentral.amazon.com/inventory/ref=xx_invmgr_dnav_xx?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:;pagination:1;')
                
                try:
                        
                    for asin in asins:
                        self.driver.get('https://sellercentral.amazon.com/inventory/ref=xx_invmgr_dnav_xx?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:;pagination:1;')
                        time.sleep(2)
                        self.driver.find_element(by=By.XPATH, value='//*[@id="myitable-search"]').send_keys(asin)
                        time.sleep(2)
                        self.driver.find_element(by=By.CLASS_NAME, value='a-button-input').click()
                        time.sleep(3)
                        #obtain parent window handle
                        p= self.driver.window_handles[0]

                        base_urls = {
                            1: "https://sellercentral.amazon.com",
                            2: "https://sellercentral.amazon.ca",
                            3: "https://sellercentral.amazon.com.mx",
                            4: "https://sellercentral.amazon.de",
                            5: "https://sellercentral.amazon.co.uk",
                            6: "https://sellercentral.amazon.fr",
                            7: "https://sellercentral.amazon.es",
                            8: "https://sellercentral.amazon.it",
                            9: "https://sellercentral.amazon.com.au",
                            10: "https://sellercentral.amazon.pl",
                            11: "https://sellercentral.amazon.nl",
                            12: "https://sellercentral.amazon.se",
                            13: "https://sellercentral.amazon.jp",
                            14: "https://sellercentral.amazon.sg",
                            15: "https://sellercentral.amazon.com.tr/",
                            16: "https://sellercentral.amazon.com.be/",
                            17: "https://sellercentral.amazon.ae/"
                        }

                        # Check if the CountryID is valid (exists in the base_urls dictionary)
                        if self.CountryID in base_urls:
                            # Construct the URL based on the CountryID
                            base_url = base_urls[self.CountryID]
                    
                            time.sleep(3)
                            
                            # Define a dictionary containing individual IDs for specific links for each country
                            individual_ids = {
                                1: 'ATVPDKIKX0DER',   # United States
                                2: 'A2EUQ1WTGCTBG2',  # Canada
                                3: 'A1AM78C64UM0Y8',  # Mexico
                                4: 'A1PA6795UKMFR9',  # Germany
                                5: 'A1F83G8C2ARO7P',  # United Kingdom
                                6: 'A13V1IB3VIYZZH',  # France
                                7: 'A1RKKUPIHCS9HS',  # Spain
                                8: 'APJ6JRA9NG5V4',   # Italy
                                9: 'A39IBJ37TRP1C6',  # Australia
                                10: 'A1C3SOZRARQ6R3', # Poland
                                11: 'A1805IZSGTT6HS', # Netherlands
                                12: 'A2NODRKZP88ZB9', # Sweden 
                                13: 'A1VC38T7YXB528', # Japan
                                14: 'A19VAU5U5O7RUS', # Singapore
                                15: 'A33AVAJ2PDY3EV', # Turkey
                                16: 'AMEN7PMS3EDWL',  # Belgium
                                17: 'A2VIGQ35RCS4UG'  # United Arab Emirates
                            }

                            checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                            time.sleep(1)
                            self.driver.execute_script("document.body.style.zoom='70%'")
                            #if len(checkbundle) > 0 and checkbundle[0].text != 'You currently have no listings that meet this criteria. Use the filters below the search bar to view more of your listings.' :
                            listed_sku = checkbundle[0].find_elements(by = By.XPATH, value='//*[@data-column="sku"]')
                            listed_sku_texts =  [i.text for i in listed_sku]
                            # print(asin,sku)
                            
                            KeypairCountry = {}
                            try:
                                para = {
                                        "data" : {"userid":2, "ASIN":asin, "table": "Product_Master_Details_ByASINAll", "CountryID": self.CountryID},
                                        "type":"Select"
                                    }
                                post = PostFun()
                                skujson = post.PostApiParaJson(para)
                                
                                countryKey  =''
                                for val in skujson['data']['input']:
                                    if val['GroupName'] !='Info':
                                        for valupdate in val['data']:
                                            if valupdate['TitleName']=='CountryID':
                                                countryKey = valupdate['data']['updatedvalue']
                                            if valupdate['TitleName']=='SKU':
                                                if 'Country '+ str(countryKey) in list(KeypairCountry.keys()):
                                                    tmp =  list(KeypairCountry['Country '+ str(countryKey)])
                                                    tmp.append(valupdate['data']['updatedvalue'])
                                                    KeypairCountry['Country '+ str(countryKey)] = tmp
                                                else:
                                                    KeypairCountry['Country '+ str(countryKey)] = [valupdate['data']['updatedvalue']]
                                            if valupdate['TitleName']=='Price':
                                                if 'Price '+ str(countryKey) in list(KeypairCountry.keys()):
                                                    tmp =  list(KeypairCountry['Price '+ str(countryKey)])
                                                    tmp.append(valupdate['data']['updatedvalue'])
                                                    KeypairCountry['Price '+ str(countryKey)] = tmp
                                                else:
                                                    KeypairCountry['Price '+ str(countryKey)] = [valupdate['data']['updatedvalue']]

                            except:
                                # KeypairCountry = input('Dict it out manually \n{"Country 1": ["HEO030MORASnL"], "Price 1": [ "8.99"]}   \t:')
                                self.mapp_relisted_items[asin] =False
                                print(f"Issue in fetching data from DB for asin {asin} ")
                                continue
                            
                            

                                        
                            print("\rKey pair ",KeypairCountry)

                            skus = KeypairCountry[f'Country {self.CountryID}']
                            prices = KeypairCountry[f'Price {self.CountryID}']
                            sku_price_mapping = dict(zip(skus, prices))

                            filtered_mapping = {key: value for key, value in sku_price_mapping.items() if key not in listed_sku_texts}
                            if not filtered_mapping:
                                print(f"\nAll skus {skus} under asin ~ {asin}  Already re listed \n ",)
                                self.post.ProcessErrorLog(self, 1, f"  All skus {skus} under asin ~ {asin}  Already re listed ")
                                self.mapp_relisted_items[asin] = True
                                
                            else:
                                print("\nGoing to relist ASIN", asin, "\n")
                                self.post.ProcessErrorLog(self, 1, f"Going to relist ASIN  {asin}")
                                for country_id, link_id in individual_ids.items():
                                        if self.CountryID == country_id:
                                            ### link = self.driver.find_element(By.ID, value=link_id).get_attribute('href')
                                            ### self.driver.get(link)
                                            # time.sleep(5)
                                            
                                            base_search_url = f"{base_url}/product-search/search?q=B076N&ref_=xx_catadd_favb_xx"
                                            # print(base_search_url)
                                            # driver.get(base_search_url)
                                            base_search_url_parts = base_search_url.split('q=')
                                            # new_search_url = base_search_url_parts[0] + 'q=' + asin + '&' + base_search_url_parts[1].split('&', 1)[1]
                                            # print(new_search_url)
                                            # self.driver.get(new_search_url)
                                            time.sleep(5) 

                                            _url = f"{base_url}/abis/listing/syh?asin={asin}&ref_=xx_catadd_favb_xx#offer"
                                            _url_parts = _url.split('asin=')
                                            _url = _url_parts[0] + 'asin=' + asin + '&' + base_search_url_parts[1].split('&', 1)[1]
                                            # print(_url)
                                            

                                            
                                            time.sleep(7) 


                                            for asin, asin_price in filtered_mapping.items():
                                                    self.driver.get(_url)
                                                    time.sleep(5)
                                                    # Check if the CountryID exists in the 'KeypairCountry' dictionary
                                                    if f'Country {self.CountryID}' in KeypairCountry:
                                                        ### If the CountryID exists, get the SKU text for the corresponding country
                                                        sku = KeypairCountry[f'Country {self.CountryID}'][0]
                                                        # sku = "asin"
                                                        # Send the SKU text to the 'item_sku' input field using Selenium
                                                        sku_text = self.driver.find_elements(By.NAME, 'contribution_sku-0-value')[0].send_keys(sku)
                                                        time.sleep(2)
                                                        # Price
                                                        price = self.driver.find_element(by=By.CLASS_NAME,value='currency')
                                                        ##cur_price = KeypairCountry[f'Price {self.CountryID}'][0]
                                                        cur_price = price
                                                        currency = price.find_element(by=By.CLASS_NAME, value='standard-price-match-low').send_keys(asin_price)
                                                        time.sleep(2)
                                                        # self.driver.find_elements(By.CLASS_NAME, 'no-bottom-padding')[1].click()
                                                        self.driver.execute_script('document.querySelector("#offerFulfillment-AFN > span").click()')
                                                    else:
                                                        # If the CountryID does not exist in the 'KeypairCountry' dictionary, print an error message
                                                        print(f"No Data found for the ASIN {asin} in the db ")
                                                        self.post.ProcessErrorLog(self, 1, f"No Data found for the ASIN {asin} in the db")
                                                        self.mapp_relisted_items[asin] = False
                                                        continue
                                                    



                                                    #select country 
                                                    btn_check = self.driver.find_elements(by=By.TAG_NAME, value='kat-toggle')

                                                    countries = ["US", "Canada", "Mexico", "United Kingdom",
                                                                "Germany", "France", "Italy", "Spain", 
                                                                "Netherlands", "Turkey", "Belgium", "Sweden", 
                                                                "Poland", "Japan", "Australia",
                                                                "Singapore"]

                                                    def unclick_click_countries():

                                                        for index, country in enumerate(countries):
                                                            if btn_check[index].get_attribute('checked') == 'true':
                                                                print(f"{country} is selected", index)
                                                                if country != countries[0]:
                                                                    # time.sleep(1.3)
                                                                    self.driver.execute_script("arguments[0].scrollIntoView();", btn_check[index])
                                                                    try:
                                                                        btn_check[index].click()
                                                                    except:
                                                                        print("button not clickable for", country)


                                                    try:
                                                        unclick_click_countries()
                                                    except:
                                                        unclick_click_countries()

                                                    time.sleep(5)
                                                
                                                    #click on Save and Finish
                                                    savebtn = self.driver.find_element(by=By.ID, value='EditSaveAction')
                                                    try:
                                                        savebtn.click()
                                                    except:
                                                        print("Save button not clickable")
                                                        self.mapp_relisted_items[asin] = False

                                                    try:
                                                        self.driver.find_element(By.CLASS_NAME,'state-error').text.startswith("Because the SKU you entered is already")
                                                        # print("Sku already in used, will use different SKU")
                                                        if f'Country {self.CountryID}' in KeypairCountry:
                                                            # If the CountryID exists, get the SKU text for the corresponding country
                                                            sku = KeypairCountry[f'Country {self.CountryID}'][1]
                                                            # Send the SKU text to the 'item_sku' input field using Selenium
                                                            self.driver.refresh()
                                                            time.sleep(5)
                                                            # self.driver.find_element(by=By.ID, value='item_sku') = sku
                                                            sku_text = self.driver.find_element(by=By.ID, value='item_sku').send_keys(sku)
                                                            time.sleep(2)
                                                            # Price
                                                            price = self.driver.find_element(by=By.CLASS_NAME,value='currency')
                                                            cur_price = KeypairCountry[f'Price {self.CountryID}'][0]
                                                            currency = price.find_element(by=By.CLASS_NAME, value='standard-price-match-low').send_keys(cur_price)
                                                            #click on Save and Finish
                                                            savebtn = self.driver.find_element(by=By.ID, value='EditSaveAction')
                                                            try:
                                                                savebtn.click()
                                                            except:
                                                                print("Save button not clickable")
                                                                self.mapp_relisted_items[asin] = False

                                                        else:
                                                            # If the CountryID does not exist in the 'KeypairCountry' dictionary, print an error message
                                                            print(f"No Data found for the ASIN {asin} in the db ")
                                                            self.post.ProcessErrorLog(self, 1, f"No Data found for the ASIN {asin} in the db")
                                                            self.mapp_relisted_items[asin] = False
                                                            continue
                                                    except:
                                                        print("No secondary issue found for  different sku \n")

                                                    time.sleep(10)

                                                    #List as FBA and Send to Amazon BUTTON
                                                    try:    
                                                        self.driver.find_elements(by=By.XPATH, value='//*[@data-testid="button-label-for-SC_FBA_LFBA_1_PAGE_LIST_AS_FBA_BUTTON_CONVERTANDSEND"]')[0].click()
                                                    except:
                                                        try:
                                                            self.mapp_relisted_items[asin] = False
                                                        except:
                                                            try:
                                                                dangerous_btn = self.driver.find_elements_by_css_selector('[data-testid="dgq-button"]')
                                                                [i.click() for i in dangerous_btn]

                                                                no_buttons = self.driver.find_elements_by_xpath('//input[@class="kat-radio" and translate(@value,"abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ")="NO"]')
                                                                [i.get_attribute('value') for i in no_buttons]
                                                                for button in no_buttons:
                                                                    try:
                                                                        self.driver.execute_script("arguments[0].click();", button)
                                                                    except Exception as e:
                                                                        # Handle any exceptions that may occur
                                                                        print(f"Error clicking element: {e}")
                                                                self.driver.find_element_by_css_selector('kat-button[data-testid="dgq-modal-submit"]').click()
                                                                time.sleep(1)
                                                                self.driver.find_elements(by=By.XPATH, value='//*[@data-testid="button-label-for-SC_FBA_LFBA_1_PAGE_LIST_AS_FBA_BUTTON_CONVERTANDSEND"]')[0].click()
                                                            except:
                                                                ...
                                                        
                                                    time.sleep(5)
                                                    try:
                                                        self.driver.find_element(by=By.ID,value='D4NpU76_3nZowGQUcKsgw').click()
                                                    except:
                                                        self.mapp_relisted_items[asin] = False
                                                        ...
                                                    self.mapp_relisted_items[asin] = True
                                                    print(f"\nRelisted Asin {asin} for all skus mentioned above\n\n ")
                                                    self.post.ProcessErrorLog(self, 1, f"Relisted Asin {asin} for all skus mentioned above")
                                                    time.sleep(5)
                            
                            ## self.mapp_relisted_items = {i:True for i in  deleted_asins_to_be_relisted}
                            for asin, is_relisted in self.mapp_relisted_items.items():
                                if is_relisted:
                                    Re_listed.append(asin)
                                else:
                                    non_listed.append(asin)
                        else:
                            print("Invalid CountryID.")
                            self.mapp_relisted_items[asin] = False
                        
                    print("\nRelisting completed for all the asins\n")
                    self.post.ProcessErrorLog(self, 1, f"Relisting completed for all the asins")

                except Exception as e:
                    print(e)
                    self.mapp_relisted_items[asin] = False
                    print("Couldnt relist asin", asin)
                    self.post.ProcessErrorLog(self, 2, f"Couldnt relist asin {asin}  ,  { str(self.mapp_relisted_items) }")

            Re_listed = list(set(Re_listed))
            if self.gsheetData_job_log['Total_Re_listed'].iloc[current_row] == 0:
                Previous_re_listed_total +=  [i for i in Total_ExtraAsins if i in Re_listed  ]
            else: 
                Previous_re_listed_total =  self.gsheetData_job_log['Total_Re_listed'].iloc[current_row].split(' ')
            Total_Re_listed = set(Previous_re_listed_total)
            Total_Re_listed = list(Total_Re_listed)
            Vl_Remaining = [i for i in Total_ExtraAsins if i not in Re_listed]
            if not Vl_Remaining : Vl_Remaining = " "

            
            
            cellsASIN=[]
            _True_Parent_ASIN = self.gsheetData_job_log.columns.get_loc('True Parent ASIN')  + 1
            _False_Parent_ASIN = self.gsheetData_job_log.columns.get_loc('False Parent ASIN')  + 1
            _ExtraAsins_from_VL = self.gsheetData_job_log.columns.get_loc('ExtraAsins from VL')  + 1
            _Total_ExtraAsins = self.gsheetData_job_log.columns.get_loc('Total_ExtraAsins')  + 1
            _Re_listed = self.gsheetData_job_log.columns.get_loc('Re_listed')  + 1
            _Total_Re_listed = self.gsheetData_job_log.columns.get_loc('Total_Re_listed')  + 1
            _Vl_Remaining = self.gsheetData_job_log.columns.get_loc('Vl_Remaining')  + 1

            cellsASIN.append(Cell(row = current_row + 2, col = _True_Parent_ASIN , value =  self.ParentTrueFalse['ParentTrue'] ))
            cellsASIN.append(Cell(row = current_row + 2, col = _False_Parent_ASIN , value =  self.ParentTrueFalse['ParentFalse'] ))
            cellsASIN.append(Cell(row = current_row + 2, col = _ExtraAsins_from_VL , value =  ' '.join(ExtraAsins) ))
            cellsASIN.append(Cell(row = current_row + 2, col = _Total_ExtraAsins , value =  ' '.join(Total_ExtraAsins)  ))
            cellsASIN.append(Cell(row = current_row + 2, col = _Re_listed , value =  ' '.join(deleted_asins_to_be_relisted)))
            cellsASIN.append(Cell(row = current_row + 2, col = _Total_Re_listed , value =  ' '.join(Total_Re_listed) ))
            cellsASIN.append(Cell(row = current_row + 2, col = _Vl_Remaining , value =  ' '.join(Vl_Remaining)  ))

            print('Relisting completed ') if asins else print("No extra asins found to be relisted , moving ahead "); self.post.ProcessErrorLog(self, 1, " No extra asins found to be relisted , moving ahead "  )
            self.post.ProcessErrorLog(self, 1, f" Relisting completed { str(self.mapp_relisted_items)  } ")
    
            self.gsheet_job_log_Update.update_cells(cellsASIN) 
        

        except Exception as e:
            print('\nIssue in relisting items, check for the attributes places in the job log sheet  ')
            self.post.ProcessErrorLog(self, 2, f"Issue in relisting items | check for the attributes places in the job log sheet | {str(e)}")

    def seller_support_case(self, asin, subject, all_child_asins=[], missing_asins_text = None, Child_ASINs = None, count_of_asins = None, batch_id = None):

        try:    
            

            self.driver.get("https://sellercentral.amazon.com/home?mons_sel_dir_mcid=amzn1.merchant.d.ADVSOBI7NLBGFP3CTZPHOFNEOKCA&mons_sel_mkid=A1F83G8C2ARO7P&mons_sel_dir_paid=amzn1.pa.d.ACK2GASJ5Y6PL7M4KUAMRCL7EO2A&ignore_selection_changed=true&mons_redirect=change_domain")
            sleep(3)

            #driver.switch_to.window(driver.window_handles[0])
            self.driver.get("https://sellercentral.amazon.com/help/hub/support/INTENT_CTI_PSS")
            sleep(5)
            
            if all_child_asins:
                print("TxT for Extra Asins")
                txt ="Hello Amazon Support, \n\n"
                txt = txt + "Please find the below ASINs and help split from Variation listing as we can't remove by ourselves. \n"
                txt = txt + "Please take note: \n\n"
                txt = txt + "1. These are the ONLY CHILDs that needs to be removed from the existing Parent \n"
                txt = txt + "2. DO NOT remove other CHILDs that are not listed below from existing Parent \n"
                txt = txt + "3. Please Do Not break the existing Variation Lisitng \n"
                txt = txt + f"Parent ASIN: {asin}\n"
                txt = txt + f"Child ASINs: {', '.join(all_child_asins)}\n"
                txt = txt + "Thanks, \n"
                txt = txt + "Alex"
                txt = txt.replace('@ASIN', asin)
                print(txt)
                self.post.ProcessErrorLog(self, 1, txt)
            
            elif missing_asins_text is not None:
                print("txt for Missing Asins")
                txt ="Hello Amazon, \n\n"
                txt = txt + f"After uploaded Flat file to add {count_of_asins} ASINs into Parent ASIN {asin} variation listing, \n"
                txt = txt + f" uploaded successfully but not reflected on live site, please review and help fix\n"
                txt = txt + "1. These are the ONLY CHILDs that needs to be added in the existing Parent \n"
                txt = txt + "2. Please Do Not break the existing Variation Lisitng \n"
                txt = txt + f"Batch id: {batch_id}\n"
                txt = txt + "Thanks, \n"
                txt = txt + "Alex"
                txt = txt.replace('@ASIN', asin)
                print(txt)
                self.post.ProcessErrorLog(self, 1, txt)

            else:
                print("Txt for Parent Asins  with or without SKU ")
                txt ="Hello Amazon Support, \n\n"
                txt = txt + "Please find the below ASINs and help Delete from Variation listing as we can't remove by ourselves. \n"
                txt = txt + f"Parent ASIN: {asin}\n"
                txt = txt + f"Child ASINs: {' '.join(Child_ASINs)}\n"
                txt = txt + "Thanks, \n"
                txt = txt + "Alex"
                txt = txt.replace('@ASIN', asin)
                print(txt)
                self.post.ProcessErrorLog(self, 1, txt)


            #Not listed issue btn
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
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


            #Continue btn
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
            continue_button_script = '''
                var mainFrame = document.querySelector("#mons-body-container").contentWindow;
                var continueButtonSelector = "#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div.button-options > kat-button";
                var continueButton = mainFrame.document.querySelector(continueButtonSelector);
                continueButton.click();
            '''
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
            self.driver.execute_script( continue_button_script)
                
            time.sleep(3)
        
            ## issus not listed
            self.driver.execute_script( 'document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div > div > div > div > div.button-options > kat-button:nth-child(4) > div").click()')
            time.sleep(2)
            
            ## Account related
            self.driver.execute_script( 'document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div > div > div:nth-child(2) > div > div.button-options > kat-button:nth-child(1) > div > div").click()' )
            time.sleep(3)
            self.driver.execute_script("window.scrollBy(0, 1000)") 
            ### Provide subject in textbox   
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

            
            time.sleep(3)

            ### send button clicked 
            for _ in range(7):
                time.sleep(2)
                actions = ActionChains(self.driver) 
                actions.send_keys(Keys.TAB )
                actions.perform()

            time.sleep(2)
            
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.ENTER )
            actions.perform()

            sleep(15)
            ### Extract the case id
            try:
                
                caseid = 'caseid = document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(3) > div > div > div:nth-child(2) > div > div > div > div.meld-case-created-outer-container > div > div > p:nth-child(2) > a").textContent ; '
                caseid += 'return caseid ;'
                caseid = self.driver.execute_script(caseid)
                print(caseid)
                self.post.ProcessErrorLog(self, 1, f" case id = {caseid } ")
                _ManualLog = caseid
                self._ManualLog = caseid
            except:
                
                caseid = 'caseid = document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(4) > div > div > div:nth-child(2) > div > div > div > div.meld-case-created-outer-container > div > div > p:nth-child(2) > a").textContent ; '
                caseid += 'return caseid ;'
                caseid = self.driver.execute_script(caseid)
                print(caseid)
                self.post.ProcessErrorLog(self, 1, f" case id = {caseid } ")
                _ManualLog = caseid
                self._ManualLog = caseid
        
            return _ManualLog
        
        except Exception as err:  
            print(str(err))
            self.post.ProcessErrorLog(self, 2, f"  Error Case Log PSS ")
            _ManualLog = "Error Case Log PSS"
            return False
    
    def generate_email_html(self, case_id, subject, asin, parent_sku, sku_line):
            """
                Html template for Extra Asins
            """
            try:

                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                table {{
                    border-collapse: collapse;
                    border: 4px solid black;
                    width: 100%;
                }}
                th, td {{
                    border: 4px solid black;
                    padding: 9px;
                    text-align: left;
                }}
                th {{
                    background-color: black;
                    color: white;
                }}
                </style>
                </head>
                <body>

                <div> <br><br>

                Hello SAS Team,\n<br>

                We found that we can't split child ASINs from our Parent ASIN {asin} with Parent SKU {parent_sku} as they're grouped by Amazon automatically, not by ourselves.\n<br>
                We have contacted SAS operations & Seller Support - they cannot address the request as they came back with a reply that it is out of their Scope.\n<br>
                <br>
                Please take note:\n<br>

                1. These are the ONLY CHILDs that needs to be removed from the existing Parent\n<br>
                2. DO NOT remove other CHILDs that are not listed below from existing Parent\n<br>
                3. Please Do Not break the existing Variation Lisitng<br><br>
                \n
                Regards,\n<br>
                STI Int\n<br>
            </div>

                <br><br><br>

                <br><br><br>

                <table>
                <tr>
                    <th  style="background-color: black; color: white; padding: 10px; text-align: center;">Issue Submission Email Form</th>
                    <th ></th>
                </tr>
                <tr>
                    <td>Subject/Headline</td>
                    <td>Child ASINs Can't Split from Parent ASIN {asin} - Parent SKU {parent_sku}</td>
                </tr>
                <tr>
                    <td>Merchant Token</td>
                    <td>A31LSP1L7F6XJ2</td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td>Alex</td>
                </tr>
                <tr>
                    <td>Seller Email</td>
                    <td>alex.ho@sti-aromas.com</td>
                </tr>
                <tr>
                    <td>Seller Phone Number</td>
                    <td>852-56163656</td>
                </tr>
                <tr>
                    <td>Issue Details :</td>
                    <td>
                    <ul>
                        <li>{sku_line}</li>
                    </ul>
                </td>
                </tr>
                <tr>
                    <td>What Steps/Actions Taken have been taken so far ?</td>
                    <td>
                        <ul>
                            <li>Opened case to ask for assistance but still not solved, case id: {case_id}</li>
                            <li>Opened case to ask SAS team for assistance but no reply, email subject: {subject}</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>What is your Desired Result ?</td>
                    <td>
                        <ul>
                            <li> Remove the attached Child ASINs from the variation listing as we are unable to remove by ourselves.</li>
                            <li> ONLY need to remove these ASINs from variation listing, NOT break all variants to keep all child ASINs in single. </li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>Related case(s) (if applicable)</td>
                    <td>{case_id}</td>
                </tr>
                <tr>
                    <td>Is the appeal or related Documents Attached ?(if applicable)</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td>Account Manager Email</td>
                    <td>
                        <ul>
                            <li>joewin@amazon.com</li>
                            <li>anramrod@amazon.com</li>
                        </ul>
                    </td>
                </tr>
                </table>

                </body>
                </html>
                """
                
                return html
            
            except:
                self.post.ProcessErrorLog(self, 2, f"  Issue in Creating HTML Template for Extra Asins ")
        
    def generate_email_html_missing_asin(self, case_id, subject, asin, parent_sku, headline = '', count_ = '', sku_line = '', batch_id = '' ):
            """
                Html template for Missing Asins
            """
            try:
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                table {{
                    border-collapse: collapse;
                    border: 4px solid black;
                    width: 100%;
                }}
                th, td {{
                    border: 4px solid black;
                    padding: 9px;
                    text-align: left;
                }}
                th {{
                    background-color: black;
                    color: white;
                }}
                </style>
                </head>
                <body>

                <div> <br><br>
       
                Hi SAS Team,<br>
                I see that ASIN {asin}, contains Historical Records of an OLD Variation SKU under Edit Listing > Variation Tab as shown in Screen Capture.<br>Please assist to STICKY DELETE the old records circled in red SKU: {parent_sku} from my ASIN {asin}.
                <br>We have contacted Amazon Support Team and SAS team about this but it is still NOT solved.<br>
                Please see details below and assist.


                </div>

                <br><br><br>

                <br><br><br>

                <table>
                <tr>
                    <th  style="background-color: black; color: white; padding: 10px; text-align: center;">Issue Submission Email Form</th>
                    <th ></th>
                </tr>
                <tr>
                    <td>Subject/Headline</td>
                    <td>{headline}</td>
                </tr>
                <tr>
                    <td>Merchant Token</td>
                    <td>A31LSP1L7F6XJ2</td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td>Alex</td>
                </tr>
                <tr>
                    <td>Seller Email</td>
                    <td>alex.ho@sti-aromas.com</td>
                </tr>
                <tr>
                    <td>Seller Phone Number</td>
                    <td>852-56163656</td>
                </tr>
                <tr>
                    <td>Issue Details :</td>
                    <td>
                    <ul>
                        <li>{sku_line}</li>
                        <li>updated whole variation listing {count_} ASINs via uploading flat file, successful but not reflect on live site, batch id:{batch_id}</li>
                    </ul>
                </td>
                </tr>
                <tr>
                    <td>What Steps/Actions Taken have been taken so far ?</td>
                    <td>
                        <ul>
                            <li>open support case but not work, case id:  {case_id}</li>
                            <li>opened case to ask SAS team to assistance but not reply</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>What is your Desired Result ?</td>
                    <td>
                        <ul>
                            <li> 1.	Added {count_} child ASINs into variation listing and keep {count_} ASINs into VL stable.(Please refer the attachment).</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>Related case(s) (if applicable)</td>
                    <td>{case_id}</td>
                </tr>
                <tr>
                    <td>Is the appeal or related Documents Attached ?(if applicable)</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td>Account Manager Email</td>
                    <td>
                        <ul>
                            <li>anramrod@amazon.com</li>
                        </ul>
                    </td>
                </tr>
                </table>

                </body>
                </html>
                """
                return html
            except:
                      self.post.ProcessErrorLog(self, 2, f"  Issue in Creating HTML Template for Missing Asins ")

    def generate__html_VL_Deletion(self, case_id, line, asin, parent_sku, headline, child_Asins):
            """
                Html template for False Parent Asin with and without SKU
            """
            try:
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                table {{
                    border-collapse: collapse;
                    border: 4px solid black;
                    width: 100%;
                }}
                th, td {{
                    border: 4px solid black;
                    padding: 9px;
                    text-align: left;
                }}
                th {{
                    background-color: black;
                    color: white;
                }}
                </style>
                </head>
                <body>

                <div> <br><br>

                Hi SAS Team,<br>


                We found that we can't split child ASINs from our Parent ASIN  {asin}  {'without Parent SKU' if line.startswith('No') else line + parent_sku}.
                <br>We have contacted Amazon Support Team and SAS team about this but it is still NOT solved.<br>
                <br>
                Please see details below and assist.

            </div>

                <br><br><br>

                <br><br><br>

                <table>
                <tr>
                    <th  style="background-color: black; color: white; padding: 10px; text-align: center;">Issue Submission Email Form</th>
                    <th ></th>
                </tr>
                <tr>
                    <td>Subject/Headline</td>
                    <td>{headline} </td>
                </tr>
                <tr>
                    <td>Merchant Token</td>
                    <td>A31LSP1L7F6XJ2</td>
                </tr>
                <tr>
                    <td>Contact Name</td>
                    <td>Alex</td>
                </tr>
                <tr>
                    <td>Seller Email</td>
                    <td>alex.ho@sti-aromas.com</td>
                </tr>
                <tr>
                    <td>Seller Phone Number</td>
                    <td>852-56163656</td>
                </tr>
                <tr>
                    <td>Issue Details :</td>
                    <td>
                    <ul>
                        <li>Parent {asin} -> {line} </li>
                        <li>Unable to split Child ASIN(s):{child_Asins}</li>
                        <li>Parent LMNO -> {line}</li>
                    </ul>
                </td>
                </tr>
                <tr>
                    <td>What Steps/Actions Taken have been taken so far ?</td>
                    <td>
                        <ul>
                            <li>Opened Multiple cases on Seller Support & SAS Operations for assistance however they are unable to resolve issue as suggested this is not a feature that they can work on</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>What is your Desired Result ?</td>
                    <td>
                        <ul>
                            <li>Split all child ASINs into single listing that we can add into our ideal variation listing.</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td>Related case(s) (if applicable)</td>
                    <td>{case_id}</td>
                </tr>
                <tr>
                    <td>Is the appeal or related Documents Attached ?(if applicable)</td>
                    <td>Yes</td>
                </tr>
                <tr>
                    <td>Account Manager Email</td>
                    <td>
                        <ul>
                            <li>anramrod@amazon.com</li>
                        </ul>
                    </td>
                </tr>
                </table>

                </body>
                </html>
                """
                return html
            except:
                self.post.ProcessErrorLog(self, 2, f"  Issue in Creating HTML Template for Parent Asins ")

    def inform_users_via_mail(self, subject, body, me=False, file_path = None, product_name = None):

        """
            Informing Users via Mail 
        """
        
        today =  date.today()
        #body = "This is an email with attachment sent from Python"
        sender_email = "rebecca.dark@sti-aromas.com"
        cc_email = []
        receiver_email = "lizzypan@sti-aromas.com" # inform USER 
        password = '#Gya12341'
        if product_name:
            cc_email = ['gyalabs.it29@gmail.com', "gaurav.k.gosain@sti-aromas.com"]
        else:
            cc_email = ["gyalabs.it29@gmail.com"]

        if me: 
            receiver_email = 'tusharmalhan@gmail.com'

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Cc"] = ", ".join(cc_email) if isinstance(cc_email, list) else cc_email
        message["Subject"] = subject
        text = body

        message["Subject"] = subject
        part1 = MIMEText(text, "plain")
        message.attach(part1)
        
        if file_path:
            with open(file_path, 'rb') as attachment:
                part2 = MIMEBase('application', 'octet-stream')
                part2.set_payload(attachment.read())
                encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', f'attachment; filename = template_{self.VL_Name}__{self.today.strftime("%y-%m-%d")}.xlsx')
                message.attach(part2)
               
        text = message.as_string()
        session = smtplib.SMTP('smtp-legacy.office365.com', 587)
        session.starttls()
        session.login(sender_email, password)
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
        print('Informed User via email \n')
        self.post.ProcessErrorLog(self, 1, f"  Informed User via email  ")

        return subject

    def SAS_issue_assistance(self, asin, case_id, subject, mail_type = "Email", file_path = None, 
                            sku_line = None, parent_sku = None, 
                            missing_asins_text = None, headline = None, 
                            count_ = None, True_parent = None, line = "with Parent SKU " ,
                            child_Asins = None, batch_id = None):
        
        """
            Send email with both options 
            - with HTML TEMPLATE
            - and Email format
        """
        
        try:
            today =  date.today()
            #body = "This is an email with attachment sent from Python"
            sender_email = "rebecca.dark@sti-aromas.com"
            receiver_email ="sasoperations@amazon.com" #"Vinod.sharma@sti-aromas.com" 
            # receiver_email = "lizzypan@sti-aromas.com" #"Vinod.sharma@sti-aromas.com" 
            # receiver_email = "gyalabs.it29@gmail.com"
            password = '#Gya12341'

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            
            if mail_type == "Email":
                ###  template for  EXTRA Asins
                if  not missing_asins_text and not True_parent:
                    print(True_parent)
                    text  = f"""
Hello SAS Team,

We found that we can’t split child ASINs from our Parent ASIN {asin} with Parent SKU {parent_sku} as they’re grouped by Amazon automatically, not by ourselves.

We have attached a file with a list of Child ASINs that we require being removed from its existing Parent.
We require these Childs as STAND ALONEs and since we are unable to remove these ourselves, we are seeking assistance from your end.

Please take note:
1. These are the ONLY CHILDs that needs to be removed from the existing Parent
2. DO NOT remove other CHILDs that are not listed below from existing Parent
3. Please Do Not break the existing Variation Lisitng
\n
Regards,
STI Int

                """
                
                ### template for Parent Asin with and without SKU
                elif True_parent   :
                    text = f"""
Hello SAS Team,

Please find the attached file and split child ASINs from Parent ASIN  {asin} from variation listing as we can't delete by ourselves. 

Thanks.
Best Regards, 

"""
                ### template for Missing Asins
                else:
                    text = f""" 

Dear SAS Support,

I see that ASIN {asin}, contains Historical Records of an OLD Variation SKU under Edit Listing > Variation Tab as shown in Screen Capture.
Please assist to STICKY DELETE the old records circled in red SKU: {parent_sku} from my ASIN  {asin}.

Regards
Alex 

                """
                
                subject +=" SAS-IO"
                message["Subject"] = subject
                part1 = MIMEText(text, "plain")
                message.attach(part1)
                with open(file_path, 'rb') as attachment:
                        part2 = MIMEBase('application', 'octet-stream')
                        part2.set_payload(attachment.read())
                        encoders.encode_base64(part2)
                        part2.add_header('Content-Disposition', f'attachment; filename= SAS_{asin}__{self.today.strftime("%y-%m-%d")}.xlsx')
                        message.attach(part2)
                        
                text = message.as_string()
                session = smtplib.SMTP('smtp-legacy.office365.com', 587)
                session.starttls()
                session.login(sender_email, password)
                session.sendmail(sender_email, receiver_email, text)
                session.quit()
                print('Email Sent Successfully\n')
                return subject

            else:
                subject.replace(" SAS-IO",'')
                subject+=" SAS-IA"
                
                message["Subject"] = subject
                
                ### HTML template for extra asins
                if not missing_asins_text and not True_parent: 
                    email_html = self.generate_email_html(case_id, subject, asin, parent_sku, sku_line = sku_line)
                
                ### HTML template for Parent asins with and without sku
                elif True_parent :
                    email_html = self.generate__html_VL_Deletion(case_id, line, asin, parent_sku = parent_sku, headline= headline, child_Asins=child_Asins)
                
                else:
                    ### HTML template for inactive missing asins
                    if missing_asins_text.startswith("IN"):
                        email_html = self.generate_email_html_missing_asin(case_id, subject, asin, parent_sku,headline=headline,count_ = count_, sku_line = sku_line, batch_id = batch_id)
                    else:
                        ### HTML template for active missing asins
                        email_html = self.generate_email_html_missing_asin(case_id, subject, asin, parent_sku,headline=headline,count_ = count_, sku_line = sku_line, batch_id = batch_id)
                part2 = MIMEText(email_html, "html")
                message.attach(part2)

                with open(file_path, 'rb') as attachment:
                        excel_file = MIMEBase('application', 'octet-stream')
                        excel_file.set_payload(attachment.read())
                        encoders.encode_base64(excel_file)
                        excel_file.add_header('Content-Disposition', f'attachment; filename= SAS_{asin}__{self.today.strftime("%y-%m-%d")}.xlsx')
                        message.attach(excel_file)
                        
                text = message.as_string()
                session = smtplib.SMTP('smtp-legacy.office365.com', 587) #use gmail with port
                session.starttls() #enable security
                session.login(sender_email, password) #login with mail_id and password
                session.sendmail(sender_email, receiver_email, text)
                session.quit()
                print('HTML Template Mail Sent Sucessfully \n')
                return subject

        except Exception as err:  
            print(" Error Send Mail PSS SAS AMZ_CatalogAttribute",str(err)) 
            self.post.ProcessErrorLog(self, 2, f"  Error Send Mail PSS SAS AMZ_CatalogAttribute - SAS_issue_assistance ")
            return False

    def recheck_email_case(self, subject):

        try:
            self._ManualLog = ''
            self.driver.get("https://sellercentral.amazon.com/cu/case-lobby?ref=xx_caselog_count_home")
            sleep(3)
            
            table = self.driver.find_element(by = By.XPATH, value='//*[@role="rowgroup"]')
            tablerows = table.find_elements(by = By.XPATH, value='//*[@role="row"]')
            searchcaseid = tablerows[0].find_element(by = By.XPATH, value='//*[@type="search"]')
            subject = subject 
            searchcaseid.send_keys(subject)#############
            sleep(2)
            searchbtn = tablerows[0].find_elements(by = By.XPATH, value='//*[@label="Go"]')
            searchbtn[0].click()
            sleep(2)
            displaylist = self.driver.find_elements(by = By.XPATH, value='//*[@role="cell"]')
            if (displaylist[2].text != 'Displaying\n0\nto\n0\nof 0'):
                caselist = self.driver.find_elements(by = By.CLASS_NAME, value='hill-case-lobby-search-results-panel')
                CaseID = caselist[0].find_element(by = By.CLASS_NAME, value='hill-case-lobby-search-results-panel-caseId').text
                self._ManualLog = CaseID
                self.post.ProcessErrorLog(self, 1, f" Got Case ID by Rechecking Email Case")
                return CaseID
            # else:
            #     return False
        
        except Exception as err:  
            self._ManualLog = ""
            print("Error in Release",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Error in Release email case - recheck_email_case() " + str(err)) 
            return False

    def create_SAS_case(self, parent_asin, all_child_asins):

        """
            SAS case  file for Extra asins
        """
        try:

            try:           
                wb_append = xw.Book(self.Excel_file_path)
            except:
                print("Close the other original excel sheets or related to it. ")
                self.post.ProcessErrorLog(self, 1, f"Close the other original excel sheets or related to it.")

            sheet = wb_append.sheets['Template - Variations Update']
            parent_skus = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == parent_asin)]['SKU'].iloc[0]
            next_row = 13
            for child_asin in all_child_asins: 
                child_asin_skus=[]
                para = {    
                    "data" : {"userid":2, "ASIN": child_asin, "CountryID": self.CountryID,"table": "Product_Master_Details_ByASINAll" },
                    "type":"Select"
                }
                post = PostFun() 
                skujson = post.PostApiParaJson(para)
                for val in skujson['data']['input']:
                    if val['GroupName'] !='Info':
                        for valupdate in val['data']:                         
                            if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                child_asin_skus.append(valupdate['data']['updatedvalue'])
                for sku in child_asin_skus:
                    sheet.cells(next_row, 2).value = child_asin
                    sheet.cells(next_row, 3).value = sku
                    sheet.cells(next_row, 4).value = parent_skus
                    sheet.cells(next_row, 5).value = parent_asin
                    sheet.cells(next_row, 6).value = "Size-Scent"
                    sheet.cells(next_row, 7).value = 'Delete SKU from Variation Listing'
                    sheet.cells(next_row, 8).value = ""
                    sheet.cells(next_row, 9).value = ""
                    sheet.cells(next_row, 10).value = "Yes"
                    next_row += 1
            file_path = f"{self.SFTPLocation}\\SAS_{parent_asin}__{self.VL_Name}_{self.today.strftime('%Y-%m-%d')}.xlsx"
            wb_append.save(file_path)
            wb_append.app.quit()
            print("DONE EDITING EXCEL FILE of SAS case for Extra asins \n")        
            self.post.ProcessErrorLog(self, 1, f"SAS case for Extra asins")
            return file_path      
          
        except:
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating SAS CASE for extra asins - create_SAS_case ")
   
    def Create_ExtraChildASINDelete_Support_SAS_Case(self):
        """
            ### GET child skus mapped with each  Child Asin
        """

        try:
            ### for READING , we dont append numeric 2 to the last row ,while updating entries we do !!
            current_row = self.gsheetData_job_log.index[-1] 
            gsheetLog =  self.gsheetData_job_log.iloc[-1] 
        

            if self.ExtraASINs:
                
                self.post.ProcessErrorLog(self, 1, f" Extra asins found, going for SAS if time exceeds ")
                if gsheetLog['Extra Upload'] == 'Upload' and  gsheetLog['EXTRA SAS - SELLER SUPPORT'] =='' :
                  
                    last_row_timing = gsheetLog['Time Extra Delete Upload']
                    last_row_datetime = datetime.strptime(last_row_timing, '%Y-%m-%d %H:%M')        
                    current_datetime = datetime.now()
                    time_difference = current_datetime - last_row_datetime
                    if time_difference > timedelta(hours=self.Sas_create_time) :
                        print(f"The date is more than {self.Sas_create_time} hours ago. gonna send the SAS cases for extra asins !\n")
                        self.post.ProcessErrorLog(self, 1, f"The date is more than {self.Sas_create_time}  hours ago. gonna send the SAS cases for extra asins")


                        for parent_asin in  list(self.VLList['RequestASIN'].unique()):        
                            all_child_asins = list(self.VLList[(self.VLList['RequestASIN'] == parent_asin ) & (self.VLList['ASIN'].isin(self.ExtraASINs))]['ASIN'].unique())
                            parent_skus = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == parent_asin)]['SKU'].iloc[0]
                            print(parent_asin, parent_skus, all_child_asins)
                            self.post.ProcessErrorLog(self, 1,"Parent Extra Child : " + parent_asin + ' '+  parent_skus + ' '+ ",".join(all_child_asins))
                            
                        
                            subject =  f"Amazon_Variations_A31LSP1L7F6XJ2_ from Parent ASIN - {parent_asin}"+ '  '+"Parent SKU - " + parent_skus + '__' + self.today.strftime("%y-%m-%d") + '- Extra Asins '
                            case_ID_generated = self.seller_support_case(parent_asin, subject,  all_child_asins = all_child_asins)
                            if not case_ID_generated: self.post.ProcessErrorLog(self, 2, f"Issue in creating seller support case id "); print('\nIssue in creating seller support case id ')
                            file_path = self.create_SAS_case(parent_asin, all_child_asins)
                            if  parent_skus == '':
                                sku_line = f"Can't split child ASINs from Parent ASIN {parent_asin} without Parent SKU"    
                            else:
                                sku_line = f"Can't split child ASINs from Parent ASIN {parent_asin} - Parent SKU {parent_skus}"
                            
                            self.SAS_IO_Subject = self.SAS_issue_assistance(parent_asin, case_ID_generated, subject, mail_type="Email" , 
                                                                            file_path = file_path, sku_line = sku_line, parent_sku = parent_skus)
                            self.SAS_IA_Subject = self.SAS_issue_assistance(parent_asin, case_ID_generated, subject, mail_type="HTML", 
                                                                            file_path = file_path, sku_line = sku_line, parent_sku = parent_skus )

                            print(  self.SAS_IO_Subject )
                            print(  self.SAS_IA_Subject )
                            print("Created Seller Support Cases For Extra Asins.\t")
                            self.post.ProcessErrorLog(self, 1, f"Created SAS Cases For Extra Asins")
                            self.post.ProcessErrorLog(self, 1, "SAS CaseID :" + case_ID_generated  + " SAS_IO_Subject :" +  self.SAS_IO_Subject + " SAS_IA_Subject :" + self.SAS_IA_Subject)

                    ### for READING , we dont append numeric 2 to the last row ,while updating entries we do !!
                    cellsASIN=[]
                    _CaseID = self.gsheetData_job_log.columns.get_loc('EXTRA SAS - SELLER SUPPORT')  + 1
                    _SASIO = self.gsheetData_job_log.columns.get_loc('EXTRA SAS - IO')  + 1
                    _SASIA = self.gsheetData_job_log.columns.get_loc('EXTRA SAS - IA')  + 1
                    cellsASIN.append(Cell(row = current_row + 2 , col = _CaseID, value =  case_ID_generated ))
                    cellsASIN.append(Cell(row = current_row + 2, col = _SASIA, value =  self.SAS_IA_Subject ))
                    cellsASIN.append(Cell(row = current_row + 2, col = _SASIO, value =  self.SAS_IO_Subject ))                    
                    self.gsheet_job_log_Update.update_cells(cellsASIN) 

            return True
        
        except Exception as e:
            self.post.ProcessErrorLog(self, 2, f" Issue in Implimenting  method  in extra asins -Create_ExtraChildASINDelete_Support_SAS_Case-> {str(e)}   ")

    def update_sas_caseid(self):
        
        try:

            cellsASIN=[]

            _Extra_SASIO = self.gsheetData_job_log.columns.get_loc('EXTRA SAS - IO')  + 1
            _Extra_SASIA = self.gsheetData_job_log.columns.get_loc('EXTRA SAS - IA')  + 1
            
            _SASIO_missing_asins_matching = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IO_Matching')  + 1
            _SASIA_missing_asins_matching = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IA_Matching')  + 1

            
            _SASIO_parent_sku_IO = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IO_UnMatching')  + 1
            _SASIA_parent_sku_IA = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IA_UnMatching')  + 1

            _SASIO_non_parent_sku_IO  = self.gsheetData_job_log.columns.get_loc('FALSE VL WITH SKU SAS  - IA')  + 1
            _SASIA_non_parent_sku_IA = self.gsheetData_job_log.columns.get_loc('FALSE VL WITH SKU  - IO')  + 1

            _SASIO_non_parent_sku_IO  = self.gsheetData_job_log.columns.get_loc('FALSE VL WITHOUT SKUSAS  - IO')  + 1
            _SASIA_non_parent_sku_IA = self.gsheetData_job_log.columns.get_loc('FALSE VL WITHOUT SKU SAS  - IA')  + 1

            # gsheetData_job_log = gsheetData_job_log[-1:]

            _gsheetLog = self.gsheetData_job_log[-1:]

            #     (self.gsheetData_job_log['EXTRA SAS - IA'].str.contains('Amazon_Variations')) | 
            #     (self.gsheetData_job_log['EXTRA SAS - IO'].str.contains('Amazon_Variations')) |


            #     (self.gsheetData_job_log['FALSE VL WITH SKU  - IO'].str.contains('Amazon_Variations')) | 
            #     (self.gsheetData_job_log['FALSE VL WITH SKU SAS  - IA'].str.contains('Child')) |

            #     (self.gsheetData_job_log['FALSE VL WITHOUT SKUSAS  - IO'].str.contains('Amazon_Variations'))|
            #     (self.gsheetData_job_log['FALSE VL WITHOUT SKU SAS  - IA'].str.contains('Child')) | 

            #     (self.gsheetData_job_log['Missing_case_SAS_IO_Matching'].str.contains('Amazon_Variations'))|
            #     (self.gsheetData_job_log['Missing_case_SAS_IA_Matching'].str.contains(f"Amazon_Variations")) | 

            #     (self.gsheetData_job_log['Missing_case_SAS_IA_UnMatching'].str.contains('Child')) | 
            #     (self.gsheetData_job_log['Missing_case_SAS_IO_UnMatching'].str.contains('Child'))
            #     ]

            for index, _rowsas in _gsheetLog.iterrows():
               
                
                _rowsas['EXTRA SAS - IA']  = str(_rowsas['EXTRA SAS - IA'] )
                _rowsas['EXTRA SAS - IO']  = str(_rowsas['EXTRA SAS - IO'] )

                _rowsas['Missing_case_SAS_IO_Matching'] = str(_rowsas['Missing_case_SAS_IO_Matching'])
                _rowsas['Missing_case_SAS_IA_Matching'] = str(_rowsas['Missing_case_SAS_IA_Matching'])
                
                _rowsas['Missing_case_SAS_IO_UnMatching']  = str(_rowsas['Missing_case_SAS_IO_UnMatching'] )
                _rowsas['Missing_case_SAS_IA_UnMatching']  = str(_rowsas['Missing_case_SAS_IA_UnMatching'] )
                
                _rowsas['FALSE VL WITH SKU  - IO']   = str(_rowsas['FALSE VL WITH SKU  - IO']  )
                _rowsas['FALSE VL WITH SKU SAS  - IA']   = str(_rowsas['FALSE VL WITH SKU SAS  - IA']  )

                _rowsas['FALSE VL WITHOUT SKUSAS  - IO']   = str(_rowsas['FALSE VL WITHOUT SKUSAS  - IO']  )
                _rowsas['FALSE VL WITHOUT SKU SAS  - IA']   = str(_rowsas['FALSE VL WITHOUT SKU SAS  - IA']  )
                
                



                ### For Extra Asins
                if 'Amazon_Variations' in _rowsas['EXTRA SAS - IA'] :
                    self.recheck_email_case(_rowsas['EXTRA SAS - IA'])
                    self.SAS_IA_Subject = self._ManualLog
                    if self.SAS_IA_Subject !='':
                        print('Case Id IA registered successfully');self.post.ProcessErrorLog(self, 1, "Case Id IA registered successfully ")
                        cellsASIN.append(Cell(row = index + 2, col = _Extra_SASIA, value =  self.SAS_IA_Subject ))
                    else:
                        print("Case ID Not found  for extra asins !")
                        self.post.ProcessErrorLog(self, 1, "Missing_case_ not found IO for extra asins !")

                if 'Amazon_Variations' in _rowsas['EXTRA SAS - IO'] :    
                    self.recheck_email_case(_rowsas['EXTRA SAS - IO'])
                    self.SAS_IO_Subject = self._ManualLog   
                    if self.SAS_IO_Subject !='':
                        cellsASIN.append(Cell(row = index + 2, col = _Extra_SASIO, value =  self.SAS_IO_Subject ))
                        print('Case Id IO registered successfully');self.post.ProcessErrorLog(self, 1, "Case Id IO registered successfully ")
                    else: 
                        print("Case ID Not found  for extra asins !")
                        self.post.ProcessErrorLog(self, 1, "Missing_case_ not found IA for extra asins !")
    
                    

                ### For Missing Case matching Historical Data
                if 'Amazon_Variations' in _rowsas['Missing_case_SAS_IO_Matching'] :
                    self.recheck_email_case(_rowsas['Missing_case_SAS_IO_Matching'])
                    self._Missing_case_SAS_IO_Matching = self._ManualLog
                    if self._Missing_case_SAS_IO_Matching !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIO_missing_asins_matching, value =  self._Missing_case_SAS_IO_Matching ))
                        print('Case Id IO registered successfully');self.post.ProcessErrorLog(self, 1, "Case Id IO registered successfully - For Missing Case matching Historical Data ")
                    else: 
                        print('\tSubject has not been registered yet - For Missing Case matching Historical Data \t')
                        self.post.ProcessErrorLog(self, 1, "No sas case created for matching records IO")
                        
                if 'Amazon_Variations' in _rowsas['Missing_case_SAS_IA_Matching'] :
                    self.recheck_email_case(_rowsas['Missing_case_SAS_IA_Matching'])
                    self._Missing_case_SAS_IA_Matching = self._ManualLog
                    if self._Missing_case_SAS_IA_Matching !='':
                        print('Case Id IA registered successfully');self.post.ProcessErrorLog(self, 1, "Case Id IA registered successfully - For Missing Case matching Historical Data ")
                        cellsASIN.append(Cell(row = index + 2, col = _SASIA_missing_asins_matching, value =  self._Missing_case_SAS_IA_Matching ))
                    else:
                        print('\tSubject has not been registered yet - For Missing Case matching Historical Data\t')
                        self.post.ProcessErrorLog(self, 1, "No sas case created for matching records IA ")
                

                ### For Missing Case with non matching Historical Data
                if 'Child' in _rowsas['Missing_case_SAS_IA_UnMatching'] :
                    self.recheck_email_case(_rowsas['Missing_case_SAS_IA_UnMatching'])
                    self._Missing_case_SAS_IA_UnMatching = self._ManualLog
                    if self._Missing_case_SAS_IA_UnMatching !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIA_parent_sku_IA, value =  self._Missing_case_SAS_IA_UnMatching ))
                        print('Case registered for missing unmatch asins IA ')
                        self.post.ProcessErrorLog(self, 1, "Case registered for missing unmatch asins IA ")
                    else: 
                        print("Missing_case_SAS_IA_UnMatching  not found - For Missing Case with non matching Historical Data !")
                        self.post.ProcessErrorLog(self, 1, "Missing_case_ not found IA for missing unmatch asins !")
                            

                if 'Child' in _rowsas['Missing_case_SAS_IO_UnMatching'] :
                    self.recheck_email_case(_rowsas['Missing_case_SAS_IO_UnMatching'])
                    self._Missing_case_SAS_IO_UnMatching = self._ManualLog            
                    if self._Missing_case_SAS_IO_UnMatching !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIO_parent_sku_IO, value =  self._Missing_case_SAS_IO_UnMatching ))
                        print('Case registered for missing unmatch asins IO '); self.post.ProcessErrorLog(self, 1, "Case registered for missing unmatch asins IO ")
                    else: 
                        print("Missing_case_SAS_IO_UnMatching not found IO !")
                        self.post.ProcessErrorLog(self, 1, "Missing_case_ not found IO for missing unmatch asins !")

        
            
                ### False Parent VL with  SKU
                if 'Amazon_Variations' in _rowsas['FALSE VL WITH SKU  - IO'] : 
                    self.recheck_email_case(_rowsas['FALSE VL WITH SKU  - IO'])
                    self.SAS_IO_with_parent_sku = self._ManualLog
                    if self.SAS_IO_with_parent_sku !='':                    
                        cellsASIN.append(Cell(row = index + 2, col = _SASIO_non_parent_sku_IO , value =  self.SAS_IO_with_parent_sku ))
                        print('Sku parent Case Id IO registered successfully')
                        self.post.ProcessErrorLog(self, 1, "Sku parent Case Id IO registered successfully ")
                    else: 
                        print("Sku parent case ID not found IO  !")
                        self.post.ProcessErrorLog(self, 1, "Sku parent case ID  not found IO ")
                
                        
                if 'Child' in _rowsas['FALSE VL WITH SKU SAS  - IA'] : 
                    self.recheck_email_case(_rowsas['FALSE VL WITH SKU SAS  - IA'])
                    self.SAS_IA_with_parent_sku = self._ManualLog
                    if self.SAS_IA_with_parent_sku !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIA_non_parent_sku_IA, value =  self.SAS_IA_with_parent_sku ))
                        print('Sku parent Case Id IA registered successfully')
                        self.post.ProcessErrorLog(self, 1, "Sku parent Case Id IA registered successfully ")
                    else: 
                        print("Sku parent case ID not found IA  !")
                        self.post.ProcessErrorLog(self, 1, "Sku parent case ID  not found IA ")
                    

                ### False Parent VL without SKU
                if 'Amazon_Variations' in _rowsas['FALSE VL WITHOUT SKUSAS  - IO'] :  
                    self.recheck_email_case(_rowsas['FALSE VL WITHOUT SKUSAS  - IO'])
                    self.SAS_IO_without_parent_sku = self._ManualLog
                    if self.SAS_IO_without_parent_sku !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIO_non_parent_sku_IO , value =  self.SAS_IO_without_parent_sku ))
                        print('Non sku parent Case ID IO registered successfully')
                        self.post.ProcessErrorLog(self, 1, "Non sku parent Case ID IO registered successfully ")
                    else: 
                        print("Non sku parent case not found IO  !")
                        self.post.ProcessErrorLog(self, 1, "Non sku parent case not found IO ")
                
                if 'Child' in _rowsas['FALSE VL WITHOUT SKU SAS  - IA'] :  
                    self.recheck_email_case(_rowsas['FALSE VL WITHOUT SKU SAS  - IA'])
                    self.SAS_IA_without_parent_sku = self._ManualLog
                    if self.SAS_IA_without_parent_sku !='':
                        cellsASIN.append(Cell(row = index + 2, col = _SASIA_non_parent_sku_IA, value =  self.SAS_IA_without_parent_sku ))
                        print('Non sku parent Case ID IA registered successfully')
                        self.post.ProcessErrorLog(self, 1, "Non sku parent Case ID IA registered successfully ")
                    else: 
                        print("Non sku parent case  ID not found IA  !")
                        self.post.ProcessErrorLog(self, 1, "Non sku parent case ID not found IA ")
                    
                

            if len(cellsASIN)>0:
                self.gsheet_job_log_Update.update_cells(cellsASIN)
            else:
                self.post.ProcessErrorLog(self, 1, "No Cells to update for VL LOG as no subjects found ")

        except Exception as e:
            print(f' Issue in updating SAS cases  error - {e}')
            self.post.ProcessErrorLog(self, 2, f' Issue in updating SAS cases - update_sas_caseid - error - {e}')

    def upload_file_missing_asin(self, parent_sku, type_ = 'match', asins_list=[] ):
        
        """
            Modified Existing upload file
        """
        
        try:
            
            if self.MissingASINs:
                
                child_asin_skus = asins_list
                try:
                    wb_append = xw.Book(self.VL_upload_file)
                except:
                    print('Try closing the excel files and try again'); time.sleep(1.5)
                    wb_append = xw.Book(self.VL_upload_file)
                
                dst_path = self.Saved_Missing_variation_path + f"MainVL_Template_Modified_{type_}_data__"+ self.VL_Name +self.today.strftime('%Y-%m-%d') + '.xlsx'
                time.sleep(2)
                sheet_name = 'Template'
                sheet = wb_append.sheets[sheet_name]
                sheet.api.Unprotect()
                time.sleep(2)
            
                df_values = list(sheet.range('B5:B1000').value)  
                missing_skus = [sku for sku in child_asin_skus if sku not in df_values]
                indexes = [i+5 for i in range(len(df_values)) if df_values[i] in child_asin_skus]
                if not indexes or missing_skus :
                    self.post.ProcessErrorLog(self, 1, f" skus {' '.join(missing_skus)} not found in the list of Main Vl template")
                    print(f"Skus {' '.join(missing_skus)} not found in the list of Main Vl template")
                    wb_append.app.quit()
                    if type_ == 'match':
                        print(f"Error: Sku(s) {', '.join(missing_skus)} not found in df_values original sheet.")
                        self.post.ProcessErrorLog(self, 1, f'New items {", ".join(missing_skus)} not in latest template sheet')
                        self._ManualLog = f'Template Issue - Matching SKUs {", ".join(missing_skus)} not present in Latest Template in {self.VL_Name}  '
                    
                    body = f"""
Hi,

For Brand {self.VL_Name}'s -  Latest template, Incorrect
Child Skus not found in  the Latest template: { ' '.join(missing_skus)  }  

Please modify accordingly.

Thanks
                    """
                    
                    if type_ == 'match' and  not self.gsheetData_job_log.iloc[-1]['Missing_case_notified_users']:
                        self.inform_users_via_mail(self._ManualLog, body)
                        cellsASIN = []
                        inactive_user_column = self.gsheetData_job_log.columns.get_loc('Missing_case_notified_users')  + 1
                        cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column, value =  "Notified user-MISSING CHILD SKU__"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                        self.gsheet_job_log_Update.update_cells(cellsASIN) 
                        print('Email sent to User for all the missing skus not present in main vl template. ')
                        self.post.ProcessErrorLog(self, 1, f"Email sent to User for all the missing skus not present in main vl template.") 
                    
                    if type_ == 'Unmatched' and  not self.gsheetData_job_log.iloc[-1]['Unmatching_case_informed_User']:
                        self.inform_users_via_mail(self._ManualLog, body)
                        cellsASIN = []
                        inactive_user_column = self.gsheetData_job_log.columns.get_loc('Unmatching_case_informed_User')  + 1
                        cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column, value =  "Notified user-MISSING CHILD SKU__"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                        self.gsheet_job_log_Update.update_cells(cellsASIN) 
                        print('Email sent to User for all the missing skus not present in main vl template. ')
                        self.post.ProcessErrorLog(self, 1, f"Email sent to User for all the missing skus not present in main vl template.") 
                        
                    return False
                        

                new_rows = []
                for index in indexes:
                    old_values = sheet.range(f"A{index}:ZZ{index}").value
                    new_rows.append(old_values)

                # new_rows = new_rows[1:]
                ## delete all the values starting from row A5  to ZZ 5 from the original sheet
                sheet.range(f"A5:ZZ{sheet.api.UsedRange.Rows.Count}").api.Delete()
                index = 5
                for row in new_rows:
                    sheet.range(f"A{index}:ZZ{index}").value = row
                    index +=1

                
                sheet.range('B4').value = parent_sku

                
                for index, sku in enumerate(indexes, start=6):
                    sheet.range(f"Z{index-1}").value = parent_sku


                sheet.range(f"Z{4}").value = ''
                print("\nModified the Excel sheet to Upload in Amazon portal  matching  ")

                time.sleep(1)
                wb_append.save(dst_path)
                wb_append.app.quit()
                time.sleep(1)
                print(dst_path)
                self.post.ProcessErrorLog(self, 1, f" Modified Existing upload file matching  {dst_path}")

                return dst_path

        except Exception as e :
            print('Error in creating Upload VL file as child asin skus may not be found ')
            self.post.ProcessErrorLog(self, 2, f"  Issue in creating file  - upload_file_missing_asin  - error - {e} ")
            return False

    def upload_vl_without_false_parent_sku(self, parent_sku):
        
        """ 
            Uploading VL without skus 
            stuck in False Parent 
        """
        

        # file_path = self.VL_upload_file
        false_parent_child_skus = self.false_parent_child_skus

        # Create a copy of the original file
        new_file_path = self.Saved_Missing_variation_path + f"US_Gya_Main_VL_Template_NEW_"+ self.VL_Name + self.today.strftime('%Y-%m-%d') + '.xlsm'
   
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        # shutil.copyfile(file_path, new_file_path)

        # Open the new workbook
        wb_append = xw.Book(self.VL_upload_file)
        time.sleep(2)
        sheet_name = 'Template'
        sheet = wb_append.sheets[sheet_name]
        sheet.api.Unprotect()
        time.sleep(2)
        df_values = list(sheet.range('F5').expand('down').value)

        indexes = [i+5 for i in range(len(df_values)) if df_values[i] not in false_parent_child_skus ]
        new_rows = []
        for index in indexes:
            old_values = sheet.range(f"A{index}:ZZ{index}").value
            new_rows.append(old_values)

        ## delete all the OLD VALUES starting from row A5  to ZZ 5 from the original sheet
        sheet.range(f"A5:ZZ{sheet.api.UsedRange.Rows.Count}").api.Delete()
        index = 5
        for row in new_rows:
            sheet.range(f"A{index}:ZZ{index}").value = row
            index +=1

        ### UPDATE the new sku in the sheet
        sheet.range('B4').value = parent_sku


        ### UPDATE all the row values with the  new sku in the sheet
        for index, sku in enumerate(indexes, start=6):
            sheet.range(f"Z{index-1}").value = parent_sku


        sheet.range(f"Z{4}").value = ''
        print("\nModified the Excel sheet to Upload in Amazon portal  matching  ")

        time.sleep(1)
        wb_append.save(new_file_path)
        wb_append.app.quit()
        time.sleep(1)
        print(new_file_path)

        print(f"\n New VL file uploaded without  skus that are  stuck in False Parent {new_file_path}\n")
        self.post.ProcessErrorLog(self, 1, f"  New VL file Ready to be uploaded with new sku and  without skus that are stuck in False Parent {new_file_path}")
        return new_file_path
               
    def create_VL_Delete_SKU_upload(self,parent_asin, sku):
            
        """
            Initiating Excel file  for template 1 file 
            - Parent with SKU
        
        """
        try:
            
            original_file_path = self.Missing_variation_path + 'Latest_Template.xlsm'

            try:
                wb_append = xw.Book(original_file_path)
            except:
                self.post.ProcessErrorLog(self, 1, "try closing other excel files to continue")
                time.sleep(2)
                wb_append = xw.Book(original_file_path)
            sheet = wb_append.sheets['Template']
            sheet.api.Unprotect() 
            time.sleep(2)
            
            sheet.api.Rows("4:" + str(sheet.api.Rows.Count)).Delete()

            next_row = 4
            sheet.cells(next_row, 1).value = 'essentialoil'
            sheet.cells(next_row, 2).value = sku
            sheet.cells(next_row, 4).value = "Delete"
    
            next_row += 1
            
            file_path = f"{self.Saved_Missing_variation_path}_{self.VL_Name}MAIN_VL_DELETE_{parent_asin}_contains SKU__{self.today.strftime('%Y-%m-%d')}.xlsx"
            wb_append.save(file_path)
            wb_append.app.quit()
            self.post.ProcessErrorLog(self, 1, "FIle created Latest template to Delete the Parent SKU \n")

            return file_path
        
        except Exception as e :
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating sas case parent sku ~ create_VL_Delete_SKU_upload  {e} ")

    def create_SAS_case_PARENT_NO_SKU(self,parent_asin_without_sku, all_child_asins ):

        """
            Initiating Excel file  for 2 template file 
            - Parent without SKU
        """
        try:

            wb_append = xw.Book(self.Parent_without_SKU_file_path)
            sheet = wb_append.sheets['Template - Variations Update']
            sheet.api.Unprotect() 
            time.sleep(2)
            

            count_of_asins = 0
            next_row = 13

            for child_asin in all_child_asins: 
                child_asin_skus=[]
                para = {    
                    "data" : {"userid":2, "ASIN": child_asin, "CountryID": self.CountryID,"table": "Product_Master_Details_ByASINAll" },
                    "type":"Select"
                }
                post = PostFun() 
                skujson = post.PostApiParaJson(para)
                for val in skujson['data']['input']:
                    if val['GroupName'] !='Info':
                        for valupdate in val['data']:                         
                            if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                child_asin_skus.append(valupdate['data']['updatedvalue'])
                # if not child_asin_skus:child_asin_skus.append('Na')
                for sku in child_asin_skus:
                    count_of_asins +=1 
                    sheet.cells(next_row, 2).value = child_asin
                    sheet.cells(next_row, 3).value = sku
                    sheet.cells(next_row, 5).value = parent_asin_without_sku
                
                    next_row += 1


            # sheet.cells(next_row, 2).value = parent_asin_without_sku
            # next_row += 1
            
            file_path = f"{self.Saved_Missing_variation_path}_{self.VL_Name}Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs unable to SPLIT - Parent ASIN {parent_asin_without_sku} contains_NO_SKU__{self.today.strftime('%Y-%m-%d')}.xlsx"
            
            wb_append.save(file_path)
            wb_append.app.quit()
            self.post.ProcessErrorLog(self, 1, "DONE EDITING EXCEL FILE for parent with NON SKU \n")

            return file_path   
        
        except Exception as e:
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating Upload VL file ~ create_SAS_case_PARENT_NO_SKU method {e} ")   

    def create_SAS_case_PARENT_SKU(self,parent_asin_with_sku, all_child_asins, parent_sku ):

        """
            Initiating sas create file for 
            - Parent with SKU
        """
        try:

            wb_append = xw.Book(self.Parent_without_SKU_file_path)
            sheet = wb_append.sheets['Template - Variations Update']
            sheet.api.Unprotect() 
            time.sleep(2)
            count_of_asins = 0
            next_row = 13

            for child_asin in all_child_asins: 
                child_asin_skus=[]
                para = {    
                    "data" : {"userid":2, "ASIN": child_asin, "CountryID": self.CountryID,"table": "Product_Master_Details_ByASINAll" },
                    "type":"Select"
                }
                post = PostFun() 
                skujson = post.PostApiParaJson(para)
                for val in skujson['data']['input']:
                    if val['GroupName'] !='Info':
                        for valupdate in val['data']:                         
                            if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                child_asin_skus.append(valupdate['data']['updatedvalue'])
                # if not child_asin_skus:child_asin_skus.append('Na')
                for sku in child_asin_skus:
                    count_of_asins +=1 
                    sheet.cells(next_row, 2).value = child_asin
                    sheet.cells(next_row, 3).value = sku
                    sheet.cells(next_row, 4).value = parent_sku
                    sheet.cells(next_row, 5).value = parent_asin_with_sku
                
                    next_row += 1


            # sheet.cells(next_row, 2).value = parent_asin_with_sku
            # next_row += 1
            
            file_path = f"{self.Saved_Missing_variation_path}_{self.VL_Name}Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs- Parent ASIN {parent_asin_with_sku} contains_SKU__{self.today.strftime('%Y-%m-%d')}.xlsx"
            print(' false parent  with sku file saved')
            wb_append.save(file_path)
            wb_append.app.quit()
            self.post.ProcessErrorLog(self, 1, "DONE EDITING EXCEL FILE for parent with NON SKU \n")

            return file_path   
        
        except Exception as e:
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating Upload VL file - create_SAS_case_PARENT_SKU - {e} ")   
            
    def get_new_sku_google_sheet(self,new_parent_asin=''):

        """
            Get the latest available ASIN ID from the google spreadsheet
            and Update with latest parent ASIN for that SKU 
        """

        try:

            if new_parent_asin  :
                
                    googleAPI = 'GoogleCredentials\client_sheet.json'
                    scope = ['https://www.googleapis.com/auth/drive']
                    credentials = service_account.Credentials.from_service_account_file(googleAPI)
                    scopedCreds = credentials.with_scopes(scope)
                    gc = gspread.Client(auth=scopedCreds)
                    gc.session = AuthorizedSession(scopedCreds)    

                    gsheetdata_parent_sku = gc.open(self._brand_file_name).worksheet('Parent SKU')      
                       
                    gsheetdata_parent_sku_data = [i[:5] for i in gsheetdata_parent_sku.get_all_values()[6:]]

                    
                    if self.VL_Name != 'Gya EOS ':
                        
                        available_entries =  [entry for entry in gsheetdata_parent_sku_data if entry[2] == 'Used' and entry[3] is not None and entry[3] !='' and entry[4] == ''   ]
                        if available_entries:
                            lastest_used_entry = available_entries[-1]
                            latest_id = lastest_used_entry[1]
                            row_index = None
                            for i, row in enumerate(gsheetdata_parent_sku_data):
                                if row[1] == latest_id:
                                    row_index = i
                                    break
                            updated_range = f'E{row_index + 7}' 
                            # updated_range
                            gsheetdata_parent_sku.update(updated_range, new_parent_asin)
                            return new_parent_asin
                    
                    available_entries =  [entry for entry in gsheetdata_parent_sku_data if entry[1] == 'Used' and entry[2] is not None and entry[2] !='' and entry[3] == '' and entry[4] == ''   ]
                    if available_entries:
                        lastest_used_entry = available_entries[-1]
                        latest_id = lastest_used_entry[0]
                        row_index = None
                        for i, row in enumerate(gsheetdata_parent_sku_data):
                            if row[0] == latest_id:
                                row_index = i
                                break
                        updated_range = f'D{row_index + 7}' 
                        # updated_range
                        gsheetdata_parent_sku.update(updated_range, new_parent_asin)
                        return new_parent_asin
            
            else:
                ### READ the lastest sheet and get latest sku and modify with current date
                googleAPI = 'GoogleCredentials\client_sheet.json'
                scope = ['https://www.googleapis.com/auth/drive']
                credentials = service_account.Credentials.from_service_account_file(googleAPI)
                scopedCreds = credentials.with_scopes(scope)
                gc = gspread.Client(auth=scopedCreds)
                gc.session = AuthorizedSession(scopedCreds)    

                gsheetdata_parent_sku = gc.open(self._brand_file_name).worksheet('Parent SKU')      
                gsheetdata_parent_sku_data = [i[:5] for i in gsheetdata_parent_sku.get_all_values()[6:]]
                
                if self.VL_Name != 'Gya EOS ':

                    available_entries = [entry for entry in gsheetdata_parent_sku_data if entry[2] =='Used' and entry[3] == '' and entry[4] == '' or entry[2]=='Available']
                    latest_available_entry = available_entries[0]
                    latest_id = latest_available_entry[1]
                    current_datetime = datetime.now().strftime('%Y-%m-%d ')
                    latest_available_entry[3] = current_datetime + ' 0:00'
                    latest_available_entry[4] = new_parent_asin
                    
                    row_index = None
                    for i, row in enumerate(gsheetdata_parent_sku_data):
                        if row[1] == latest_id:
                            row_index = i
                            break
                    updated_range = f'D{row_index + 7}:E{row_index + 7}' 
                    latest_available_entry = [i for i in latest_available_entry[3:] if i ]
                    gsheetdata_parent_sku.update(updated_range, [latest_available_entry])
                    return latest_id
                
                available_entries = [entry for entry in gsheetdata_parent_sku_data if entry[1] =='Used' and entry[3] == '' and entry[4] == '' or entry[1]=='Available']
                latest_available_entry = available_entries[0]
                latest_id = latest_available_entry[0]
                current_datetime = datetime.now().strftime('%Y-%m-%d ')
                latest_available_entry[2] = current_datetime + ' 0:00'
                latest_available_entry[3] = new_parent_asin
                
                row_index = None
                for i, row in enumerate(gsheetdata_parent_sku_data):
                    if row[0] == latest_id:
                        row_index = i
                        break
                updated_range = f'C{row_index + 7}:D{row_index + 7}' 
                latest_available_entry = [i for i in latest_available_entry[2:] if i ]
                gsheetdata_parent_sku.update(updated_range, [latest_available_entry])
                return latest_id

        except Exception as e :
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating new google sheet - get_new_sku_google_sheet - {e}")

    def find_parent_vl(self, parent_sku):
           
            try:
                    
                self.driver.get('https://sellercentral.amazon.com/inventory/ref=xx_invmgr_dnav_xx?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:;pagination:1;')
                time.sleep(2)
                self.driver.find_element(by=By.XPATH, value='//*[@id="myitable-search"]').send_keys(parent_sku)
                time.sleep(2)
                self.driver.find_element(by=By.CLASS_NAME, value='a-button-input').click()
                time.sleep(10)
                            
                checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                
                # means no listings, Variation deleted successfully
                if checkbundle[0].text.startswith('You currently have no listings'):
                    print("No items found ")
                    return True
                
                print("items found ",parent_sku)
                return False

            except Exception as e:
                self.post.ProcessErrorLog(self, 2, f" Error in find_parent_vl - find_parent_vl {e} " )

    def read_master_asin_sheet(self):
        try:
            googleAPI = 'GoogleCredentials\client_sheet.json'
            scope = ['https://www.googleapis.com/auth/drive']
            credentials = service_account.Credentials.from_service_account_file(googleAPI)
            scopedCreds = credentials.with_scopes(scope)
            gc = gspread.Client(auth=scopedCreds)
            gc.session = AuthorizedSession(scopedCreds)     
            self.Master_sheet_update = gc.open('Amazon -Master ASIN & SKU List').worksheet("Master List")
            self.Master_sheet_read = self.Master_sheet_update.get_all_records()
            self.post.ProcessErrorLog(self, 1, f" Reading Master Sheet ")
            self.Master_sheet_read = pd.DataFrame.from_dict(self.Master_sheet_read)
            self.false_parent_child_skus=  self.Master_sheet_read[self.Master_sheet_read['Amazon Site'] == 'US']['ASIN'].tolist()  
            self.post.ProcessErrorLog(self, 1, f" Returning records from Master Sheet ")
            return self.false_parent_child_skus
        except Exception as e:
            self.post.ProcessErrorLog(self, 1, f"Issue in Reading Master Sheet  {e}")
            print('Issue in Reading Master Sheet DB')
            return True
              
    def VLCheckAddVariation(self):
        
        try:    

            ### Get Top 20 Child ASIN to Parent ASIN  and search the parent for top 20 Imp child asins
            tmp_ChildASIN =  self.gsheetData[(self.gsheetData['Parent for System Verification'] == self._ParentASIN) & (self.gsheetData['Top 20 Sales Child ASIN'] != '')] 
            tmp_ChildASIN = list(tmp_ChildASIN['Child ASIN VL List'].unique())
            # tmp_ChildASIN = tmp_ChildASIN[:1]
            # tmp_ChildASIN = ['B09HBVP5MX11','B09HBVP5MX4']
            

            self.VLList = pd.DataFrame(columns=["RequestASIN", "Type", "ASIN", "SKU"])
            self.VLList = self.VLList.drop(self.VLList.index[:])
            _parentli = None


            ### Map and check parent for top 20 child asins frpm the Live portal
            self.mapped_parent_child_items = self.FindVLData(tmp_ChildASIN)
            if self.mapped_parent_child_items == 'PAGE NOT LOADED':
                self.post.ProcessErrorLog(self, 2, "Error In Find VL Data, will try again in next run, returning back... " ) ; 
                self._ManualLog = f'BUTTON ISSUE in  Find VL DATA '
                self.ReadUpdateGoogleSheet(2)
                sys.exit(1)
    

            if not  [ i for i in self.mapped_parent_child_items if i ] :  
                self.post.ProcessErrorLog(self, 2, "No mapped items found from top 20 child asins, will check with parent " ) ; 
            

            ### If parent found, from top 20 childs, restoring it in a variable
            _parentli = list(self.VLList[(self.VLList['Type']=='parent')]['ASIN'].unique())


            ### Here self.VLList == Live data from the portal - all parents with their sku and associated child 
            self.VLList = self.VLList.drop(self.VLList.index[:])
            self.mapped_parent_child_items = self.FindVLData(_parentli, parent = True)
           


            ### Will recheck the data by searching with parent, as couldn't find any result from parent earlier !
            if len(self.VLList)==0:
                time.sleep(10)
                self.mapped_parent_child_items = self.FindVLData(_parentli, parent = True)
        
            ### Getting the difference of all child found from parent from Live Portal - Child from Main VL data sheet
            child_values = list(self.mapped_parent_child_items.values())
            if child_values:
                child_values = child_values[0]
            no_parent_childs = list( set(self.gsheetData['Child ASIN VL List'].to_list()) - set(child_values ) ) 
            
            self.post.ProcessErrorLog(self, 1, f'Currently these child asins are with no sku == Missing = {str(self.false_parent_child_skus)}  ');print(f'Currently these child asins are with no sku == Missing = {str(self.false_parent_child_skus)}   ')
            ### Saved the Live portal log in a csv file for  a better view
            self.VLList.to_csv(f'VLList_{self.VL_Name}{self.today.strftime("%Y-%m-%d")}.csv')

            ### Modified the VL Data Sheet from the Live portal
            self.gsheetData['Live Parent ASIN'] = "No Parent" 
            for _ASINindex, _ASINRow in self.gsheetData.iterrows():
                _rowexist = self.VLList[self.VLList['ASIN'] == _ASINRow['Child ASIN VL List']]
                if len(_rowexist)>0:
                    self.gsheetData.loc[_ASINindex,'Live Parent ASIN'] = ",".join(list(_rowexist['RequestASIN'].unique()))
            
            ### Saved the VL Data sheet log in a csv file for  a better view
            self.post.ProcessErrorLog(self, 1, "Prepared VLlistData file"  )
            self.gsheetData.to_csv('VLListData.csv')

            self.read_master_asin_sheet()
            if not self.false_parent_child_skus: 
                self.false_parent_child_skus = no_parent_childs 

            self.false_parent_child_skus = self.false_parent_child_skus if  set(no_parent_childs).issubset(set(self.false_parent_child_skus)) else no_parent_childs
            
            self.post.ProcessErrorLog(self, 1, f'1. Current len of our child asin present in Portals = {str(len(list(self.mapped_parent_child_items.values())[0]) )}  ')
            print(f'1. Current len of our child asins present in Portal = {str(len(list(self.mapped_parent_child_items.values())[0]) )}   ')
           
            if len(list(self.mapped_parent_child_items.values())[0]) != len(list(self.gsheetData['Child ASIN VL List'].unique()))  : ### 107 == 107
                self.post.ProcessErrorLog(self, 1, f'2. We will get the Missing or Extra ASINS as count from portal is  mismatched  ')
                print(f'2. We will get  Missing or Extra ASINS as count from portal is  mismatched   ')

            ### If no parent is found From top 20 chils, finding, it in rest of 87 childs and marking as False Parent
            if not [ i for i in self.mapped_parent_child_items if i ]:
                self.post.ProcessErrorLog(self, 1, "Checked the combination from relationship with parent  as well, no mapping Found  " )
                print('We will find the parent stuck in the rest 87 child asins, and delete it ')
                self.post.ProcessErrorLog(self, 2, "We find the parent stuck in the rest 87 child asins, and delete it, since main VL is not found anywhere from the top 20  " )
                non_imp_ChildASIN =  self.gsheetData[(self.gsheetData['Parent for System Verification'] == self._ParentASIN) & (self.gsheetData['Top 20 Sales Child ASIN'] == '')] 
                non_imp_ChildASIN = list(non_imp_ChildASIN['Child ASIN VL List'].unique())
                # non_imp_ChildASIN = ['B09HBVP5MX11', 'B09M88ZX322R']
                self.mapped_parent_child_items = self.FindVLData(non_imp_ChildASIN)
                non_imp_parent = ''
                try:
                    non_imp_parent = list(self.mapped_parent_child_items.keys())[0]
                except: ...
                if not( non_imp_parent ):
                    print("Confirmed No  parent  found from any of the remaining 87 child asins, proceeding with Creation of NEW parent VL ")
                    self.post.ProcessErrorLog(self, 1, "Confirmed No  parent  found from any of the remaining 87 from any of the remaining 87 child asins, proceeding with Creation of NEW parent VL By deleting all previous parents " )
                    self.post.ProcessErrorLog(self, 1, " Now, Reading Master Sheet to get the asins which are stuck in parent which will be exlcuded for Main VL Upload")
                    self.post.ProcessErrorLog(self, 1, f'Current false sku checked it in rest 87 asins = {str(self.false_parent_child_skus)}  ');print(f'Current false sku checked it in rest 87 asins = {str(self.false_parent_child_skus)}   ')
                    self.post.ProcessErrorLog(self, 1, f'2. Current len of our child asins = {str(len(list(self.mapped_parent_child_items.values())[0]) )}  ');print(f'2. Current len of our child asins = {str(len(list(self.mapped_parent_child_items.values())[0]) )}   ')
                    return self.false_parent_child_skus
                else:
                    self.post.ProcessErrorLog(self, 2, f" Parent True False {self.ParentTrueFalse} " )
                    self.post.ProcessErrorLog(self, 1, "Found parent in some of the non imp child asins, lets proceed with True False parent relationship  " )
                    self.ParentTrueFalse['ParentTrue'] = ''
                    self.ParentTrueFalse['ParentFalse'] = non_imp_parent
                    self.post.ProcessErrorLog(self, 2, f" Parent True False {self.ParentTrueFalse} " )
                    return True
            else:
                self.post.ProcessErrorLog(self, 1, f"Mapped Parent dict item = True, as parent and their child items are mapped, will check further if any of the child is stuck with other False Parent " ) 
            


            ### Calculated the True and False Parent from live portal Data sheet
            vallist = [] 
            mcount = len(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] != ''])
            ncount = len(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] == ''])
            # ncount = 1
            _parentli = list(self.VLList[(self.VLList['Type']=='parent')]['ASIN'].unique())
            for _parent in _parentli:                
                major_count = len(self.gsheetData[(self.gsheetData['Live Parent ASIN'] == _parent) & ( self.gsheetData['Top 20 Sales Child ASIN'] != '' ) ])/ mcount*100                
                non_major_count = len(self.gsheetData[(self.gsheetData['Live Parent ASIN'] == _parent ) & (  self.gsheetData['Top 20 Sales Child ASIN'] == '' ) ]) / ncount*100
                rowdata = {'Parent':_parent , 'M':major_count, 'N':non_major_count  }                
                vallist.append(rowdata)
            _true_parents = []    
            _false_parents = []
            for true_parent in vallist:
                if true_parent['M'] >=50 and true_parent["N"] >=70:
                    _true_parents.append(true_parent['Parent'])                    
                else:
                    _false_parents.append(true_parent['Parent'])
            self.ParentTrueFalse = {'ParentTrue':",".join(_true_parents),'ParentFalse': ",".join(_false_parents)}
            self.post.ProcessErrorLog(self, 1, f" Parent trueFalse  current   {self.ParentTrueFalse}"  )
            ### Finding Parent of all the childs which are not associated with the Live Parent
            self.post.ProcessErrorLog(self, 1, f"Finding Parent of all the childs which are not associated with the Live Parent " ) 
            false_parent_key = ''
            if no_parent_childs:
                parent_limited_childs_ = self.FindVLData(no_parent_childs)
                try:
                    false_parent_key = list(parent_limited_childs_.keys())[0] if list(parent_limited_childs_.keys())[0] != self.ParentTrueFalse['ParentTrue'] else ''
                except:
                    self.post.ProcessErrorLog(self, 1, f"No Parent associated with the Asin, as asin is not in touch with Live parent from top 20 child asins" )
                if [i for i in parent_limited_childs_] and false_parent_key:
                    self.post.ProcessErrorLog(self, 2, f"Found child missing from top 20 list, checking the parent, marking as False parent and removing them out " )
                    # self.ParentTrueFalse['ParentTrue'] = list(self.mapped_parent_child_items.keys())[0]
                    self.ParentTrueFalse['ParentFalse'] = false_parent_key
                    self.post.ProcessErrorLog(self, 2, f" Missing child parent {str(parent_limited_childs_)} " )
                    self.post.ProcessErrorLog(self, 2, f" Gonna delete this false parent which was found in Missing asins of the top 20 child asins" )
                    self.mapped_parent_child_items = parent_limited_childs_
                    return True
            else:
               self.post.ProcessErrorLog(self, 1, f"No Child asins found that are not mapped with our Live Parent, Surpassed the method of finding parent all of child which are not associated with the Live Parent, " ) 
            
            

            ### self.Child_asin_skus_comparison(self.VLList)   ! ON HOLD FOR NOW !

            
            child_list_Master = list(self.gsheetData['Child ASIN VL List'].unique())
            child_list_VLList = list(self.VLList[self.VLList['Type']=='child']['ASIN'].unique())
            self.ExtraASINs = list(set(child_list_VLList) - set(child_list_Master))
            self.MissingASINs = list(set(child_list_Master) - set(child_list_VLList))
            
            self.MissingASINs = [ i for  i in self.MissingASINs if i]
            self.ExtraASINs = [ i for  i in self.ExtraASINs if i]
            
            if len(self.ExtraASINs) > 0 :
                self.post.ProcessErrorLog(self, 1, f"Extra asins found,  going for further checks to perform the changes "  )
            if  len(self.MissingASINs)>0:                
                self.post.ProcessErrorLog(self, 1, f"Missing asins found,  going for further checks to perform the changes "  )
            if len(self.ExtraASINs) > 0 or   len(self.MissingASINs)>0:     
                return False
            self.post.ProcessErrorLog(self, 2, f"VLCheckAddVariation No missing asins or Extra Asins found, returning True " ) 
            return True
        
        except Exception as err:  
            print("VLCheckAddVariation Error ", str(err))
            self.post.ProcessErrorLog(self, 2, "VLCheckAddVariation Error, Wait for Next run  " + str(err)) 
            # self._ManualLog = f'Error on  VLCheckAddVariation RPA '
            # self.ReadUpdateGoogleSheet(2)
            sys.exit(1)
    
    def Child_asin_skus_comparison(self, vl_list):

        filtered_mapped_master_list = {}


        v = self.ParentTrueFalse['ParentTrue']
        all_child_asins = list(self.VLList[self.VLList['RequestASIN']  == v]['ASIN'].unique())
        parent_sku = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == v)]['SKU'].iloc[0]
        
        
        # def master_table():

        #     import csv

            
        #     googleAPI = 'GoogleCredentials\client_sheet.json'
        #     scope = ['https://www.googleapis.com/auth/drive']
        #     credentials = service_account.Credentials.from_service_account_file(googleAPI)
        #     scopedCreds = credentials.with_scopes(scope)
        #     gc = gspread.Client(auth=scopedCreds)
        #     gc.session = AuthorizedSession(scopedCreds) 

    
        #     self.master_sku_data_update = gc.open("Amazon -Master ASIN & SKU List").worksheet("Master List")
        #     self.master_sku_data_read = self.master_sku_data_update.get_all_records()
        #     self.master_sku_data_read = pd.DataFrame.from_dict(self.master_sku_data_read)

        #     mapped_master_list = {}
        #     filtered_skus = []

        #     for _, row in self.master_sku_data_read.iterrows():
        #         child_asin = row["ASIN"] 
        #         child_sku = row['SKU']
        #         if row['Amazon Site'] == 'US'and row["ASIN"] and row['SKU']:
        #             if child_asin not in mapped_master_list:
        #                 mapped_master_list[child_asin] = []
        #             mapped_master_list[child_asin].append(child_sku)

        #     # 

        #     with open('mapped.csv', 'w', newline='') as csvfile:
        #         writer = csv.writer(csvfile)
        #         for key, value in mapped_master_list.items():
        #             writer.writerow([key, value])

         
    

        # master_table()

        ## from original df, get the count of top 20 asins and rest of count of asins 
        vallist = [] 
        mcount = len(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] != ''])
        ncount = len(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] == ''])

        ### got all child asins with mapped sku from the portal
        ### Create a dictionary to store the mapped ASINs and SKUs
        portal_list = {}
        for index, row in vl_list.iterrows():
            asin = row['ASIN']
            sku = row['SKU']
            if asin not in portal_list:
                portal_list[asin] = []
            portal_list[asin].append(sku)
        portal_list.pop(v)
        # print(portal_list)

        
        missing_child_skus_not_matching = {}
        matching_child_skus = {}
        for k,v in filtered_mapped_master_list.items():
            if k in portal_list:
                result = list(set(portal_list[k]) - set(v))
                if result:
                    missing_child_skus_not_matching[k] = result
                else:
                    matching_child_skus[k] = v

        print("COMPARISON WITH MASTER FILE FOR MISSING CHILD SKUS")
        

        top_20_asins = list(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] != '' ]['Child ASIN VL List'].unique())
        rest_asins = list(self.gsheetData[self.gsheetData['Top 20 Sales Child ASIN'] == '' ]['Child ASIN VL List'].unique())

        ### will compare the skus of child asin from the map sheet
        missing_child_skus = set(missing_child_skus_not_matching)
        ### Number of ASINs in the top 20 ASINs list that are also in the missing child SKUs set
        top_20_missing_asins = len(set(top_20_asins).intersection(missing_child_skus))
        ### Number of ASINs in the rest of the ASINs list that are also in the missing child SKUs set
        rest_missing_asins = len(set(rest_asins).intersection(missing_child_skus))
        ### Total number of ASINs in the top 20 ASINs list and the rest of the ASINs list
        total_asins = len(top_20_asins) + len(rest_asins)
        top_20_missing_asins_percentage = 100 - top_20_missing_asins / total_asins * 100
        rest_missing_asins_percentage = 100 -rest_missing_asins / total_asins * 100
        print("Percentage of ASINs in the top 20 ASINs list that are also in the missing child SKUs set:", top_20_missing_asins_percentage, "%")
        print("Percentage of ASINs in the rest of the ASINs list that are also in the missing child SKUs set:", rest_missing_asins_percentage,"%" )
        
    


        if top_20_missing_asins_percentage > 90 and rest_missing_asins_percentage > 90:

            print('Initating SAS Case for all the missing child asin skus')
            self.post.ProcessErrorLog(self, 1, f"  Initating SAS Case for all the missing child asin skus ")

            ## correct the sas case templates
            
            self.post.ProcessErrorLog(self, 1, f" Immediate Action. gonna send the SAS cases for extra asins")
            
            subject = f"Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs unable to SPLIT - Child ASIN {v} contains NO SKU__{self.today.strftime('%Y-%m-%d')}"
            case_ID_generated = self.seller_support_case(v, subject, Child_ASINs = all_child_asins )
            
            file_path = self.create_SAS_case_PARENT_NO_SKU(v, all_child_asins)
            headline = f"Child ASINs unable to SPLIT - Child ASIN {v} contains NO SKU" 
            sku_line = f"Can't split child ASINs from Child ASIN {v} without Child SKU" 
            line = "No Child SKU"

            
            self.SAS_IO_without_child_sku = self.SAS_issue_assistance(v, case_ID_generated, subject, 
                                                                        mail_type="Email" , file_path = file_path, 
                                                                        sku_line = sku_line, parent_sku = parent_sku, 
                                                                        line = line,child_Asins=' '.join(all_child_asins),
                                                                        True_parent = True )
            
            subject = f"Child ASINs unable to SPLIT - Child ASIN {v} contains NO SKU | A31LSP1L7F6XJ2__{self.today.strftime('%Y-%m-%d')}"
            self.SAS_IA_without_child_sku = self.SAS_issue_assistance(v, case_ID_generated, subject, mail_type="HTML", 
                                                                        file_path = file_path, sku_line = sku_line, 
                                                                        parent_sku = parent_sku, headline = headline,
                                                                        line = line, child_Asins=' '.join(all_child_asins),
                                                                        True_parent = True)
            print('Subjects \n')
            print(  self.SAS_IO_without_child_sku )
            print(  self.SAS_IA_without_child_sku )
            print("\n\tCreated Seller Support Cases for Child Asins without SKUs - VL Deletion  \t")
            self.post.ProcessErrorLog(self, 1, "Created Seller Support Cases for Child Asins without SKUs - VL Deletion ")

            
            ## updated the columns  for sas cases
            cellsASIN=[]
            # time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc(false_parent__without_sku_SAS_time_column)  + 1
            # case_ID_generated_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_seller_support)  + 1
            # SAS_IO_without_child_sku_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_IO)  + 1
            # SAS_IA_without_child_sku_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_IA)  + 1
            
            # cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = time_case_ID_generated_column      , value =  datetime.today().strftime('%Y-%m-%d %H:%M') ))     
            # cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = case_ID_generated_column            , value =  case_ID_generated      ))
            # cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = SAS_IO_without_child_sku_column , value =  self.SAS_IO_without_child_sku    ))
            # cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = SAS_IA_without_child_sku_column , value =  self.SAS_IA_without_child_sku    ))
            print('Case file missing unmatch file Uploaded  successfully');self.post.ProcessErrorLog(self, 1, "Case file missing unmatch asin successfully ")
            
            self.gsheet_job_log_Update.update_cells(cellsASIN) 
            print('Subjects noted  successfully in excel sheet')
            self.post.ProcessErrorLog(self, 1, "Subjects noted  successfully in excel sheet ")

        else:

            self.post.ProcessErrorLog(self, 1, 'Deleting Previous SKU and Uploading NEW VL ')    
            
            print(f"\n\t~ Deleting VL for False Parent with sku after ")
            self.post.ProcessErrorLog(self, 1, f"Deleting VL for False Parent with sku ")
            file_path = self.create_VL_Delete_SKU_upload(v, parent_sku)
            time.sleep(1)
            batch_id_returned = self.Delete1ASIN2SKU(parent_sku, filepath = file_path, function_run = 'both' )

            
            false_parent_sku_time_column = 'Time of False Parent with SKU VL Delete'
            false_parent_sku_SAS_time_column = 'Time of FALSE VL WITH SKU SAS CASES'
            false_parent_sku_column_name = 'False Parnet with SKU VL Delete Status'

            ## updated the column for entry point
            cellsASIN=[]
            Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(false_parent_sku_time_column)  + 1
            missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(false_parent_sku_column_name)  + 1
            false_vl_sku_time_sas = self.gsheetData_job_log.columns.get_loc(false_parent_sku_SAS_time_column) + 1

            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = Time_missing_asin_vl_upload_file_batch_id , value = datetime.today().strftime('%Y-%m-%d %H:%M') ))
            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = missing_asin_vl_upload_file_batch_id , value =  batch_id_returned ))
            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = false_vl_sku_time_sas , value =  '' ))

            print(' Deletion of old Parent VL status completed ')
            self.post.ProcessErrorLog(self, 1, " Deletion of old Parent VL status completed successfully ")
            self.gsheet_job_log_Update.update_cells(cellsASIN) 
            self.post.ProcessErrorLog(self, 1, f"{file_path} Existing VL {v} File Uploaded Sucessfully")
       
            result_deletion = self.find_parent_vl(parent_sku)
            if result_deletion: print('Deleted successfully')
            self.post.ProcessErrorLog(self, 1, "Check VL still Exists " + parent_sku + ' ' + result_deletion)

        
            ## Confirmation of the deleted asin batch id data in EXCEL sheet
            if  result_deletion  :
                    
                print("DELETED PARENT FLAT FILE UPLOADED SUCCESSFULLY " ,end='\n')
                self.post.ProcessErrorLog(self, 1, "DELETED PARENT FLAT FILE UPLOADED SUCCESSFULLY")
                result_deletion_parent  = self.find_parent_vl(v)
            
                ### Upload New VL  ###
                if  result_deletion_parent:
                    new_sku = self.get_new_sku_google_sheet()
                    if not new_sku:
                        self.post.ProcessErrorLog(self, 1, f' No new Sku found,  ');print(f' No new Sku found,   ')
                        return
                    if self.find_parent_vl(new_sku)==True:
                        self.post.ProcessErrorLog(self, 3, "New SKU  already Exists in VL  " + new_sku )  
                        return

                    # filepath = self.upload_vl(new_sku)   ### set the file path THIS IS FOR CHILD SKU 
                    filepath = ' '
                    self.post.ProcessErrorLog(self, 2, f"Going to Upload file for New parent VL   ")
                    new_parent_batch_id_returned = self.Delete1ASIN2SKU(new_sku, 
                                                            function_run='upload' ,
                                                            filepath=filepath )
                    if  new_parent_batch_id_returned:
                        print("\nNew VL uploaded, get the parent asin ")
                        self.post.ProcessErrorLog(self, 1, "New VL file uploaded Sucessfully")
                        checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                        mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
                        if not checkbundle[0].text.startswith('You currently have no listings'): 
                                for each_product in mtrowlis:
                                    id = each_product.get_attribute('id')
                                    name = each_product.find_element(by = By.ID, value=id + '-title')
                                    name = name.text.split('\n')[2]
                                    print(name)

                        print(f'\n Got the new parent asin {name}, extract it \n')
                        self.post.ProcessErrorLog(self, 1, f"Got the new parent asin {name}, extract it \n")
                        self.get_new_sku_google_sheet(name) 
                        self.post.ProcessErrorLog(self, 1, f"New VL name {name} Loaded Sucessfully")
                        if not self.find_parent_vl(new_sku):
                            print("New VL Added Successfully")
                            print(new_parent_batch_id_returned)
                            ## updated the new vl columnn
                            cellsASIN=[]
                            Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Time of  Main VL Upload')  + 1
                            missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Main VL Upload status')  + 1

                            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = Time_missing_asin_vl_upload_file_batch_id , value = self.today.strftime('%Y-%m-%d %H:%M') ))
                            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = missing_asin_vl_upload_file_batch_id , value =  new_parent_batch_id_returned ))

                            self.gsheet_job_log_Update.update_cells(cellsASIN) 
                            print('New VL Added Successfully in sheet as well ')
                            self.post.ProcessErrorLog(self, 1, "New VL Added Successfully in sheet as well ")
                        else:
                            self.post.ProcessErrorLog(self, 2, f"Checked from existing page new vl Upload not successfull   ")
                    else:
                        print('No batch ID found, no file uploaded, was about to Upload New VL ')
                        self.post.ProcessErrorLog(self, 2, f"No batch ID found, no file uploaded, was about to Upload New VL   ")

    def Missing_asins_Support_SAS_case(self):

        try:   ### Download the Latest template from google drive 
            if self.ParentTrueFalse['ParentTrue'] == '' or self.ParentTrueFalse['ParentFalse'] != '' or self.MissingASINs:
                file_downloaded = self.DownloadGoogleFile()
                if not file_downloaded:
                    self.post.ProcessErrorLog(self, 2, f"  File didnt downloaded in first go, going for second try ...")
                    time.sleep(3)
                    file_downloaded = self.DownloadGoogleFile()
                print("Download Google file complete");self.post.ProcessErrorLog(self, 1, 'Download Google file complete')
                time.sleep(5)

                
                self.post.ProcessErrorLog(self, 2, f"  Moving to download template file method.")
                result_download_template = self.DownloadTemplateFile()
                if not result_download_template:
                    self.post.ProcessErrorLog(self, 2, f"  Issue in Downloading template method , returning back ...")
                    return False
                
                self.post.ProcessErrorLog(self, 1, "Moving Content from google drive to template Excel file") 
                download_move_content = self.move_content_from_drive_to_template()
                if not download_move_content:
                    self.post.ProcessErrorLog(self, 2, f"Issue in copy paste data from source to destination file  returning back ...")
            
                    self.sendmessage()
                   
                    
                    body = f"""
Hi,

For Brand {self.VL_Name}'s -  Issue in Creating the VL Upload file as the template columns do not match, wiht the latest one downloaded from Amazon.

Template file name : {self.file_name_google_drive}

Please modify the template file Link : https://drive.google.com/drive/folders/1QxvMKKLtqj0lwDwzVnVewUs1X4VR4QRK

Link to get the latest Template file from Amazon : https://sellercentral.amazon.com/listing/cards/add-product?style=standalone

Attached the Google drive template for your reference.

Please help update the latest Template in Google Drive, so VL system can asssit on the same.
Kindly Modify it at the earliest.

Thanks
                    """
                    new_filename = self.Missing_variation_path + "file_with_values_sku.xlsx"
                    self.inform_users_via_mail(f'Issue in VL Template - for {self.VL_Name}  Brand ', body, file_path=new_filename)
                    return False
                self.post.ProcessErrorLog(self, 1, f"Data copied successfully to Latest Vl Upload File")
                
                # self.sendmessage()  
                self.post.ProcessErrorLog(self, 2, str(self.ParentTrueFalse))
            
            # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
            # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)     
                
            data_values = self.gsheet_job_log_Update.get_all_values()
            headers = data_values[0]
            self.gsheetData_job_log = pd.DataFrame(data_values[1:], columns=headers)   
            gsheet_Last_index = self.gsheetData_job_log.shape[0] - 1
            gsheet_Last_Row = self.gsheetData_job_log.iloc[-1]

            try:
                if self.MissingASINs:

                    for child_asin in self.MissingASINs:             
                        para = {    
                                "data" : {"userid":2, "ASIN":child_asin, "CountryID":self.CountryID,"table": "Product_Master_Details_ByASINAll" },
                                "type":"Select"
                            }
                        post = PostFun() 
                        skujson = post.PostApiParaJson(para)
                        countryKey  ='' 
                        for val in skujson['data']['input']:
                            if val['GroupName'] !='Info':
                                for valupdate in val['data']:                         
                                    if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                        self.child_asin_skus[child_asin]=(valupdate['data']['updatedvalue'])
                    
            except:
                print('Child asin not found ')
        
        except Exception as e:
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating Missing SAS Case - Missing_asins_Support_SAS_case - {str(e)} ")

        
        
        def delete_false_parent_with_sku(vl_upload = False):
            
            false_parent_sku_time_column = 'Time of False Parent with SKU VL Delete'
            false_parent_sku_SAS_time_column = 'Time of FALSE VL WITH SKU SAS CASES'
            false_parent_sku_column_name = 'False Parnet with SKU VL Delete Status'


            
            self.post.ProcessErrorLog(self, 1, f"Checking entry point for deleting VL by checing the last row column value of parent false should be  null or not ! ")
            ### entry point for SKU Delete VL
            if  gsheet_Last_Row[false_parent_sku_column_name] == '':
                print(f"\n\t~ Deleting VL for False Parent with sku  ")
                self.post.ProcessErrorLog(self, 1, f"Deleting VL for False Parent with sku ")
                file_path = self.create_VL_Delete_SKU_upload(v, parent_sku)
                time.sleep(1)
                self.post.ProcessErrorLog(self, 2, f"File Created to delete main VL, Going to Upload file  and do manual delete for to Delete FALSE parent VL ")
                batch_id_returned = self.Delete1ASIN2SKU(parent_sku,filepath = file_path, function_run = 'both' )
    
                if  batch_id_returned: 
                    self.post.ProcessErrorLog(self, 2, f"Batch uploaded succesfully, will delete VL with SKU file ")
                    ## updated the column for entry point
                    cellsASIN=[]
                    Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(false_parent_sku_time_column)  + 1
                    missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(false_parent_sku_column_name)  + 1
                    false_vl_sku_time_sas = self.gsheetData_job_log.columns.get_loc(false_parent_sku_SAS_time_column) + 1
                    
                    inactive_user_column = self.gsheetData_job_log.columns.get_loc('False_vl_with_sku_notified_user')  + 1; 
                    cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column , value =  ""  ))
                    
                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Time_missing_asin_vl_upload_file_batch_id , value = datetime.today().strftime('%Y-%m-%d %H:%M') ))
                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = missing_asin_vl_upload_file_batch_id , value =  batch_id_returned ))
                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = false_vl_sku_time_sas , value =  '' ))

                    print('Deletion of old Parent VL status completed ')
                    self.post.ProcessErrorLog(self, 1, " Deletion of old Parent VL status completed successfully ")
                    self.gsheet_job_log_Update.update_cells(cellsASIN) 
                    self.post.ProcessErrorLog(self, 1, f"{file_path} Existing VL {v} File Uploaded Sucessfully")
                else:
                    self.post.ProcessErrorLog(self, 2, f"No batch found so no file uploaded, MAIN VL Delete File Not Uploaded  ")

                ### rechecking if existing vl parent asin got deleted from Variation Wizard page and relisting page ###    
                time.sleep(20)            
                result_deletion = self.find_parent_vl(parent_sku)
                if result_deletion: 
                    print('Existing VL Deleted successfully')
                    self.post.ProcessErrorLog(self, 1, f"Existing VL Deleted successfully  {parent_sku}")
                else:
                    print('Existing VL still Exists')
                    self.post.ProcessErrorLog(self, 1, f"Check  VL Exists  {parent_sku}"  )

            
                ## First recheck if old VL exists from parent sku vise 
                if  result_deletion and vl_upload and batch_id_returned :
                        #  second recheck if old exists from parent asin vise
                        print("DELETED PARENT FLAT FILE UPLOADED SUCCESSFULLY " ,end='\n')
                        result_deletion_parent  = self.find_parent_vl(v)
                    
                        self.post.ProcessErrorLog(self, 1, "Gonna check for the previous ASIN if its exists or not")
                        ### Upload New VL  ###
                        if  result_deletion_parent:
                            self.post.ProcessErrorLog(self, 1, "DELETED PARENT FLAT FILE UPLOADED SUCCESSFULLY, Asin deleted successfully")
                            new_sku = self.get_new_sku_google_sheet()
                            if not self.find_parent_vl(new_sku)==True:
                                self.post.ProcessErrorLog(self, 1, "New SKU VL from sheet already Exist in Manage Inventory Page " + new_sku )  
                                return

                            self.post.ProcessErrorLog(self, 2, f"Going to Upload file for New parent VL without the skus stuck in false parent  ")
                            filepath = self.upload_vl_without_false_parent_sku(new_sku)
                            new_parent_batch_id_returned = self.Delete1ASIN2SKU(new_sku, 
                                                                    function_run='upload' ,
                                                                    filepath=filepath )
                            if  new_parent_batch_id_returned:
                                print("\nNew VL uploaded, get the parent asin ")
                                self.post.ProcessErrorLog(self, 1, "New VL file uploaded Sucessfully")
                                self.find_parent_vl(new_sku)
                                checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                                mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
                                if not checkbundle[0].text.startswith('You currently have no listings'): 
                                    for each_product in mtrowlis:
                                        id = each_product.get_attribute('id')
                                        name = each_product.find_element(by = By.ID, value=id + '-title')
                                        name = name.text.split('\n')[2]
                                        print(name)

                                    print(f'\n Got the new parent asin {name}, extract it \n')
                                    self.post.ProcessErrorLog(self, 1, f"Got the new parent asin {name}, extracted it and updated the SKU sheet as well \n")
                                    self.get_new_sku_google_sheet(name) 
                                    self.post.ProcessErrorLog(self, 1, f"New VL name {name} Loaded Sucessfully")
                                else:
                                    print('No VL Added Successfully in PORTAL')
                                    self.post.ProcessErrorLog(self, 1, "No VL Added Successfully in PORTAL , ALTHOUGH FILE UPLOADED SUCCESSFULLY ")

                                if not self.find_parent_vl(new_sku):
                                    print("New VL Added Successfully")
                                    print(new_parent_batch_id_returned)
                                    ## updated the new vl columnn
                                    cellsASIN=[]
                                    Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Time of  Main VL Upload')  + 1
                                    missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Main VL Upload status')  + 1
                                    false_parent_sku_column_name = self.gsheetData_job_log.columns.get_loc('False Parnet with SKU VL Delete Status')  + 1

                                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Time_missing_asin_vl_upload_file_batch_id , value = self.today.strftime('%Y-%m-%d %H:%M') ))
                                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = missing_asin_vl_upload_file_batch_id , value =  new_parent_batch_id_returned ))
                                    cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = false_parent_sku_column_name , value =  '' ))

                                    self.gsheet_job_log_Update.update_cells(cellsASIN) 
                                    print('New VL Added Successfully in sheet as well ')
                                    self.post.ProcessErrorLog(self, 1, "New VL Added Successfully in sheet as well ")
                                else:
                                    self.post.ProcessErrorLog(self, 1, "No VL Added Successfully UPDATED in sheet as well ")

                            else:
                                print('No batch ID found, no file uploaded, was about to Upload New VL ')
                                self.post.ProcessErrorLog(self, 2, f"No batch ID found, no file uploaded, was about to Upload New VL   ")

                        else:
                            self.post.ProcessErrorLog(self, 1, f"No batch file uploaded, so existing VL still persists and thus no new VL upload as could find it by parent asin name ")
                else:
                    print("No need to upload  new VL upload")
                    self.post.ProcessErrorLog(self, 1, f"No need to upload  new VL upload ")
            
            ### time difference to upload SAS -  for previous DELETION of ASIN 
            if gsheet_Last_Row[false_parent_sku_time_column] != '':
                current_datetime = datetime.now()
                time_difference = current_datetime -  datetime.strptime(gsheet_Last_Row[false_parent_sku_time_column], '%Y-%m-%d %H:%M')   
                threshold = timedelta(hours=self.Sas_create_time)
            
            ### Sending SAS case,  Previous batch file is uploaded, time threshold crossed and last sas time is null
            if gsheet_Last_Row[false_parent_sku_column_name] != '' and time_difference > threshold  and  gsheet_Last_Row[false_parent_sku_SAS_time_column] == '' :
                    
                    # SAS CREATION
                    batch_id_returned = gsheet_Last_Row[false_parent_sku_column_name]
                    print(f"\nRunning SAS operations for false parent as time exceeded for more than {self.Sas_create_time} hour.")
                    headline = f" Child ASINs unable to SPLIT - Parent ASIN {v}  Parent SKU {parent_sku}"
                    sku_line = f"Can't split child ASINs from Parent ASIN {v} - Parent SKU {parent_sku}"
                    subject = f"Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs Can't Add into VL for Parent ASIN {v}__{self.today.strftime('%Y-%m-%d')}"                                
                    case_ID_generated = self.seller_support_case(v, subject, Child_ASINs = all_child_asins, batch_id= batch_id_returned )
        
                    file_path = self.create_SAS_case_PARENT_SKU(v, all_child_asins, parent_sku)
                    if file_path:
                        self.SAS_IO_with_parent_sku = self.SAS_issue_assistance(v, case_ID_generated, subject,
                                                                                    mail_type="Email" , file_path = file_path, 
                                                                                    sku_line = sku_line, parent_sku = parent_sku,
                                                                                    True_parent = True, headline=headline,
                                                                                    child_Asins=' '.join(all_child_asins),
                                                                                    batch_id= batch_id_returned)
                        
                        subject = f"Child ASINs unable to SPLIT - Parent ASIN {v} with sku {parent_sku} | A31LSP1L7F6XJ2__{self.today.strftime('%Y-%m-%d')}"
                        self.SAS_IA_with_parent_sku = self.SAS_issue_assistance(v, case_ID_generated, subject, mail_type="HTML", 
                                                                                    file_path = file_path, sku_line = sku_line, 
                                                                                    parent_sku = parent_sku, True_parent = True, 
                                                                                    headline = headline, child_Asins=' '.join(all_child_asins),
                                                                                    batch_id= batch_id_returned)

                        print( 'SUBJECTS ~ \n' ,case_ID_generated,self.SAS_IO_with_parent_sku, self.SAS_IA_with_parent_sku )
                        print(" ~ \tCreated Seller Support Cases for Parent Asins with SKUs - VL Deletion")
                        self.post.ProcessErrorLog(self, 1, " Created Seller Support Cases for Parent Asins with SKUs - VL Deletion ")
                        
                        ## updated the column for false parent sas
                        cellsASIN=[]
                        time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc( false_parent_sku_SAS_time_column )  + 1
                        case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('FALSE VL WITH SKU - SELLER SUPPORT')  + 1
                        SAS_IA_parent_sku_column = self.gsheetData_job_log.columns.get_loc('FALSE VL WITH SKU SAS  - IA')  + 1
                        SAS_IO_parent_sku_column_column = self.gsheetData_job_log.columns.get_loc('FALSE VL WITH SKU  - IO')  + 1
                        
                        
                        cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = time_case_ID_generated_column       , value =  datetime.today().strftime('%Y-%m-%d %H:%M') ))     
                        cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = case_ID_generated_column            , value =  case_ID_generated      ))
                        cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = SAS_IO_parent_sku_column_column     , value =  self.SAS_IO_with_parent_sku  ))  
                        cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = SAS_IA_parent_sku_column            , value =  self.SAS_IA_with_parent_sku ))
                        
                        print(' delete_false_parent_with_sku method completed and updated')
                        self.post.ProcessErrorLog(self, 1, " delete_false_parent_with_sku method completed and updated ")                    
                        self.gsheet_job_log_Update.update_cells(cellsASIN) 
                    else:
                        self.post.ProcessErrorLog(self, 1, f' {file_path} Error, as it came out to be None, kindly check the method - create_SAS_case_PARENT_SKU ')
                        self._ManualLog = 'create_SAS_case_PARENT_SKU file None'

            ### Informing User
            if gsheet_Last_Row[false_parent_sku_SAS_time_column] and not gsheet_Last_Row['False_vl_with_sku_notified_user']:
                
                cellsASIN = []
                _Last_SAS_Date = datetime.strptime(gsheet_Last_Row[false_parent_sku_SAS_time_column], '%Y-%m-%d %H:%M')   
                self.post.ProcessErrorLog(self, 1, f"False parent with SKU , gonna inform the user") 
                current_datetime = datetime.now()
                time_difference = current_datetime - _Last_SAS_Date
                threshold_inform_user = timedelta(hours=self.threshold_inform_user_time)
                if time_difference > threshold_inform_user  :
                    subject = 'False parent with sku ' + datetime.today().strftime('%Y-%m-%d %H:%M')
                   
                    
                    body = f"""
Hi,

For Brand {self.VL_Name}'s -  False parent with sku  {self.ParentTrueFalse["ParentFalse"]}\n
not yet deleted. Thus, the system won't be able to Create New VL.

Please modify accordingly.

Thanks
                    """
                    
                    self.inform_users_via_mail(subject, body)
                    
                    inactive_user_column = self.gsheetData_job_log.columns.get_loc('False_vl_with_sku_notified_user')  + 1
                    cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column , value =  " notified user_"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                    
                    self.gsheet_job_log_Update.update_cells(cellsASIN) 
                    print('False parent with sku not yet deleted ')
                    self.post.ProcessErrorLog(self, 1, f"False parent with sku not yet deleted") 
                     
        def delete_false_parent_without_sku():

            print("Starting with Immediate Action. for seller support  ~ DELETE FALSE PARENT ASIN WITHOUT SKUs  !\n")
            self.post.ProcessErrorLog(self, 1, f" Starting with Immediate Action. for seller support  ~ DELETE FALSE PARENT ASIN WITHOUT SKUs ")
      
            false_parent__without_sku_SAS_time_column = 'Time of FALSE VL WITHOUT SKU SAS'
            false_paren_without_sku_column_seller_support = 'FALSE VL WITHOUT SKUSAS - SELLER SUPPORT'
            false_paren_without_sku_column_IA = 'FALSE VL WITHOUT SKU SAS  - IA'
            false_paren_without_sku_column_IO = 'FALSE VL WITHOUT SKUSAS  - IO'


            self.post.ProcessErrorLog(self, 1, f" Going to Delete False parent without SKu ")
            
            ### ENTRY point for SAS Case for PARENT VL Without  SKU if last entry is null
            if  gsheet_Last_Row[false_parent__without_sku_SAS_time_column] == '' :

                self.post.ProcessErrorLog(self, 1, f" Immediate Action. gonna send the SAS cases for extra asins")
                subject = f"Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs unable to SPLIT - Parent ASIN {v} contains NO SKU__{self.today.strftime('%Y-%m-%d')}"
                case_ID_generated = self.seller_support_case(v, subject, Child_ASINs = all_child_asins )
                
                file_path = self.create_SAS_case_PARENT_NO_SKU(v, all_child_asins)
                if file_path:
                    headline = f"Child ASINs unable to SPLIT - Parent ASIN {v} contains NO SKU" 
                    sku_line = f"Can't split child ASINs from Parent ASIN {v} without Parent SKU" 
                    line = "No Parent SKU"

                    
                    self.SAS_IO_without_parent_sku = self.SAS_issue_assistance(v, case_ID_generated, subject, 
                                                                                mail_type="Email" , file_path = file_path, 
                                                                                sku_line = sku_line, parent_sku = ' ', 
                                                                                line = line,child_Asins=' '.join(all_child_asins),
                                                                                True_parent = True )
                    
                    subject = f"Child ASINs unable to SPLIT - Parent ASIN {v} contains NO SKU | A31LSP1L7F6XJ2__{self.today.strftime('%Y-%m-%d')}"
                    self.SAS_IA_without_parent_sku = self.SAS_issue_assistance(v, case_ID_generated, subject, mail_type="HTML", 
                                                                                file_path = file_path, sku_line = sku_line, 
                                                                                parent_sku = ' ', headline = headline,
                                                                                line = line, child_Asins=' '.join(all_child_asins),
                                                                                True_parent = True)
                    print('Subjects \n')
                    print(  self.SAS_IO_without_parent_sku )
                    print(  self.SAS_IA_without_parent_sku )
                    print("\n\tCreated Seller Support Cases for Parent Asins without SKUs - VL Deletion  \t")
                    self.post.ProcessErrorLog(self, 1, "Created Seller Support Cases for Parent Asins without SKUs - VL Deletion ")

                    
                    ### updated the column  for sas cases
                    cellsASIN=[]
                    time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc(false_parent__without_sku_SAS_time_column)  + 1
                    case_ID_generated_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_seller_support)  + 1
                    SAS_IO_without_parent_sku_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_IO)  + 1
                    SAS_IA_without_parent_sku_column = self.gsheetData_job_log.columns.get_loc(false_paren_without_sku_column_IA)  + 1
                    
                    inactive_user_column = self.gsheetData_job_log.columns.get_loc('delete_false_parent_without_sku_notified')  + 1
                    cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column, value =  ""    ))
                    
                    cellsASIN.append(Cell(row = index + 2, col = time_case_ID_generated_column    , value =  datetime.today().strftime('%Y-%m-%d %H:%M') ))     
                    cellsASIN.append(Cell(row = index + 2, col = case_ID_generated_column         , value =  case_ID_generated      ))
                    cellsASIN.append(Cell(row = index + 2, col = SAS_IO_without_parent_sku_column , value =  self.SAS_IO_without_parent_sku    ))
                    cellsASIN.append(Cell(row = index + 2, col = SAS_IA_without_parent_sku_column , value =  self.SAS_IA_without_parent_sku    ))
                    print('Case file missing unmatch file Uploaded  successfully');self.post.ProcessErrorLog(self, 1, "Case file missing unmatch asin successfully ")
                    
                    self.gsheet_job_log_Update.update_cells(cellsASIN) 
                    print('Subjects noted  successfully in excel sheet')
                    self.post.ProcessErrorLog(self, 1, "Subjects noted  successfully in excel sheet ")
                else:
                    self.post.ProcessErrorLog(self, 1, f' {file_path} Error, as it came out to be None, kindly check the method - create_SAS_case_PARENT_NO_SKU ')
                    self._ManualLog = 'create_SAS_case_PARENT_NO_SKU file None'

            ### Making sure SAS is created and user is not notified earlier then we Notify the User about it
            if  gsheet_Last_Row[false_parent__without_sku_SAS_time_column] and not  gsheet_Last_Row['delete_false_parent_without_sku_notified'] :
                cellsASIN = []
                _Last_SAS_Date = datetime.strptime(gsheet_Last_Row[false_parent__without_sku_SAS_time_column], '%Y-%m-%d %H:%M')   
                self.post.ProcessErrorLog(self, 1, f"False parent without SKU , gonna inform the user") 
                current_datetime = datetime.now()
                time_difference = current_datetime - _Last_SAS_Date
                threshold_inform_user = timedelta(hours=self.threshold_inform_user_time)
                if time_difference > threshold_inform_user  :
                    
                    inactive_user_column = self.gsheetData_job_log.columns.get_loc('delete_false_parent_without_sku_notified')  + 1
                    cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column, value =  "notified user_"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                    
                    time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('Time of FALSE VL WITHOUT SKU SAS')  + 1
                    cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = time_case_ID_generated_column    , value = ""))
                    
                    subject = 'False parent without sku ' + datetime.today().strftime('%Y-%m-%d %H:%M')
                   
                    
                    body = f"""
Hi,

For Brand {self.VL_Name}'s -  False parent without sku  {self.ParentTrueFalse["ParentFalse"]}\n
not yet deleted. Thus, the system won't be able to continue ahead.

Please modify accordingly.

Thanks
                    """
                    
                    self.inform_users_via_mail(subject, body)
                    print('False parent withour sku not yet deleted ')
                    self.gsheet_job_log_Update.update_cells(cellsASIN) 
                    self.post.ProcessErrorLog(self, 1, f"False parent withour sku not yet deleted, thus notified user ") 
                     
            
            
        """  
            - Taking action on VL Deletion     with or without Parent SKU
        """    
        all_child_asins = ' '
        ### ( False Only ) TRUE PARENT == ' '   &  FALSE PARENT == TRUE     >>> Will Delete Existing False Parent With or Without SKU and Upload New VL
        if  (self.ParentTrueFalse['ParentTrue'] == '') and (self.ParentTrueFalse['ParentFalse'] != ''  ) :
            
            self.inform_users_via_mail(F"Found False parent in {self.VL_Name}",f'Please check - {str(self.ParentTrueFalse)}' ,me = True)
            
            v = self.ParentTrueFalse['ParentFalse']
            self.post.ProcessErrorLog(self, 1, f"Found False parent {v} - with no True parent ")
            try:
                all_child_asins = list(self.VLList[(self.VLList['RequestASIN'] == v ) & (self.VLList['ASIN'].isin(self.MissingASINs) )]['ASIN'].unique())
            except Exception as e:
                self.post.ProcessErrorLog(self, 1, 'No child found in vl list for the false parent, lets check with other methods')
            parent_sku = ''
            if not all_child_asins:
                print('Missing asins found, mapped all the missing child asins with the false parent  ')
                self.post.ProcessErrorLog(self, 2, f"Missing asins found, mapped all the missing child asins with the false parent")
                all_child_asins = self.mapped_parent_child_items.get(v)
                if not all_child_asins:
                    all_child_asins =   list(self.VLList[(self.VLList['RequestASIN'] == v )& (self.VLList['ASIN']  != v) ]['ASIN'].unique()   )
            if not self.VLList.empty:
                parent_sku = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == v)]['SKU'].iloc[0]
            if not parent_sku: print('No parent sku found for False Parent from vl list file ');self.post.ProcessErrorLog(self, 2, f"No parent sku found for False Parent from vl list file")
            print('Parent ',v, 'SKU\t~', parent_sku)
            self.post.ProcessErrorLog(self, 1, f" parent sku for false VL {parent_sku}")
            self.post.ProcessErrorLog(self, 1, f"Parent {v} - Sku {parent_sku}")
            
            index = self.gsheetData_job_log.shape[0] -1

            
            ### DELETE FALSE PARENT ASIN WITH SKUs
            if parent_sku:
                delete_false_parent_with_sku(vl_upload = True)

            ### DELETE FALSE PARENT ASIN WITHOUT SKUs ###
            else:
                delete_false_parent_without_sku()

        ### ( Both True  ) TRUE PARENT == TRUE  &  FALSE PARENT == TRUE     >>> Will Delete False Parent With or Without SKU
        elif ( self.ParentTrueFalse['ParentTrue'] != '') and ( self.ParentTrueFalse['ParentFalse'] != '') :
            
            self.inform_users_via_mail(F"Found False and True Parents  in {self.VL_Name}",f'Please check  - {str(self.ParentTrueFalse)}' ,me = True)
            
            v = self.ParentTrueFalse['ParentFalse']
            self.post.ProcessErrorLog(self, 1, f" Found the False parent {v} - with  True parent as well , gonna delet the false parent")
            try:
                all_child_asins = list(self.VLList[(self.VLList['RequestASIN'] == v ) & (self.VLList['ASIN'].isin(self.MissingASINs) )]['ASIN'].unique())
            except:
                ...
            parent_sku = ''
            if not all_child_asins: 
                print(' parent asin -   child asins dont have relationship with any of the missing asins ')
                self.post.ProcessErrorLog(self, 2, f"parent asin - child asins dont have relationship with any of the missing asins")
                all_child_asins = self.mapped_parent_child_items.get(self.ParentTrueFalse['ParentFalse'])
              
            if not self.VLList.empty:
                parent_sku = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == v)]['SKU'].iloc[0]
            if not parent_sku: print('No parent sku found for False Parent from vl list file ')
            self.post.ProcessErrorLog(self, 2, f"No parent sku found for False Parent from vl list file")
            index = self.gsheetData_job_log.shape[0] - 1
            
            print('Parent ',v, 'SKU\t~', parent_sku)
            self.post.ProcessErrorLog(self, 1, f" parent sku for false VL {parent_sku}")

            if parent_sku:
                delete_false_parent_with_sku(vl_upload = False)
                    
            ## DELETE FALSE PARENT ASIN WITHOUT SKUs ###
            else:
                if not all_child_asins:
                    all_child_asins =   list(self.VLList[(self.VLList['RequestASIN'] == v )& (self.VLList['ASIN']  != v) ]['ASIN'].unique()   )                
                delete_false_parent_without_sku()

        ### ( Both False ) TRUE PARENT == ' '   &  FALSE PARENT == ' '      >>> Recheck previous Parent if not Exists and Upload New VL
        elif (self.ParentTrueFalse['ParentTrue'] == '') and (  self.ParentTrueFalse['ParentFalse'] == '') :
            
            self.inform_users_via_mail(F"Not Found any MAIN VL Parent in {self.VL_Name}",f'Please check - {str(self.ParentTrueFalse)}' ,me = True)

            googleAPI = 'GoogleCredentials\client_sheet.json'
            scope = ['https://www.googleapis.com/auth/drive']
            credentials = service_account.Credentials.from_service_account_file(googleAPI)
            scopedCreds = credentials.with_scopes(scope)
            gc = gspread.Client(auth=scopedCreds)
            gc.session = AuthorizedSession(scopedCreds)    

            gsheetdata_parent_sku = gc.open(self._brand_file_name).worksheet('Parent SKU')      
            gsheetdata_parent_sku_data = [i[:5] for i in gsheetdata_parent_sku.get_all_values()[6:]]
            
            if self.VL_Name != 'Gya EOS ':
                last_used_entries_skus = [i[1] for i in  [entry for entry in gsheetdata_parent_sku_data if entry[2] == 'Used' and entry[4]!='']]
                last_used_entries_names = [i[4] for i in  [entry for entry in gsheetdata_parent_sku_data if entry[2] == 'Used'] if i[4]]
            else:
                last_used_entries_skus = [i[0] for i in  [entry for entry in gsheetdata_parent_sku_data if entry[1] == 'Used' and entry[3]!='']]
                last_used_entries_names = [i[3] for i in  [entry for entry in gsheetdata_parent_sku_data if entry[1] == 'Used'] if i[3]]


            self.post.ProcessErrorLog(self, 1, f" Both True and False Parent Empty, Uploading new VL, But first lets check and delete all previous skus and their names  ")

            try:
                print('\nUploading New VL, as both True and False parents are null, But first lets check and delete all previous skus and their names ')
                index = self.gsheetData_job_log.shape[0] - 1

                self.post.ProcessErrorLog(self, 1, f" First checking with all previous sku and their names in manage inventory page if those exists or not ! ")
                result_deletion = False
                ### Check all previous Asin names and their SKUs and DELETE them
                skus_with_false_values = [sku for sku, value in zip(last_used_entries_skus, [ self.find_parent_vl(i) for i in  last_used_entries_skus]) if not value]
                skus_with_false_names_values = [sku for sku, value in zip(last_used_entries_names, [ self.find_parent_vl(i) for i in  last_used_entries_names]) if not value]
                skus_with_false_names_values = [i for i in skus_with_false_names_values if i ]
                skus_with_false_names_values = list(set(skus_with_false_names_values))
                skus_with_false_values = list(set(skus_with_false_values))
                if skus_with_false_values or skus_with_false_names_values: 
                    for i in zip(skus_with_false_values, skus_with_false_names_values) :
                        previous_sku = i[0] if len(skus_with_false_values) >= 0 else ''
                        previous_sku_name = i[1] if len(skus_with_false_names_values)>0 else ''
                        self.post.ProcessErrorLog(self, 1, f'Deleting Previous SKU and their name {previous_sku, previous_sku_name} ')    
                        print('previous_sku Found',previous_sku, '\tprevious_sku name found', previous_sku_name)  
                        
                        file_path_previous_sku_ = self.create_VL_Delete_SKU_upload("_", previous_sku )
                        time.sleep(1)
                        self.post.ProcessErrorLog(self, 1, f" Found previous sku {previous_sku}, will manually delete it and upload file and check status ")
                        

                        batch_id_returned = self.Delete1ASIN2SKU(previous_sku_name, function_run = 'delete' )
                        if batch_id_returned:
                            self.post.ProcessErrorLog(self, 1, f"Deleted previous_sku_name {previous_sku_name} - {batch_id_returned} with score status as Expected ")
                        else:
                            self.post.ProcessErrorLog(self, 1, f"Status not as Expected for name {previous_sku_name} While Deleting previous_sku_name , Retry... ")
                        
                        batch_id_returned = self.Delete1ASIN2SKU(previous_sku, filepath = file_path_previous_sku_, function_run = 'both' )
                        if batch_id_returned:
                            self.post.ProcessErrorLog(self, 1, f"Deleted previous_sku {previous_sku} - {batch_id_returned} with score status as Expected ")
                            result_deletion = True
                        else:
                            self.post.ProcessErrorLog(self, 1, f"Status not as Expected for sku {previous_sku} While Deleting previous_sku, Retry... ")
                else:
                    result_deletion = True
                if self.ParentTrueFalse['ParentTrue'] == '':
                    self.post.ProcessErrorLog(self, 1, f' No True Parent EXISTS {str(self.ParentTrueFalse)}  ');print(f' No True Parent EXISTS {str(self.ParentTrueFalse)}   ')
                # Then Upload New VL while checking if previous is deleted !
                if  result_deletion and gsheet_Last_Row['Main VL Upload status'] == ''  :
                    self.post.ProcessErrorLog(self, 1, f"Gonna Upload NEW VL")
                    new_sku = self.get_new_sku_google_sheet()
                    if not new_sku:
                        self.post.ProcessErrorLog(self, 1, f' No new Sku found,  ');print(f' No new Sku found,   ')
                        return
                    filepath = self.upload_vl_without_false_parent_sku(new_sku)
                    
                    self.post.ProcessErrorLog(self, 2, f"Going to Upload file for New parent VL as Existing Got deleted    ")
                    new_parent_batch_id_returned = self.Delete1ASIN2SKU(new_sku, 
                                                            function_run='upload' ,
                                                            filepath=filepath )
                    if  new_parent_batch_id_returned: 
                        time.sleep(60)
                        print("\nNew VL uploaded, get the parent asin ")
                        self.find_parent_vl(new_sku)
                        checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                        mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
                        if not checkbundle[0].text.startswith('You currently have no listings'): 
                            self.post.ProcessErrorLog(self, 1, "New VL Loaded Sucessfully, extracting the parent ASIN name")
                            for each_product in mtrowlis:
                                id = each_product.get_attribute('id')
                                name = each_product.find_element(by = By.ID, value=id + '-title')
                                name = name.text.split('\n')[2]
                                print(name)
                            print(f'\n Got the new parent asin {name}, extract it \n')
                            self.post.ProcessErrorLog(self, 1, f"Got the new parent asin {name}, extract it \n")
                            self.get_new_sku_google_sheet(name) # update google sheet with new name for the new asin name
                        else:
                            print("no New VL not Added Successfully")
                            self.post.ProcessErrorLog(self, 2, f"no New VL not Added Successfully , ALTHOUGH FILE UPLOADED SUCCESSFULLY  ")
                        
                        if not self.find_parent_vl(new_sku):
                            self.post.ProcessErrorLog(self, 1,"New VL Added Successfully")
                            self.post.ProcessErrorLog(self, 1, f"new_parent_batch_id_returned {new_parent_batch_id_returned}")
                            ## updated the new vl columnn with parent sku
                            cellsASIN=[]
                            Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Time of  Main VL Upload')  + 1
                            missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Main VL Upload status')  + 1
                            cellsASIN.append(Cell(row = index + 2, col = Time_missing_asin_vl_upload_file_batch_id , value = self.today.strftime('%Y-%m-%d %H:%M') ))
                            cellsASIN.append(Cell(row = index + 2, col = missing_asin_vl_upload_file_batch_id , value =  new_parent_batch_id_returned ))
                            
                            self.gsheet_job_log_Update.update_cells(cellsASIN) 
                            print('New VL Added Successfully in sheet as well ')
                            self.post.ProcessErrorLog(self, 1, "New VL Added Successfully in sheet as well ")
                        else:
                            print("no New VL not Added Successfully")
                            self.post.ProcessErrorLog(self, 2, f"NOT GONNA UPDATE THE SHEET AS No New VL not Added, Retry...    ")
                    else:
                        print('No batch ID found, no file uploaded as status score didnt matched, was about to Upload New VL, Retry...')
                        self.post.ProcessErrorLog(self, 2, f"No batch ID found, no file uploaded no file uploaded as status score didnt matched, was about to Upload New VL, Retry...  ")
                else:
                    print(f'From Previous parent  SKU deleted,  still previous sku exists , cant create new VL')
                    self.post.ProcessErrorLog(self, 2, f'Previous parent SKU still previous sku exists, cant create new VL' )
            except Exception as e:
                print('Issue in creating new VL\n')
                self.post.ProcessErrorLog(self, 2, f" New VL - not Uploaded Sucessfully {str(e)}")
                
        # RUN HISTORICAL DATA ON MISSINGS ASINS where PARENT == TRUE AND FALSE PARENT == ''
        else:
            if self.MissingASINs:
                
                self.inform_users_via_mail(F"Found missing ASINs in  {self.VL_Name}",f'Please check Missing ASINS - {str(self.MissingASINs)}  ' ,me = True)

                print('\nRunning Historical Data for Parent Asins as Only parent Exists  and  missing asins have been found \n')
                self.post.ProcessErrorLog(self, 1, f"Running Historical Data for Parent of missing asins ")
                self.get_historical_data(self.MissingASINs)
            else:
                self.post.ProcessErrorLog(self, 1, f" No Requirement of running Historical Data as No missings found ✔️ ")
      
    def get_historical_data(self, missing_asins):
        
        """
            ### HISTORICAL DATA ###
        """

        try:
           
          
            # self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
            # self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)
            
            data_values = self.gsheet_job_log_Update.get_all_values()
            headers = data_values[0]
            self.gsheetData_job_log = pd.DataFrame(data_values[1:], columns=headers)   
   

            gsheet_Last_index = self.gsheetData_job_log.shape[0] - 1
            gsheet_Last_Row = self.gsheetData_job_log.iloc[-1]


            """  
                - Taking action on MISSING ASINS
                - Checking the Skus from Manage inventory Page
            """    

            print('Checking historical data for each missing asin\n ')
            self.post.ProcessErrorLog(self, 1, "Checking Historical data for each missing asin ")

            
            missing_asins_Parent_child_map = {}
            for key, values in self.mapped_parent_child_items.items():
                temp_list = []
                for value in values:
                    if value in self.MissingASINs:
                        temp_list.append(value)
                if temp_list:
                    missing_asins_Parent_child_map[key] = temp_list
            rows = []
            parent_sku = ''
            if not missing_asins_Parent_child_map :
                missing_asins_Parent_child_map[''.join(list(self.mapped_parent_child_items.keys()))] = self.MissingASINs
            
            for asin in missing_asins:
                child = asin
                live_parent = " ".join(map(str, missing_asins_Parent_child_map.keys()))

                if live_parent == 'No Parent' or live_parent == '' or live_parent == ' ':
                    action = ' Historical Data Checks'
                else:
                    if parent_sku != 'Unknown':
                        action = 'Will be Deleting from flat file + manual'
                    else:
                        action = ' Historical Data Checks'
                timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                parent_sku = self.VLList[(self.VLList['Type']=='parent') & (self.VLList['ASIN'] == live_parent)]['SKU'].iloc[0]
            
                rows.append(
                            {'Timestamp': timestamp, 
                            'Child Asin': child, 
                            'Live Parent Asin': live_parent, 
                            'Parent Skus': parent_sku, 
                            "Active SKUS": '',
                            'Active Action': action , 
                            "Inactive SKUS":'',
                            'Inactive Action': 'Informed the user' ,
                            'Result': ''})
            new_df = pd.concat([pd.DataFrame([row]) for row in rows], ignore_index=True)    
                    

           
            ### check for historical data for each missing asin
            self.driver.get( self.CountryURL(self.CountryID, 2))
            matched_keys = []
            unmatched_keys = []
            inactive_keys = {}
            historical_data_list = missing_asins
            # print(historical_data_list)

            no_asins_found = []
            ### Checking historical data for each missing asin  ###
            for _ASIN in historical_data_list: 
                    
                    print("\n\t", _ASIN, '\n')
                    all_inactive_child_skus = []
                    all_active_child_skus = []
                    form = self.driver.find_element(by = By.ID,value='myitable-search-form')
                    inputbox = form.find_element(by = By.NAME,value='search')
                    time.sleep(2)
                    inputbox.clear()
                    time.sleep(1)
                    inputbox.send_keys(_ASIN)
                    time.sleep(1)
                    searchbtn = form.find_element(by = By.CLASS_NAME,value='a-button-inner')
                    searchbtn.click()
                    time.sleep(5)
                    checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                    time.sleep(1)
                    mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
                    if not checkbundle[0].text.startswith('You currently have no listings'): 
                        for each_product in mtrowlis:
                            id = each_product.get_attribute('id') 
                            status = each_product.find_element(by = By.ID, value=id + '-status')
                            sku = each_product.find_element(by = By.ID, value=id + '-sku-sku')
                            child_sku= sku.text.replace('\nNew','')
                            if status.text:
                                # print('\n',status.text)
                                
                                if status.text.startswith("Inactive") or status.text.startswith("Incomplete"):
                                    print(f"For ASIN {_ASIN} ~ SKU {sku.text}  Status is  inactive" ,"Informing the user")
                                    self.post.ProcessErrorLog(self, 1, f"For ASIN {_ASIN} ~ SKU {sku.text}  Status is  inactive, Will Inform the user")
                                    inactive_keys[sku.text] = _ASIN
                                    all_inactive_child_skus.append(child_sku)
                                    continue
                                
                                else:
                                    print(f"\nFor ASIN {_ASIN} ~ Status is Active {sku.text}  ")
                                    self.post.ProcessErrorLog(self, 1, f"For ASIN {_ASIN} ~ Status is Active {sku.text}  ")
                                    button = each_product.find_element(by = By.ID, value=id+'-action').find_element(By.CLASS_NAME,'a-dropdown-prompt')
                                    button.click()
                                    time.sleep(13)

                                    self.driver.switch_to.window(self.driver.window_handles[1])
                                    try:
                                        variation_button = self.driver.find_element(By.ID,'variations-link')
                                        variation_button.click()
                                    except:
                                        self.driver.find_element(By.PARTIAL_LINK_TEXT,'Variations').click()
                                    time.sleep(4)
                                    
                                    try:
                                        query = ' iframepath = document.querySelector("#variations-details > div.qDEMCDizuqCjrxkUNcha > section > div > div > div.lDXuuEc2TWjgcu688eII > div > div > section > span > kat-link").shadowRoot.querySelector("a > slot > span").textContent;'
                                        query=query + ' return iframepath'
                                        variation_number = self.driver.execute_script(query) 
                                    except:
                                        self.driver.find_element(By.CLASS_NAME,'rB6DuUEkdeOxGb0e0pba').text
                                        self.post.ProcessErrorLog(self, 1, "No Variation Number found ")
                                        print('No variation number detected for the same')
                                        variation_number = None
                                
                                    if not variation_number:
                                        print("No Variation Number found, adding it to MAIN VL")
                                        self.post.ProcessErrorLog(self, 1, "No Variation Number found, adding it to MAIN VL ")
                                        self.list_of_no_historical_bg_asins[child_sku] = _ASIN
                                        if _ASIN in self.list_of_no_historical_bg_asins:
                                            self.list_of_no_historical_bg_asins.pop(_ASIN)
                                        self.driver.close()
                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                    else:
                                        print("Found the Variation  Number of the above Active SKU",variation_number,f"Gonna match with the parent sku {parent_sku} from portal in below code \n ")
                                        self.post.ProcessErrorLog(self, 1, f"Found the Variation  Number of the above Active SKU {variation_number} Gonna match with the parent sku {parent_sku} from portal in below code ")
                                        all_active_child_skus.append({child_sku:variation_number})

                                        self.driver.close()
                                        self.driver.switch_to.window(self.driver.window_handles[0])

                    else: print(f'ASIN {_ASIN} does not exist in the manage inventory portal'); self.post.ProcessErrorLog(self, 1, f'ASIN {_ASIN} does not exist in the manage inventory portal'); no_asins_found.append(_ASIN)
                    new_df.loc[new_df['Child Asin'] == _ASIN, 'Inactive SKUS'] = ', '.join(all_inactive_child_skus)
                    all_active_child_skus_result = ', '.join([f"{k}: {v} " for sku_dict in all_active_child_skus for k, v in sku_dict.items()])

                    """ CONFIRMING HISTORICAL DATA FOR ALL Active ASINS """
                    for sku_dict in all_active_child_skus:
                        for k, v in sku_dict.items():
                            matching_row = new_df.loc[new_df['Child Asin'] == _ASIN]
                            if not matching_row.empty:
                                parent_sku = matching_row['Parent Skus'].iloc[0]
                                if v == parent_sku:
                                    print(f"\t==  Variation Number Matched {variation_number} ")
                                    self.post.ProcessErrorLog(self, 1, f" Variation Number Matched {variation_number} ")
                                    matched_keys.append({k:_ASIN})
                                else:
                                    print(f"\t== NOT Matched child SKU {k} of child asin {_ASIN} with the historical data with variation number {variation_number} ")
                                    self.post.ProcessErrorLog(self, 1, f"Not Matched child SKU {k} of child asin {_ASIN} with the historical data with variation number {variation_number} ")
                                    unmatched_keys.append({k:_ASIN})
                        
                      
            
                    new_df.loc[new_df['Child Asin'] == _ASIN, 'Active SKUS'] = all_active_child_skus_result
           
            print("\n\t- Collected All skus of each Missing Child ASIN, now gonna work for Checking historical data for each active ASIN\n")    
            if self.list_of_no_historical_bg_asins:
                matched_keys.append(self.list_of_no_historical_bg_asins)
            
            if no_asins_found and not gsheet_Last_Row['No_child_in_Manage_inventory'] :
                no_asins_found = list(set(no_asins_found))
                body = f"""
Hi,

For Brand {self.VL_Name}'s -  Missing ASINS does not exist in the manage inventory portal\n

ASINS: { ' '.join(no_asins_found) }  

Please modify accordingly.

Thanks
                """
                
                print(body  )
                cellsASIN = []
                
                subject = f"All Missings Asins not in Manage inventory in  {self.VL_Name}" + datetime.today().strftime('%Y-%m-%d %H:%M') 
                missing_asin_in_inventory = self.gsheetData_job_log.columns.get_loc('No_child_in_Manage_inventory')  + 1
                cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = missing_asin_in_inventory, value =  f"notified user - {datetime.today().strftime('%Y-%m-%d %H:%M')}"     ))
                self.inform_users_via_mail(subject, body )
                self.gsheet_job_log_Update.update_cells(cellsASIN) 
                self.post.ProcessErrorLog(self, 1, f" Informed user for All missing_asin_in_inventory  { ' '.join(no_asins_found)  } ")
            


            if inactive_keys and not gsheet_Last_Row['Inactive_case_notified_users']:
                cellsASIN = []
                print("\nInforming User for Inactive ASIN")
                common_inactive_keys_asin = {}
                for key, value in inactive_keys.items():
                    if value in common_inactive_keys_asin:
                        common_inactive_keys_asin[value] += (key,)
                    else:
                        common_inactive_keys_asin[value] = (key,)
                
                body = f"""
Hi,

For Brand {self.VL_Name}'s -  Missing ASINS\n

Inactive keys found: { ' '.join(list(common_inactive_keys_asin.values())[0])  }  
Mapped to child ASIN: { str(list(common_inactive_keys_asin.keys())[0])  }

Please modify accordingly.

Thanks
                """
                
                print(body  )
                subject = f"All Inactive Asins for {self.VL_Name}" + datetime.today().strftime('%Y-%m-%d %H:%M') 
                inactive_user_column = self.gsheetData_job_log.columns.get_loc('Inactive_case_notified_users')  + 1
                cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = inactive_user_column, value =  f"notified user_ {datetime.today().strftime('%Y-%m-%d %H:%M')}"     ))
                self.inform_users_via_mail(subject, body )
                self.gsheet_job_log_Update.update_cells(cellsASIN) 
                self.post.ProcessErrorLog(self, 1, f" Informed user for All Inactive Keys {  ' '.join(list(common_inactive_keys_asin.values())[0]) } ")
            
            if matched_keys:

                try:
                    filtered_Last_SAS_Date = None
                    print("\nGoing for matched Cases of Historical data missing asins "); self.post.ProcessErrorLog(self, 1, "Going for matched Cases ")
                    self.post.ProcessErrorLog(self, 1, f"All Matched Keys { matched_keys } ")
                    
                    filtered_Last_SAS = self.gsheetData_job_log[(self.gsheetData_job_log['Missing file VL Upload Status'] != '')]
                    if len(filtered_Last_SAS) > 0 :
                        filtered_Last_SAS = filtered_Last_SAS.iloc[-1]
                        if filtered_Last_SAS['Time of VL Upload']:
                            filtered_Last_SAS_Date = datetime.strptime(filtered_Last_SAS['Time of VL Upload'], '%Y-%m-%d %H:%M')   
                        else:
                            filtered_Last_SAS_Date = self.gsheetData_job_log[self.gsheetData_job_log['Time of VL Upload'] !=''][-1:]['Time of VL Upload']
                            filtered_Last_SAS_Date = datetime.strptime(filtered_Last_SAS_Date.values[0], '%Y-%m-%d %H:%M')   
                            self.post.ProcessErrorLog(self, 1, f"No latest date found to be converted ") 
                            
                    match_filtered_Last_ml_status_value_dict = self.gsheetData_job_log[self.gsheetData_job_log['Missing file VL Upload Status'] !=''][-1:]['Missing file VL Upload Status']
                    if match_filtered_Last_ml_status_value_dict.values:
                        try:
                            match_filtered_Last_ml_status_value_dict = eval(match_filtered_Last_ml_status_value_dict.values.tolist()[0])
                            previous_row_skus = list(match_filtered_Last_ml_status_value_dict.values())[0]
                        except Exception as e:
                            self.post.ProcessErrorLog(self, 2, "  Check for the previous values under column Missing file VL Upload Status, as it couldnt find any dict ")                  
                    else:
                        previous_row_skus = []

                    if  filtered_Last_SAS_Date:
                        ### time difference of upload time for sas case
                        current_datetime = datetime.now()
                        time_difference = current_datetime - filtered_Last_SAS_Date 
                    else:
                        time_difference = datetime.now()




                    all_new_child_skus = list(set([k for item in matched_keys for k,v in item.items()]))
                    previous_row_skus = previous_row_skus
                    check =  all_new_child_skus == previous_row_skus
                    _new_items = list( set( all_new_child_skus )  - set ( previous_row_skus ) )
                    _new_child_skus_to_upload = ''

                    ### entry point 
                    self.post.ProcessErrorLog(self, 1, "Found new item for Matching Missing Data  ")
                    if  _new_items and not check   :

                        _new_child_skus_to_upload = _new_items

                        file_path = self.upload_file_missing_asin(parent_sku, asins_list=_new_child_skus_to_upload)
                    

                        if not file_path : 
                            print(f'New SKUs items  {str(_new_items)} not in latest template sheet')
                            self.post.ProcessErrorLog(self, 1, f'New SKUs items {str(_new_items)} not in latest template sheet  ')
                            self._ManualLog = f'Template Issue - UnMatching SKUs {str(_new_items)} not present in Latest Template in {self.VL_Name}  '
                            return False
                        
                        
                        
                        time.sleep(1.5)
                        
                        self.post.ProcessErrorLog(self, 1, "Going to create and upload the file for Matching Missing Data  ")
                        batch_id_returned = self.Delete1ASIN2SKU(parent_sku, function_run ='upload' , filepath = file_path )  
                        if  batch_id_returned and file_path: 

                            ## update the column "Missing file VL Upload Status"
                            cellsASIN=[]
                            Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Time of VL Upload')  + 1
                            missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc('Missing file VL Upload Status')  + 1
                            time_missing_sas = self.gsheetData_job_log.columns.get_loc('Time Missing Sas')  + 1
                            
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2 , col = Time_missing_asin_vl_upload_file_batch_id , value = datetime.today().strftime('%Y-%m-%d %H:%M') ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2 , col = missing_asin_vl_upload_file_batch_id , value =  str({batch_id_returned: list(set(_new_child_skus_to_upload))  }) ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2 , col = time_missing_sas , value =  ''  ))
                            print(' Created New entry for matching Missing asins with the historical data  ')
                            self.post.ProcessErrorLog(self, 1, "  Created New entry for matching Missing asins with the historical data ")                    
                            self.gsheet_job_log_Update.update_cells(cellsASIN)
                        else:    
                            print('No batch ID found, or Status score not appropriate, Kindly modify the file or else will later ')
                            self.post.ProcessErrorLog(self, 2, f"No batch ID found, or Status score not appropriate, Kindly modify the file or else will later  ")

                    ### SAS
                    # if gsheet_Last_Row['Missing file VL Upload Status'] != '' and time_difference > threshold_sas  and not gsheet_Last_Row['Time Missing Sas']   :    ### entry for SAS case after 4 hours of file upload
                    else: 
                    
                        print("No new items to be updated in job log sheet, going to check for previous Upload Files batch ID's SAS case ")
                        self.post.ProcessErrorLog(self, 1, "No new items to be updated in job log sheet, going to check for previous Upload File SAS case ")
                        if gsheet_Last_Row['Missing file VL Upload Status'] != '' and not gsheet_Last_Row['Time Missing Sas']   :
                            print('Initiating SAS case  for  Missing Asins with historical data ')
                            self.post.ProcessErrorLog(self, 1, "initiating SAS case asin for  Missing Asins with historical data  ")  
                            batch_id_returned = gsheet_Last_Row['Missing file VL Upload Status']
                            batch_id_returned = list(eval(batch_id_returned).keys())[0]


                            result = {} 
                            for item in matched_keys:
                                key, value = next(iter(item.items()))
                                if value in result:
                                    result[value] += (key,)
                                else:
                                    result[value] = (key,)
                            print(result)

                            ''' Create the file sent to SAS '''
                            wb_append = xw.Book(self.file_matching_historical_data)
                            sheet = wb_append.sheets['Template - Variations Update']
                            sheet.api.Unprotect() 
                            time.sleep(2)
                            next_row = 13
                            count_of_asins = 0
                            for common_value, child_asin_list in result.items():
                                for child_asin in child_asin_list:
                                    count_of_asins +=1 
                                    sheet.cells(next_row, 2).value = common_value 
                                    sheet.cells(next_row, 3).value = child_asin
                                    sheet.cells(next_row, 4).value = parent_sku
                                    sheet.cells(next_row, 5).value = "Size-Scent"
                                    sheet.cells(next_row, 9).value = "Yes"
                                    next_row += 1
                            file_path_SAS = f"{self.Saved_Missing_variation_path}{self.VL_Name}Amazon_Variations_A31LSP1L7F6XJ2_Gya Group {count_of_asins} ASINs in Main VL__{self.today.strftime('%Y-%m-%d')}.xlsx"
                            wb_append.save(file_path_SAS)
                            wb_append.app.quit()
                            print("\n Missing asins Matched cases DONE EDITING EXCEL FILE For matched Historical Data keys SAS \n") 
                            self.post.ProcessErrorLog(self, 1, f"DONE EDITING EXCEL FILE For matched Historical Data keys SAS ")
                            time.sleep(3)
                            subject = f"Child ASINs Can't Add into VL for Parent ASIN {live_parent }__{self.today.strftime('%Y-%m-%d')}"
                            print("\n Immediately Creating SAS cases  for matching records asins list ")
                            self.post.ProcessErrorLog(self, 1, f"Immediately Opening Seller Support cases for Matched Keys ")
                            case_ID_generated = self.seller_support_case(  live_parent , subject ,missing_asins_text='Missing ASIN', 
                                        Child_ASINs=' '.join(list(set([v for i in matched_keys for v in i.values()])) ) , 
                                        count_of_asins=count_of_asins, batch_id= batch_id_returned )
                
                            sku_line = f"Partial update to add {count_of_asins} ASINs via uploading flat file, successful but not reflect on live site, batch id: {batch_id_returned}"
                            subject = f"Amazon_Variations_A31LSP1L7F6XJ2_Child ASINs Can't Add into VL for Parent ASIN  { live_parent }__{self.today.strftime('%Y-%m-%d')} -  Missing ASINs"
                            self._Missing_case_SAS_IO_Matching = self.SAS_issue_assistance(live_parent, case_ID_generated, subject, 
                                                                mail_type="Email", file_path = file_path_SAS, 
                                                                sku_line = sku_line, parent_sku = parent_sku, 
                                                                missing_asins_text="ACTIVE ASINS", count_ = count_of_asins,
                                                                batch_id= batch_id_returned )
                            
                            
                            subject = f"Amazon_Variations_A31LSP1L7F6XJ2_ {count_of_asins} Child ASINs Can't Add into Parent ASIN {live_parent}  with parent sku {parent_sku}  | {self.today.strftime('%Y-%m-%d')}  - Missing ASINs"
                            headline = f"{count_of_asins} Child ASINs Can't Add into Parent ASIN {live_parent}"
                            self._Missing_case_SAS_IA_Matching = self.SAS_issue_assistance(live_parent, case_ID_generated, subject, 
                                                                mail_type="HTML", file_path = file_path_SAS, 
                                                                sku_line = sku_line, parent_sku = parent_sku, 
                                                                missing_asins_text="ACTIVE ASINS", count_ = count_of_asins,
                                                                headline = headline, batch_id= batch_id_returned )

                            
                            print( 'SUBJECTS ~ \n')
                            print(  self._Missing_case_SAS_IO_Matching )
                            print(  self._Missing_case_SAS_IA_Matching )
                            print("Created Seller Support Cases for Missing Asins  ~ Matched Keys \t")
                            self.post.ProcessErrorLog(self, 1, f"Created Seller Support Cases for Missing Asins ~ Matched Keys ")
                            

                            ## updated the column "Missing file VL Upload Status"
                            cellsASIN=[]
                            time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('Time Missing Sas')  + 1
                            case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('Missing ASINS SAS - SELLER SUPPORT')  + 1
                            Missing_case_SAS_IA_Matching_column = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IA_Matching')  + 1
                            Missing_case_SAS_IO_Matching_column = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IO_Matching')  + 1
                            
                            
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = time_case_ID_generated_column       , value =  datetime.today().strftime('%Y-%m-%d %H:%M')  ))     
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = case_ID_generated_column            , value =  case_ID_generated      ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Missing_case_SAS_IO_Matching_column , value =  self._Missing_case_SAS_IO_Matching    ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Missing_case_SAS_IA_Matching_column , value =  self._Missing_case_SAS_IA_Matching    ))
                            
                            print('For Matching Asins missing  file Uploaded  successfully')
                            self.post.ProcessErrorLog(self, 1, "For Matching Asins missing  fille Uploaded successfully ")                        
                            self.gsheet_job_log_Update.update_cells(cellsASIN) 
                            print('Updated Excel sheet as well');self.post.ProcessErrorLog(self, 1, "Updated Excel sheet as well ")

                        else:
                            self.post.ProcessErrorLog(self, 1, f"Sas Case already Created for previous missing Asins for matched historical data")

                    if gsheet_Last_Row['Time Missing Sas']  and not gsheet_Last_Row['Missing_case_notified_users']:
                        cellsASIN = []
                        _Last_SAS_Date = datetime.strptime(gsheet_Last_Row['Time Missing Sas'], '%Y-%m-%d %H:%M')   
                        self.post.ProcessErrorLog(self, 1, f"Matched keys Missing asins time increased, will inform user") 
                        current_datetime = datetime.now()
                        time_difference = current_datetime - _Last_SAS_Date
                        threshold_inform_user = timedelta(hours=self.threshold_inform_user_time)
                        if time_difference > threshold_inform_user  :
                            subject = 'Missing asins with Matched Historical Data__' + datetime.today().strftime('%Y-%m-%d %H:%M')
                           
                            
                            body = f"""
Hi,

For Brand {self.VL_Name}'s -  Missing ASINS still exists after creating SAS\n

Inactive keys found: { ' '.join(list(matched_keys[0].keys()))  }  
Mapped to child ASIN: { ' '.join(list(matched_keys[0].values())) }

Please modify accordingly.

Thanks
                            """
                            
                            inactive_user_column = self.gsheetData_job_log.columns.get_loc('Missing_case_notified_users')  + 1
                            self.inform_users_via_mail(subject, body)
                            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0]   +1 , col = inactive_user_column, value =  "notified user_"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                            self.gsheet_job_log_Update.update_cells(cellsASIN) 
                            print('Email sent for missing asins with matched historical data ')
                            self.post.ProcessErrorLog(self, 1, f"Email sent for missing asins with matched historical data") 


                    # return True
                
                except Exception as e:
                    self.post.ProcessErrorLog(self, 2, f"  Issue in Matched Keys data {e} ")
                    self._ManualLog = 'Error in Matched Keys'
            
            if unmatched_keys:
                
                try:

                    unmatch_time_column = 'Time Upload file Unmatched KEYS'
                    unmatch_column_name = 'VL Delete Status Unmatched Keys'
                    print("\n Going for Un-matched Cases of Historical data missing asins ") 
                    self.post.ProcessErrorLog(self, 1, "Going for Un-matched Cases ")   
                    self.post.ProcessErrorLog(self, 1, f"All UnMatched Keys { unmatched_keys } ")

                    
                    filtered_Last_SAS_Date = None
                    filtered_Last_SAS = self.gsheetData_job_log[(self.gsheetData_job_log[unmatch_column_name] != '') ]
                    if len(filtered_Last_SAS)>0:
                        filtered_Last_SAS = filtered_Last_SAS.iloc[-1]
                        if filtered_Last_SAS[unmatch_time_column]:
                            filtered_Last_SAS_Date = datetime.strptime(filtered_Last_SAS[unmatch_time_column], '%Y-%m-%d %H:%M')  
                        else:
                            filtered_Last_SAS_Date = self.gsheetData_job_log[self.gsheetData_job_log[unmatch_time_column] !=''][-1:][unmatch_time_column]
                            filtered_Last_SAS_Date = datetime.strptime(filtered_Last_SAS[unmatch_time_column], '%Y-%m-%d %H:%M')   
                            self.post.ProcessErrorLog(self, 1, f"No latest date found to be converted ") 
                            
                    ### time difference of upload time SAS
                    if filtered_Last_SAS_Date:
                        current_datetime = datetime.now()
                        time_difference = current_datetime - filtered_Last_SAS_Date
                        threshold = timedelta(hours=self.Sas_create_time)
                    
                    
                    filtered_unmatch_Last_ml_status_value_dict = self.gsheetData_job_log[self.gsheetData_job_log[unmatch_column_name] !=''][-1:][unmatch_column_name]
                    if filtered_unmatch_Last_ml_status_value_dict.values:
                        try:
                            filtered_unmatch_Last_ml_status_value_dict = eval(filtered_unmatch_Last_ml_status_value_dict.values.tolist()[0])
                            previous_row_skus = list(filtered_unmatch_Last_ml_status_value_dict.values())[0]
                        except:
                            print(f' Column {unmatch_column_name} not a dictionary  ')
                            self.post.ProcessErrorLog(self, 1, f' Column {unmatch_column_name} not a dictionary where items should "batch_id":["new_items"] in a dict ')
                    else:
                        filtered_unmatch_Last_ml_status_value_dict = {}
                        previous_row_skus = []

                    
                    
                
                    all_new_child_skus = list(set([k for item in unmatched_keys for k,v in item.items()]))
                    check =  all_new_child_skus == previous_row_skus
                    _new_items = list( set( all_new_child_skus )  - set ( previous_row_skus ) )
                    _new_child_skus_to_upload = ''

                    ### entry point
                    if  _new_items and not check :

                        print(f"\n\t~ Proceeing to Add Child ASIN into Main VL, After {self.Sas_create_time} hour Issuing Seller support cases for the same")
                        self.post.ProcessErrorLog(self, 1, f"Proceeding to Add Child ASIN into Main VL, After {self.Sas_create_time} Hour Issuing Seller support cases for the same")
                        # _new_child_skus_to_upload = list(set(list(unmatched_keys[0].values()) ) - set(list(filtered_unmatch_Last_ml_status_value_dict.values())[0]))
                        _new_child_skus_to_upload = _new_items

                        file_path = self.upload_file_missing_asin(parent_sku, type_='Unmatched',  asins_list=_new_child_skus_to_upload)
                        
                        time.sleep(1)

                        if not file_path : 
                            print(f'New SKUs items  {str(_new_items)} not in latest template sheet')
                            self.post.ProcessErrorLog(self, 1, f'New SKUs items {str(_new_items)} not in latest template sheet  ')
                            self._ManualLog = f'Template Issue - UnMatching SKUs {str(_new_items)} not present in Latest Template in {self.VL_Name}  '
                            return False
                        
                        self.post.ProcessErrorLog(self, 2, f"Going to Upload file for Missing asins VL with unmatch historical data   ")
                        
                        batch_id_returned = self.Delete1ASIN2SKU(parent_sku, function_run ='upload' , filepath = file_path )
                        
                        if  batch_id_returned and file_path : 
                            
                            cellsASIN=[]
                            missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(unmatch_column_name)  + 1
                            Time_missing_asin_vl_upload_file_batch_id = self.gsheetData_job_log.columns.get_loc(unmatch_time_column)  + 1
                            time_non_matching_missing_sas = self.gsheetData_job_log.columns.get_loc('Time_Missing_Case_SAS_unmatching')  + 1

                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Time_missing_asin_vl_upload_file_batch_id , value =  datetime.today().strftime('%Y-%m-%d %H:%M')  ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = missing_asin_vl_upload_file_batch_id , value =  str({batch_id_returned: list(set(_new_child_skus_to_upload))  }) ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = time_non_matching_missing_sas , value =  ''  ))

                            print(' Created new entry for Missing asins with their historical data ')
                            self.post.ProcessErrorLog(self, 1, "    Created new entry for Missing asins with their historical data  ")
                            if len(cellsASIN)>0:
                                self.gsheet_job_log_Update.update_cells(cellsASIN) 
                                time.sleep(2)
                        else:
                            print('No batch ID found, no file uploaded' )
                            self.post.ProcessErrorLog(self, 2, f"No batch found, no file uploaded, was about to upload for missing asins with unmatch historical data  ")
                    

                    
                    # gsheet_Last_Row[unmatch_column_name] != '' and time_difference > threshold and  not gsheet_Last_Row['Time_Missing_Case_SAS_unmatching'] :
                    else:
                        ### SEND SAS IMMEDIATELY ASAP
                        if gsheet_Last_Row[unmatch_column_name] != '' and not gsheet_Last_Row["Time_Missing_Case_SAS_unmatching"]:

                            print('initiating SAS case  for unmatch asins successfully');self.post.ProcessErrorLog(self, 1, "initiating SAS case asin  for unmatch asins successfully ")

                            batch_id_returned = gsheet_Last_Row[unmatch_column_name]
                            batch_id_returned = list(eval(batch_id_returned).keys())[0]
                    
                            result = {}
                            for item in unmatched_keys:
                                key, value = next(iter(item.items()))
                                if value in result:
                                    result[value] += (key,)
                                else:
                                    result[value] = (key,)
                            print(result)

                            ''' Create the file sent to SAS '''
                            wb_append = xw.Book(self.file_unmatching_historical_data)
                            sheet = wb_append.sheets['Template - Variations Update']
                            sheet.api.Unprotect() 
                            time.sleep(2)
                            next_row = 13
                            count_of_asins = 0
                            for common_value, child_asin_list in result.items():
                                for child_asin in child_asin_list:
                                    count_of_asins +=1 
                                    sheet.cells(next_row, 2).value = common_value
                                    sheet.cells(next_row, 3).value = child_asin
                                    sheet.cells(next_row, 4).value = parent_sku
                                    sheet.cells(next_row, 5).value = live_parent
                                    sheet.cells(next_row, 6).value = "Size-Scent"
                                    sheet.cells(next_row, 7).value = "Delete SKU from Variation Listing"
                                    sheet.cells(next_row, 10).value = "Yes"
                                    next_row += 1
                            file_path_SAS = f"{self.Saved_Missing_variation_path}_{self.VL_Name}Unmatched_asins_SAS_file_{live_parent}__{self.today.strftime('%Y-%m-%d')}.xlsx"
                            wb_append.save(file_path_SAS)
                            wb_append.app.quit()
                            print("DONE EDITING EXCEL FILE  for Missing asins unmatched Keys  \n") 
                            self.post.ProcessErrorLog(self, 1, f"DONE EDITING EXCEL FILE  for Missing asins unmatched Keys  ")
                            time.sleep(1)

                        
                            print(f"\nRunning SAS operations as time exceeded for more than {self.Sas_create_time}  hour . ")
                            self.post.ProcessErrorLog(self, 1, f" Running SAS operations as time exceeded for more than  {self.Sas_create_time} hour ")
                            print('For UN-MATCHING Historical data Missing asins\n')
                            subject = f"Child ASINs Can't Add into VL for Parent ASIN {live_parent}__{self.today.strftime('%Y-%m-%d')}"
                            ## need the child asins
                            case_ID_generated = self.seller_support_case(  live_parent , subject ,all_child_asins = list(set([v for i in unmatched_keys for v in i.values()])) ,
                                        missing_asins_text='Missing ASIN', Child_ASINs=' '.join(list(set([v for i in unmatched_keys for v in i.values()]))) , 
                                        count_of_asins=count_of_asins, batch_id= batch_id_returned
                                        )

                
                            sku_line = f"partial update to add {count_of_asins} ASINs via uploading flat file, successful but not reflect on live site, batch id: {batch_id_returned}"
                            headline = f"{count_of_asins} Child ASINs Can't Add into Parent ASIN {live_parent}"
                            self._Missing_case_SAS_IO_UnMatching = self.SAS_issue_assistance(live_parent, case_ID_generated, subject, 
                                                                mail_type="Email" , file_path = file_path_SAS, sku_line = sku_line,
                                                                parent_sku = parent_sku, 
                                                                missing_asins_text="INACTIVE ASINS", headline = headline, count_ = count_of_asins,
                                                                batch_id= batch_id_returned
                                                                )
                            self._Missing_case_SAS_IA_UnMatching = self.SAS_issue_assistance(live_parent, case_ID_generated, subject, 
                                                                mail_type="HTML", file_path = file_path_SAS, sku_line = sku_line, 
                                                                parent_sku = parent_sku ,
                                                                missing_asins_text="INACTIVE ASINS",headline = headline,
                                                                batch_id= batch_id_returned
                                                                )

                            print( 'SUBJECTS ~ \n')
                            print(  self._Missing_case_SAS_IO_UnMatching )
                            print(  self._Missing_case_SAS_IA_UnMatching )
                            print("Created Seller Support Cases for Missing Asins for unmatching  ASINS \n")
                            self.post.ProcessErrorLog(self, 1, f"Created Seller Support Cases for Missing Asins for unmatching  ASINS")
                                    

                            
                            ## updated the column for sas cases
                            cellsASIN=[]
                            time_case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('Time_Missing_Case_SAS_unmatching')  + 1
                            case_ID_generated_column = self.gsheetData_job_log.columns.get_loc('Missing_Case_Seller_support_unmatching')  + 1                        
                            Missing_case_SAS_IO_UnMatching_column = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IO_UnMatching')  + 1                        
                            Missing_case_SAS_IA_UnMatching_column = self.gsheetData_job_log.columns.get_loc('Missing_case_SAS_IA_UnMatching')  + 1
                            
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = time_case_ID_generated_column      , value =  datetime.today().strftime('%Y-%m-%d %H:%M') ))     
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = case_ID_generated_column            , value =  case_ID_generated      ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Missing_case_SAS_IO_UnMatching_column , value =  self._Missing_case_SAS_IO_UnMatching    ))
                            cellsASIN.append(Cell(row = gsheet_Last_index + 2, col = Missing_case_SAS_IA_UnMatching_column , value =  self._Missing_case_SAS_IA_UnMatching    ))
                            print('Case file missing unmatch file Uploaded  successfully')
                            self.post.ProcessErrorLog(self, 1, "Case file missing unmatch asin successfully ")                        
                            self.gsheet_job_log_Update.update_cells(cellsASIN) 

                        else:
                            self.post.ProcessErrorLog(self, 1, f"Sas Case already Created for previous missing Asins with unmatch historical data")

                    if gsheet_Last_Row['Time_Missing_Case_SAS_unmatching'] and not gsheet_Last_Row['Unmatching_case_informed_User'] :
                        cellsASIN = []
                        _Last_SAS_Date = datetime.strptime(gsheet_Last_Row['Time_Missing_Case_SAS_unmatching'], '%Y-%m-%d %H:%M')   
                        self.post.ProcessErrorLog(self, 1, f"UnMatched keys Missing asins time increased, will inform user") 
                        current_datetime = datetime.now()
                        time_difference = current_datetime - _Last_SAS_Date
                        threshold_inform_user = timedelta(hours=self.threshold_inform_user_time)
                        if time_difference > threshold_inform_user  :
                            subject = 'Missing asins with UnMatched Historical Data' + datetime.today().strftime('%Y-%m-%d %H:%M')
                            
                            
                            body = f"""
Hi,

For Brand {self.VL_Name}'s - Unmatched Missing ASINS still exists after creating SAS\n

Inactive keys found: { ' '.join(list(unmatched_keys[0].keys()))  }  
Mapped to child ASIN: { ' '.join(list(unmatched_keys[0].values())) }

Please modify accordingly.

Thanks
                            """
                            
                            inactive_user_column = self.gsheetData_job_log.columns.get_loc('Unmatching_case_informed_User')  + 1
                            self.inform_users_via_mail(subject, body)
                            cellsASIN.append(Cell(row = self.gsheetData_job_log.shape[0] + 1, col = inactive_user_column, value =  "notified user_"+ datetime.today().strftime('%Y-%m-%d %H:%M')     ))
                            self.gsheet_job_log_Update.update_cells(cellsASIN) 
                            print('Email sent for missing asins with Unmatched historical data ')
                            self.post.ProcessErrorLog(self, 1, f"Email sent for missing asins with Unmatched historical data") 

                except Exception as e:
                    self.post.ProcessErrorLog(self, 2, f"  Issue in UnMatched Keys data {e} ")
                    self._ManualLog = 'Error in Unmatched Keys'

            print("Done with Historical Data")
            self.post.ProcessErrorLog(self, 1, f"Done with Historical Data")

        except Exception as e:
            self.post.ProcessErrorLog(self, 2, f"  Missing asins Historical data - get_historical_data ~ exception {e} ")

    def CreateSKUList(self):
        """ 
            Delete extra skus manually 
            Get the latest updated data for all missing and extra asin
        
        """
        combined_asins = self.ExtraASINs + self.MissingASINs
        try:

            for _ASIN in combined_asins :   
                 
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.get( self.CountryURL(self.CountryID, 2))
                time.sleep(3)
                form = self.driver.find_element(by = By.ID,value='myitable-search-form')
                inputbox = form.find_element(by = By.NAME,value='search')
                time.sleep(3)
                inputbox.send_keys(_ASIN)
                time.sleep(2)
                searchbtn = form.find_element(by = By.CLASS_NAME,value='a-button-inner')
                searchbtn.click()
                time.sleep(5)
                checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                time.sleep(1)
                self.driver.execute_script("document.body.style.zoom='70%'")
                #if len(checkbundle) > 0 and checkbundle[0].text != 'You currently have no listings that meet this criteria. Use the filters below the search bar to view more of your listings.' :
                if not checkbundle[0].text.startswith('You currently have no listings'): 
                    fnsku = checkbundle[0].find_elements(by = By.XPATH, value='//*[@data-column="fnsku"]')
                    upcOrEan = checkbundle[0].find_elements(by = By.XPATH, value='//*[@data-column="upcOrEan"]')
                    # boxprice_ele = checkbundle[0].find_elements(by = By.CLASS_NAME,value='mt-input-text')
                    sku = checkbundle[0].find_elements(by = By.XPATH, value='//*[@data-column="sku"]')
                    if checkbundle[0].text.lower().count('no listing') > 0:
                        print(_ASIN, 'No ASIN Found')                
                    else:

                        mtrowlis =  self.driver.find_elements(by = By.CLASS_NAME, value="mt-row")
                        for mtrow in  mtrowlis:  
                            try:
                                id = mtrow.get_attribute('id') 
                                sku = mtrow.find_element(by = By.ID, value=id + '-sku')
                                sku= sku.text.replace('\nNew','')
                                fnsku = mtrow.find_element(by = By.ID, value=id + '-fnsku')
                                fnsku = fnsku.text
                                upcOrEan = mtrow.find_element(by = By.ID, value=id + '-upcOrEan')
                                upcOrEan = upcOrEan.text
                                price = mtrow.find_element(by = By.ID, value=id + '-price-price')
                                price = price.find_element(by = By.TAG_NAME, value='input')    
                                price = price.get_attribute('value').replace('$','')
                                print(_ASIN, fnsku, sku, upcOrEan, price)
                                self.UpdteSKUInDB(_ASIN, fnsku, sku, upcOrEan, price, self.CountryID)
                                time.sleep(1)
                                self._ManualLog = 'Created SKU List'
                            except: 
                                self.post.ProcessErrorLog(self, 1, f'SKU -  {sku} incomplete details  ...  ');print(f'SKU  - {sku} incomplete details  ... ')
                        
                        time.sleep(2)
                        if _ASIN in self.MissingASINs :
                            self._ManualLog = ''
                            continue

                        if len(mtrowlis)>0 :
                            self.DeleteASINs.append(_ASIN)


                            # # # delete code
                            radbtn = self.driver.find_element(by = By.ID,value='mt-select-all')
                            actions = ActionChains(self.driver)
                            actions.move_to_element(radbtn).perform()
                            radbtn.send_keys( Keys.SPACE )
                            time.sleep(3)
                            
                            
                            self.driver.execute_script("window.scrollTo(0,0)")
                            time.sleep(2)   

                            droplst = self.driver.find_element(by = By.CLASS_NAME,value='a-button-dropdown')
                            actions = ActionChains(self.driver)
                            actions.move_to_element(droplst).perform()
                            # droplst.click()

                            self.driver.execute_script('document.querySelector("#myitable > div.mt-header.clearfix > div.mt-header-bulk-action > span > span > select").click()')

                            
                            time.sleep(2)
                            dlst = self.driver.find_element(by = By.CLASS_NAME,value='a-dropdown-common')
                            if dlst.text.count('Delete products and listings') > 0:
                                droplst = self.driver.find_elements(by = By.CLASS_NAME,value='a-dropdown-item')
                                for num in range(len(droplst)):
                                    if droplst[num].text == 'Delete products and listings':
                                        actions = ActionChains(self.driver)
                                        actions.move_to_element(droplst[num]).perform()
                                        
                                        link =  droplst[num].find_element(by = By.TAG_NAME,value='a')
                              
                                        link = link.get_attribute('ID')
                                        link = 'document.querySelector("#'+ link +'").click()' 
                                        self.driver.execute_script(link)
                                        

                                        self.post.ProcessErrorLog(self, 1, "Deleted ASIN " + _ASIN )
                                        time.sleep(4)
                                        Alert(self.driver).accept()
                                        time.sleep(2)
                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                        time.sleep(2)
                                        sucess_message = self.driver.find_elements(by = By.CLASS_NAME,value='a-alert-success')
                                        if len(sucess_message)>0 and sucess_message[0].text.lower() == 'Your change is being processed. It may take up to 15 minutes to take effect.'.lower():
                                            print('Asin Removed 15')
                                            break
                                        conformation_message = self.driver.find_elements(by = By.ID,value='interStitialPageMessage')
                                        continue_btn = self.driver.find_elements(by = By.ID,value='interstitialPageContinue')
                                        if len(conformation_message) > 0 and len(continue_btn) > 0 :
                                            print('Asin Removed confirmation ')
                                            continue_btn[0].click()
                                        time.sleep(3)
                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                        time.sleep(2)
                                        sucess_message = self.driver.find_elements(by = By.CLASS_NAME,value='a-alert-success')
                                        if sucess_message[0].text.lower() == 'Thanks for suggesting changes to the catalogue. Note: Amazon considers inputs from multiple sources before changing the detail pages for our customers. Your recommendation is currently being reviewed. If we accept your recommendations, the changes will be reflected within 24 hours.'.lower() :
                                            print('Asin Removed 24')
                                        break

                        time.sleep(2)
                else:  print( f'ASIN {_ASIN} not Found in child sku list') ; self.post.ProcessErrorLog(self, 1, f'ASIN {_ASIN} not Found in child sku list')
            return True        
        
        except Exception as err:  
            print("Error in method CreateSKUList :",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Error in method CreateSKUList " + str(err))
            self._ManualLog = 'Error in Creating SKU List - CreateSKUList  - '+ str(err)
            return False      
    
    def DownloadTemplateType(self,country_list):
        try:
            
            if len(self.DeleteASINs)==0:
                self._ManualLog =='Not in Catalog'
                return False   

            self._ManualLog ='File Not Download'
            self.driver.switch_to.window(self.driver.window_handles[0])            
            filtergsheetData = self.gsheetData[self.gsheetData['Parent for System Verification'] ==  self._ParentASIN ] 
            #filtergsheetData = self.gsheetData[self.gsheetData['List of Extra ASINs'] !=  '' ]            
            filtergsheetData = filtergsheetData.replace({np.nan: None})
            filtergsheetData = filtergsheetData.head(1)
            filterBrsheet = self.Brsheet[(self.Brsheet['Country'] == self.CountryID) & (self.Brsheet['ASIN'] ==  self.DeleteASINs[0] )]

            def select_node_keywords(node_keyword):
                selected = [i.strip() for i in node_keyword if  i ] 
                Fullnode = selected
                Fullnode[-1] = Fullnode[-1] + '\nSelect'       
                ele=''  
                for nd in Fullnode:
                    f = self.driver.find_elements(by=By.TAG_NAME, value='browse-node-component')
                    for i in f:
                        if i.text == nd:
                            print(i.text, nd, i.text == nd )
                            actions = ActionChains(self.driver)
                            actions.move_to_element(i).perform()
                            i.click()
                            ele = i
                            time.sleep(3)
                            break
                time.sleep(3)
                return ele
        
            for _indices,_row in filtergsheetData.iterrows():
                if len(filterBrsheet) == 0:
                    self._ManualLog = 'ASIN not avaliable in category node gsheet for' + country_list                  
                    return False
                node_keyword = list(filterBrsheet['File NodePath'])[0]
                node_keyword  = node_keyword.split('›')
                print('Node Keyword', node_keyword);self.post.ProcessErrorLog(self, 1, f' node_keyword {node_keyword} ')

                if node_keyword == '':
                    self._ManualLog = 'Node path empty for ' + country_list                    
                    return False
                
                for cntry in country_list:
                    
                    url =  self.CountryURL(self.CountryID, 1) 
                    self.driver.get(url)
                    time.sleep(3)
                    searchbox = self.driver.find_element(by=By.ID,value = "search-box")

                    remove_all = self.driver.find_elements(By.LINK_TEXT, "Remove All")
                    if len(remove_all)>0:
                        remove_all[0].click()   

                    time.sleep(1)
                    self.driver.find_element(By.CLASS_NAME,"a-button-search").click()
                    time.sleep(3)
                    
                    ele = ''  
                    ele = select_node_keywords(node_keyword)

                    result_untick_countries= self.untick_all_countries()
                    if not result_untick_countries:
                        self.post.ProcessErrorLog(self, 2, f" Issue in unticking countries ")
                        self._ManualLog = 'Issue in unticking countries while downloading latest template from amazon portal'
                        return False
                    
                    time.sleep(3)
                    if ele != '' :
                        select_btn = ele.find_elements(by=By.CLASS_NAME, value='select-button-ungated')
                        if len(select_btn)>0 and select_btn[0].text.strip()=='Select':
                            select_btn[0].click()
                            time.sleep(10)
                            self.driver.find_element(By.ID, "custom-template-button").click()
                            self._ManualLog ='File Downloaded'
                    else:
                        self._ManualLog = 'Node not Found in list'
                    print('Self of manual log = ',self._ManualLog)
                    self.post.ProcessErrorLog(self, 1, str(self._ManualLog) + ' about to move the file')
                    
                    DownloadSpreadsheet = self.driver.find_elements(By.CLASS_NAME, "node-column")
                    for nodes in range(len(DownloadSpreadsheet)):
                        web_node = DownloadSpreadsheet[nodes].text.split('\n')[1].replace('>','').replace(' ','')
                        if web_node == list(filterBrsheet['File NodePath'])[0].replace('›','').replace(' ',''):
                            select_btn = self.driver.find_elements(by = By.XPATH, value='//*[@type="submit"]')
                            select_btn[1+nodes].click()
                            break
                    
                    #----------------------------------------------------------------------------------
                    #Selecting Second last Node from category node
                    # remove_all = self.driver.find_elements(By.LINK_TEXT, "Remove All")
                    # if len(remove_all)==0:
                    #     node_keyword2 = list(filterBrsheet['File NodePath'])[0].split('›')[-2]

                    #     searchbox = self.driver.find_element(by=By.ID,value = "search-box")
                    #     searchbox.clear()
                    #     time.sleep(1)
                    #     searchbox.send_keys(node_keyword2)
                    #     # ele=''  
                    #     # ele = select_node_keywords(node_keyword2)

                    #     time.sleep(1)
                    #     self.driver.find_element(By.CLASS_NAME,"a-button-search").click()
                    #     time.sleep(3)
                    #     DownloadSpreadsheet = self.driver.find_elements(By.CLASS_NAME, "node-column")
                    #     for nodes in range(len(DownloadSpreadsheet)):

                    #         web_node = DownloadSpreadsheet[nodes].text.split('\n')[1].replace('>','').replace(' ','')
                    #         if web_node == list(filterBrsheet['File NodePath'])[0].replace('›','').replace(' ',''):
                    #             select_btn = self.driver.find_elements(by = By.XPATH, value='//*[@type="submit"]')
                    #             select_btn[1+nodes].click()
                    #             break
                    #----------------------------------------------------------------------------------



                    print('Going to move file from download to template directory, wait 10 sec')
                    self.post.ProcessErrorLog(self, 1, f' Going to move file from download to template directory, wait 10 sec ')
                    # if cntry != 'SG':
                    #     self.CountrySelection(cntry)
                    time.sleep(10)
                    #Delete Node file if exist
                    filename = self.driver.find_element(By.ID, 'classifications-table').find_elements(By.CLASS_NAME,'ng-binding')[1].text
                    filename = filename.replace(' ','_')
                    # fileList = os.listdir(self.DownloadLocation)
                    # for file in fileList:
                    #     if filename in file and '.xlsm' in file:                            
                    #         os.remove(self.DownloadLocation +  file)
                    # download template button again
                    # self.driver.find_element(By.ID, "custom-template-button").click()
                    time.sleep(3)
                    #Move download file to DG Folder 
                    fileList = os.listdir(self.DownloadLocation)
                    for file in fileList:
                        if filename in file and '.xlsm' in file:                                                        
                            shutil.move(os.path.join(self.DownloadLocation, file) , os.path.join(self.SFTPLocation, file.replace(filename,self._ParentASIN +'_'+self.VL_Name+ '_' + filename + '_' + cntry + '__' + self.today.strftime('%Y-%m-%d') ))  )
                            self.post.ProcessErrorLog(self, 1, f' File moved to directory  ');print(f'File moved to directory    ')
                            self._ManualLog ='File Downloaded'
                            break      
            
            if self._ManualLog =='File Not Download':
                return False    
            
            return  True
        except Exception as err:  
            print("Error File Downloaded ",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Error File Downloaded " + str(err))
            self._ManualLog ='Error File Downloaded'
            return False
       
    def CreateTemplateForUploadType(self, country_list):

        try:
            self._ManualLog ='File Not Download'
            asin_sku=[] 

            for _ASIN in self.DeleteASINs:             
                para = {    
                        "data" : {"userid":2, "ASIN":_ASIN, "CountryID": self.CountryID , "table": "Product_Master_Details_ByASINAll" },
                        "type":"Select"
                    }
                post = PostFun() 
                skujson = post.PostApiParaJson(para)
                countryKey  ='' 
                for val in skujson['data']['input']:
                    if val['GroupName'] !='Info':
                        for valupdate in val['data']:                         
                            if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                asin_sku.append(valupdate['data']['updatedvalue'])
                                    

            for cntry in country_list:
                for file_name in os.listdir(self.SFTPLocation):
                    #cn = file_name.split('_')[2]
                    if self._ParentASIN in file_name and '.xlsm' in file_name and cntry in file_name   and self.today.strftime('%Y-%m-%d') in file_name :
                        file_path = os.path.join(self.SFTPLocation, file_name)
                        wb = xw.Book(file_path)
                        ws = wb.sheets["Template"]  
                        #Unhide row and column
                        column_range = ws.range('A2:ZZ2')
                        column_range.column_width = 12
                        row_range = ws.range('3:10000')
                        row_range.row_height = 15
                        
                        #Extracting and writing product key                            
                        wt = wb.sheets["Dropdown Lists"]
                        prod_type = wt["A4"].value
                        for hdr in ws.range('A3:ZZ3'):
                            if hdr.value =='' or hdr.value == None :
                                break
                            #print(hdr.address.split('$')[1])
                            celladdress = hdr.address.split('$')[1]
                            #feed_product_type insert
                            if hdr.value == 'feed_product_type':
                                for i in range(len(asin_sku)):
                                    ws.range(celladdress + str(4+i)).value = prod_type
                                    i = 1+ i
                            #SKU insert
                            elif hdr.value == 'item_sku':
                                for i in range(len(asin_sku)):
                                    ws.range(celladdress + str(4+i)).value = asin_sku[i]
                                    i = 1+ i
                            #update_delete insert
                            elif hdr.value == 'update_delete':
                                for i in range(len(asin_sku)):
                                    ws.range(celladdress + str(4+i)).value = 'Delete'
                            
                        wb.save()
                        wb.app.quit()    
                        self._ManualLog = 'File Update'                        
                        break

            if self._ManualLog =='File Not Download':
                return False                        
            
            return True                    
        except Exception as err:  
            print("Error CreateTemplateForUploadType :",str(err)) 
            self.post.ProcessErrorLog(self, 2, "Error CreateTemplateForUploadType " + str(err))
            self._ManualLog = 'Error Create Template For Upload Type'
            return False
  
    def UploadVLFileType(self, country_list):
        
        try:

            if len(self.DeleteASINs)==0:
                self._ManualLog =='Not in Catalog'
                return False   

            self._ManualLog = 'File about to upload '

            filtergsheetData = self.gsheetData[self.gsheetData['Parent for System Verification'] ==  self._ParentASIN ]            
            filtergsheetData = filtergsheetData.replace({np.nan: None})
            filtergsheetData  = filtergsheetData.head(1)
            
            for ind,rw in filtergsheetData.iterrows():
                for cntry in country_list:                
                    for FileName in os.listdir(self.SFTPLocation):
                        if rw['Parent for System Verification'] in FileName and '.xlsm' in FileName and cntry in FileName and self.today.strftime('%Y-%m-%d') in FileName:
                            try:
                                current_row = self.gsheetData_job_log.index[-1] 
                                gsheetLog =  self.gsheetData_job_log.iloc[-1] 
                            
                                if not gsheetLog['Extra Upload'] == 'Upload':
                                    time.sleep(2)
                                    self.driver.get(self.CountryURL(self.CountryID,3))
                                    time.sleep(5)
                                    _file = self.SFTPLocation + FileName
                                    elems = self.driver.find_element( By.ID, value= 'file-upload-input')
                                    self.driver.execute_script("arguments[0].style.display = 'block';", elems)
                                    time.sleep(1)            
                                    elems.send_keys( _file )
                                    time.sleep(2)            
                                    self.driver.execute_script("arguments[0].style.display = 'none';", elems)
                                    time.sleep(1)    
                                    self.post.ProcessErrorLog(self, 1, f" file {_file} uploaded successfully ")  

                                    popup_submit = self.driver.find_elements(by= By.XPATH,value= '//*[@label="Submit products"]')
                                    time.sleep(5)
                                    if len(popup_submit)>0:
                                        popup_submit[0].click()
                                    time.sleep(10)
                                    self.post.ProcessErrorLog(self, 1, "dialog file selected")
                                    self._ManualLog = 'Template Uploaded Status Pending'
                                    self.VLStatus(FileName)
                                    self._ManualLog == ''

                                    cellsASIN=[]
                                    Extra_Upload = self.gsheetData_job_log.columns.get_loc('Extra Upload')  + 1
                                    current_row = self.gsheetData_job_log.index[-1]

                                    Time_Extra_Upload = self.gsheetData_job_log.columns.get_loc('Time Extra Delete Upload')  + 1
                                    cellsASIN.append(Cell(row = current_row + 2 , col = Extra_Upload, value =  "Upload" ))
                                    cellsASIN.append(Cell(row = current_row + 2 , col = Time_Extra_Upload, value =  datetime.now().strftime('%Y-%m-%d %H:%M') ))                  
                                    
                                    self.gsheet_job_log_Update.update_cells(cellsASIN) 

                                else:
                                    self.post.ProcessErrorLog(self, 1, f'Extra ASINs file already uploaded successfully ');print(f'Extra ASINs file already uploaded successfully  ')

                                return True  
                            except Exception as e:
                                print('dialog_window_title not open ',e)
                                self.post.ProcessErrorLog(self, 2, f"dialog_window_title not open Error: {e}") 
                                return False           
        
            if self._ManualLog == 'File Not Download':
                return False   
        
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error Template Upload " + str(err)) 
            self._ManualLog = 'Error Template Upload'
            return False 

    def Delete1ASIN2SKU(self , sku, country_list =['US'], 
                        function_run = None, 
                        filepath = None ):
        
        """
            - Delete old Asin SKU  Manually from Variation Listing Page
            - Upload the Existing VL or New VL file and get the batch ID
            - _parentsku > pass in sku or name, it will be worth it
        """

        try:

            uploadfilelist    = [filepath]
            _parentsku =   sku

            
            def delete_vl_sku_manual():

                """
                        Manual VL SKU Delete  from manage inventory
                """
                
                child_asin_skus=[]
                for child_asin in self.MissingASINs: 
                    para = {    
                        "data" : {"userid":2, "ASIN": child_asin, "CountryID": self.CountryID,"table": "Product_Master_Details_ByASINAll" },
                        "type":"Select"
                    }
                    post = PostFun() 
                    skujson = post.PostApiParaJson(para)
                    for val in skujson['data']['input']:
                        if val['GroupName'] !='Info':
                            for valupdate in val['data']:                         
                                if valupdate['TitleName']=='SKU' and valupdate['data']['updatedvalue']!='':  
                                    child_asin_skus.append(valupdate['data']['updatedvalue'])
                

                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.get( self.CountryURL(self.CountryID, 2))
                time.sleep(3)
                form = self.driver.find_element(by = By.ID,value='myitable-search-form')
                inputbox = form.find_element(by = By.NAME,value='search')
                time.sleep(3)
                inputbox.send_keys(_parentsku)
                time.sleep(2)
                searchbtn = form.find_element(by = By.CLASS_NAME,value='a-button-inner')
                searchbtn.click()
                time.sleep(5)
                checkbundle = self.driver.find_elements(by = By.CLASS_NAME,value='mt-row')
                time.sleep(1)
                self.driver.execute_script("document.body.style.zoom='70%'")
                self.post.ProcessErrorLog(self, 1, "About to delete manually Variation VL")
                if not checkbundle[0].text.startswith('You currently have no listings'): 
                    self.post.ProcessErrorLog(self, 1, f"Found the VL SKU- {_parentsku} ")
                    # # # delete sku code
                    radbtn = self.driver.find_element(by = By.ID,value='mt-select-all')
                    actions = ActionChains(self.driver)
                    actions.move_to_element(radbtn).perform()
                    radbtn.send_keys( Keys.SPACE )
                    time.sleep(3)
                    
                    
                    self.driver.execute_script("window.scrollTo(0,0)")
                    time.sleep(2)   

                    droplst = self.driver.find_element(by = By.CLASS_NAME,value='a-button-dropdown')
                    actions = ActionChains(self.driver)
                    actions.move_to_element(droplst).perform()
                    # droplst.click()

                    self.driver.execute_script('document.querySelector("#myitable > div.mt-header.clearfix > div.mt-header-bulk-action > span > span > select").click()')

                    
                    time.sleep(2)
                    dlst = self.driver.find_element(by = By.CLASS_NAME,value='a-dropdown-common')
                    if dlst.text.count('Delete products and listings') > 0:
                        droplst = self.driver.find_elements(by = By.CLASS_NAME,value='a-dropdown-item')
                        for num in range(len(droplst)):
                            if droplst[num].text == 'Delete products and listings':
                                actions = ActionChains(self.driver)
                                actions.move_to_element(droplst[num]).perform()
                                
                                link =  droplst[num].find_element(by = By.TAG_NAME,value='a')
                        
                                link = link.get_attribute('ID')
                                link = 'document.querySelector("#'+ link +'").click()' 
                                self.driver.execute_script(link)
                                

                                self.post.ProcessErrorLog(self, 1, "Deleted parent SKU " + _parentsku )
                                time.sleep(4)
                                Alert(self.driver).accept()
                                time.sleep(2)
                                self.driver.switch_to.window(self.driver.window_handles[0])
                                time.sleep(2)
                                sucess_message = self.driver.find_elements(by = By.CLASS_NAME,value='a-alert-success')
                                if len(sucess_message)>0 and sucess_message[0].text.lower() == 'Your change is being processed. It may take up to 15 minutes to take effect.'.lower():
                                    print('Asin Removed 15')
                                    break
                                conformation_message = self.driver.find_elements(by = By.ID,value='interStitialPageMessage')
                                continue_btn = self.driver.find_elements(by = By.ID,value='interstitialPageContinue')
                                if len(conformation_message) > 0 and len(continue_btn) > 0 :
                                    print('Asin Removed confirmation ')
                                    continue_btn[0].click()
                                time.sleep(3)
                                self.driver.switch_to.window(self.driver.window_handles[0])
                                time.sleep(2)
                                sucess_message = self.driver.find_elements(by = By.CLASS_NAME,value='a-alert-success')
                                if sucess_message[0].text.lower() == 'Thanks for suggesting changes to the catalogue. Note: Amazon considers inputs from multiple sources before changing the detail pages for our customers. Your recommendation is currently being reviewed. If we accept your recommendations, the changes will be reflected within 24 hours.'.lower() :
                                    print('Asin Removed 24')
                                break
                    
                else:
                    print('Old VL Already deleted manually')
                    self.post.ProcessErrorLog(self, 1, "Old VL Already deleted manually " ) 
                    return ('Old VL Already deleted manually')

            def upload_vl_file():
                """
                Upload the file 
                
                """
               
                for file in uploadfilelist:   
                                         
                        filename = file.split('\\')[-1].split('.')[0]
                        print('File That will be uploaded:\t', file)
                        time.sleep(2)
                        self.driver.get(self.CountryURL(self.CountryID,3))
                        time.sleep(5)
                        
                        elems = self.driver.find_element( By.ID, value= 'file-upload-input')
                        self.driver.execute_script("arguments[0].style.display = 'block';", elems)
                        time.sleep(1)            
                        elems.send_keys( file )
                        time.sleep(2)            
                        self.driver.execute_script("arguments[0].style.display = 'none';", elems)  
                        self.post.ProcessErrorLog(self, 1, f" file {file} uploaded successfully ")
                        time.sleep(15)
                        try:
                            try:
                                popup_submit = self.driver.find_elements(by= By.XPATH,value= '//*[@label="Submit products"]')
                                time.sleep(5)
                                if len(popup_submit)>0:
                                    popup_submit[0].click()
                            except: self.driver.find_elements(By.ID,'submit-feed-button')[0].click()
                            time.sleep(5)
                            self.post.ProcessErrorLog(self, 1, "dialog file selected")
                            self._ManualLog = 'Template Uploaded Status Uploaded'
                        except:
                            
                            btn = 'document.querySelector("#submit-feed-button").shadowRoot.querySelector("button > div.content > slot > span").click()'
                            self.driver.execute_script(btn)
                            time.sleep(10)
                            self.post.ProcessErrorLog(self, 1, "dialog file selected")
                            self._ManualLog = 'Template Uploaded Status Pending'
                         
                                                
                        pageStatus = False
                        percentage = 0
                        icount = 0
                        element_text = ''
                        result = None
                        while pageStatus == False  :                             
                            if icount >= 10 :
                                pageStatus = True
                            print(0)
                            try:
                                time.sleep(40)   
                                icount += 1
                                self.driver.get(self.CountryURL(self.CountryID,4))
                                time.sleep(10)
                                print(1)
                                keylist =  self.driver.find_elements (by= By.XPATH,value= '//*[@id="submission-status-table"]/table/tbody/tr')                            
                                for rowkey in keylist:
                                    keylist =  self.driver.find_elements (by= By.XPATH,value= '//*[@id="submission-status-table"]/table/tbody/tr')
                                    td = rowkey.find_elements(By.TAG_NAME, "td")                     
                                    if len(td)> 0:  
                                        if filename in td[0].text  or filename.startswith(td[0].text):
                                            
                                            print(2, ' FILE FOUND IN ROW:: \ttd text: ', td[0].text, '\tfilename:',filename, '\n\n')
                                            self._ManualLog = td[4].text
                                            if 'Done' in td[3].get_attribute('innerHTML') :                            
                                                print('Status Shown is done')
                                                self.post.ProcessErrorLog(self, 1, "Upload Status Done") 
                                            print("Batch id\t:",self._ManualLog)
                                            if 'In Progress' in td[3].get_attribute('innerHTML') : 
                                                self.post.ProcessErrorLog(self, 1, f'File In progress  ');print(f'File In progress   ')
                                                time.sleep(10)
                                                continue  
                                            print('td 2 text',td[2].text )
                                            element_text = td[2].text
                                            if element_text == 'N/A':
                                                print("Can't depict percentage status yet, N/A shown, wait ..")
                                                self.post.ProcessErrorLog(self, 1, "Can't depict percentage status yet, N/A shown, wait ...")
                                                time.sleep(10)
                                                continue
                                            parts = element_text.split('/')
                                            percentage = (int(parts[0].strip()) / int(parts[1].strip())) * 100
                                            result = percentage >=60
                                            if result:
                                                pageStatus = True
                                                break
                                            print( 'Current percentage Score\t', (int(parts[0].strip())) ,'/' , (int(parts[1].strip())) , ' current icount', icount, '\n')
                                            print(f'Current percentage = ', percentage)
                                            if percentage < 60:
                                                self.post.ProcessErrorLog(self, 1, f'Current percentage Score {parts[0].strip() } / {parts[1].strip()}')
                                                pageStatus = True
                                                break
                                                  
                                        else:
                                            keylist =  self.driver.find_elements (by= By.XPATH,value= '//*[@id="submission-status-table"]/table/tbody/tr')
                                            continue
                            except Exception as e:
                                print(f'Stale Element Exception, re-locating the elements...   ')
                             
                            result = percentage >=60
                            print('RESULT', result, 'Percentage', percentage)
                            self.post.ProcessErrorLog(self, 1, f' result {result} - percentage {percentage} ')
                        
                        if result:
                            self.post.ProcessErrorLog(self, 2, f'Result of file upload status >= 60%  Means File uploaded successfully'  )
                            return self._ManualLog
                        else:
                            print(f'Result of file upload status in percentage as result is not greater than 60%, as current status score is not adequate  ' )
                            self.post.ProcessErrorLog(self, 2, f'Result of file upload status in percentage as result is not greater than 60%, as current status score is not adequate, File upload Failed  '  )
                            return False
                          

            if function_run == "delete":
                self.post.ProcessErrorLog(self, 1, "Delete1ASIN2SKU - running manual delete")
                print('Delete1ASIN2SKU - running manual delete ')
                delete_vl_sku_manual()
            elif function_run == 'upload' and filepath:
                self.post.ProcessErrorLog(self, 1, "Delete1ASIN2SKU - running upload method")
                print('Delete1ASIN2SKU - running upload method ')
                return upload_vl_file()
            elif function_run == 'both':
                self.post.ProcessErrorLog(self, 1, "Delete1ASIN2SKU - running both delete and upload")
                print("Running Both Functions")
                self.post.ProcessErrorLog(self, 1, "Delete1ASIN2SKU - running manual delete first")
                print('Delete1ASIN2SKU - running manual delete ')
                delete_vl_sku_manual()
                print('Delete1ASIN2SKU - running upload delete ')
                self.post.ProcessErrorLog(self, 1, "Delete1ASIN2SKU - running upload delete now")
                return upload_vl_file()
            else:
                print("\nFiles Ready\n")
                 
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error Template Upload " + str(err)) 
            self._ManualLog = 'Error method Delete1ASIN2SKU '
            return False 

    def ProcessStart(self,CountryID, RPAPID, RPAID):
        
        
        try:

            self.RPAID = RPAID
            CloseCount = 2
            CurrentCount = 0
            if RPAID == 10:
                self.VL_Name = 'Gya EOS '
            elif RPAID == 34:
                self.VL_Name = 'Hana '
            elif RPAID == 35:
                self.VL_Name = 'Kukka '
                
            self.CountryID= CountryID
            self.ID = RPAPID
            self.IsComplete =0
            self.PLID =0
            self.Status =0
            self.ProcessLog =''
            self.arr = []   
            self.IDList=[]

            
            file_names = {
                ### Main VL google drive file
                10: 'US- Gya EOS Partial Update Child ASINs in Main VL Template.xlsx', 
                ### Hana google drive file
                34: 'US- Hana EOS All Child ASINs Template -231122.xlsx', 
                ### Kukka google drive file
                35: 'US- Kukka EOS All Child ASINs Template -231122.xlsx'  
            }

            brand_file_name = {
                ### Main VL google drive file
                10: 'Variation Listing - Main VL', 
                ### Hana google drive file
                34: 'Variation Listing - Hana VL', 
                ### Kukka google drive file
                35: 'Variation Listing - Kukka VL'  
                
            }
            

            self.file_name_google_drive = file_names[self.RPAID]

            self._brand_file_name  = brand_file_name[self.RPAID]
            
            # pick up location of all  the files
            self.Missing_variation_path = self.SFTPLocation + self.VL_Name +"Template\\"

            # saved location of all the files 
            self.Saved_Missing_variation_path = self.SFTPLocation

            self.Excel_file_path = self.SFTPLocation +self.VL_Name + "Template\\SAS_TEMPLATE.xlsx" 

            self.SFTPLocation = self.SFTPLocation + self.VL_Name +"Template\\"
            
            ## parent with or without sku file
            self.Parent_without_SKU_file_path = self.Missing_variation_path +"Amazon_Variations_A31LSP1L7F6XJ2_Split from NON-SKU VL- Template.xlsx"
            ## Missing asins active and inActive historical data check file
            self.file_matching_historical_data = self.Missing_variation_path + "Amazon_Variations_A31LSP1L7F6XJ2_Gya Group 107 ASINs in Main VL-Template.xlsx"
            self.file_unmatching_historical_data = self.Missing_variation_path + "Amazon_Variations_A31LSP1L7F6XJ2_Split from NON-SKU VL- Template.xlsx"
            self.VL_upload_file =  self.Missing_variation_path + f'Latest_Template.xlsm'

            print("Amazon Suppressions VL Alert "+ self.VL_Name , str(CountryID), str (RPAPID))  
            if self.ID == 0:
                self.loadASIN()
            else:
                self.gsheetData = self.ReadUpdateGoogleSheet(0)
            
            self.IDList = self.post.ProcessLogGetLast(self)
            #self.IDList =  self.IDList[self.IDList['Process_Name'].isin(['1|B075MBKTTY'])]
            

            while len(self.IDList.loc[self.IDList['Status']==0]) != 0:
                print('Current Count ', str(CurrentCount))            
                if CurrentCount == CloseCount:
                    print('App Close')
                    break
                CurrentCount= CurrentCount + 1
                

                time.sleep(5)
                self.openbrowser()
                self.ImageCaptcha()    
                self.ImageCaptcha()
                time.sleep(5)
                self.filllogin()
                time.sleep(5)
                self.getdatafromamazon()
                time.sleep(5)
                self.signout()
                time.sleep(5)
                self.driver.close()
                self.driver.quit()
                time.sleep(5)
                self.IDList = self.post.ProcessLogGetLast(self)
                time.sleep(30)
            
            if len(self.IDList.loc[self.IDList['Status']==0]) == 0:
                self.sendmessage()
                ...
            else:
                time.sleep(60)


            self.post.ProcessErrorLog(self, 1, "ProcessStart Successfully")
            
        except Exception as err:  
            print(str(err))
            self.post.ProcessErrorLog(self, 2, "ProcessStart " + str(err)) 
           


