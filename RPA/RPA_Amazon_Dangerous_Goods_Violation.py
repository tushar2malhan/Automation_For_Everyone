

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
from selenium.common.exceptions import StaleElementReferenceException
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
from gspread.cell import Cell
import urllib
import base64
import subprocess
import ast


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
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload
import os
import io
import re 
from datetime import datetime, timedelta
import ast
import subprocess

## DB setup

import psycopg2
from psycopg2 import sql
import pandas as pd
from datetime import datetime
import pytz
import sys

from PostFun import PostFun



class RPA_Amazon_Dangerous_Goods_Violation:
    
    def __init__(self):
        
        self.RPAID = 30
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
        self.all_cases_dataset = []
        self.gsheetUpdate= []
        self._ASINProductName = ""
        self._ASIN = ""
        self._ASINNode =  ""
        self._ASINCategory =  ""
        self._NodeError = ""
        self._AutoLog =  ""
        self._ManualLog =  ""
        self.post = PostFun() 
        self.ir = IRFun()
        self.Sas_create_time = 48
        self.SAS_manager_time_period = 7
        self.second_threshold_timeperiod = 24
        self.asins_directory_path = os.path.join(os.getcwd(), "asins")
        self.Lab_Reports_path = self.asins_directory_path + '\\LabReports'
        self.keyword = '100% Pure'
        self.dangerous_good = {}
        self.DownloadLocation = str(os.path.join(Path.home(), "Downloads\\"))
        self.SAS_Manager_Cases = []
        self.missing_lab_reports = []

        self.df_case_ids = None

        self.StartDate = datetime.now()
        self.SAS_REPORT = ''
        self.reopen_case = None
        self.SAS_Manager_asins_list = {}
        
    def __del__(self):
        self.IDList=[]
        self.ID = -1
        del self
        print('Destructor called')       
   
    def convert_date_IST_timezone(self, date):
        ist_timezone = pytz.timezone('Asia/Kolkata')
        date_ist = date.astimezone(ist_timezone)
        return date_ist

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

    def readgooglesheet(self):
        """
            First   step: Read join of master and stage table
            and secondly: Read final all cases table 
        """

        try:

            # self.post.ProcessErrorLog(self, 1, "gsheet Sucessfully loaded")


            para = {
                "data": { "role": 1, "userid": 2, "table": "Report_Abuse"},
                "type": "Select"
            }
            post = PostFun()
            jsondata = self.post.PostApiParaJson(para)
            self.gsheetData = pd.DataFrame(jsondata['data'])

            date_columns = ['Date', 'Check_Date', 'Filing_Activity', 'Lab_Date']
            for column in date_columns:
                self.gsheetData[column] = pd.to_datetime(self.gsheetData[column], unit='ms')
                self.gsheetData[column] = self.gsheetData[column].dt.strftime('%Y-%m-%d %H:%M')

            ### calling final stage table
            self.read_final_stage_table()
            # self.all_cases_dataset
            return self.gsheetData            
        
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "gsheet " + str(err)) 

    def read_final_stage_table(self):
        try:

            para = {
                "data": { "role": 1, "userid": 2, "table": "read_final_stage_all_cases"},
                "type": "Select"
            }
            post = PostFun()
            jsondata = self.post.PostApiParaJson(para)
            self.all_cases_dataset = pd.DataFrame(jsondata['data'])
            
            self.all_cases_dataset["Date"] = pd.to_datetime(self.all_cases_dataset["Date"], unit='ms')
            self.all_cases_dataset["Date"] = self.all_cases_dataset["Date"].dt.strftime('%Y-%m-%d %H:%M')

            return self.all_cases_dataset            
        
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "gsheet " + str(err)) 

    def updategooglesheet(self, flag, _CountryID):
        try:            
            
            if flag == 1:
                googleAPI = 'GoogleCredentials\client_sheet.json'
                scope = ['https://www.googleapis.com/auth/drive']
                credentials = service_account.Credentials.from_service_account_file(googleAPI)
                scopedCreds = credentials.with_scopes(scope)
                gc = gspread.Client(auth=scopedCreds)
                gc.session = AuthorizedSession(scopedCreds)     
                
                
                self.gsheet_job_log_Update = gc.open("Report Abuse System Master").worksheet("RPA Job Log")
                self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
                self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)

                self.post.ProcessErrorLog(self, 1, "gsheet open update Sucessfully")
            else:
                print('Appending row in google log sheet\n')
                insertRow = [datetime.today().strftime('%Y-%m-%d  %H:%M'), self.ID,  self._ASIN, '' ,'', '', '', '' ,'','', self._ManualLog, '' ]
                self.gsheet_job_log_Update.append_row(insertRow)   
                self.post.ProcessErrorLog(self, 1, "gsheet append row Sucessfully")
                self.gsheetData_job_log = self.gsheet_job_log_Update.get_all_records()
                self.gsheetData_job_log = pd.DataFrame.from_dict(self.gsheetData_job_log)

            

            return self.gsheetData            
        except Exception as err:                 
            print("openbrowser",str(err)) 
            self.post.ProcessErrorLog(self, 2, "gsheet " + str(err)) 
 
    def loadASIN(self):
        try:
            
            self.arr=[]
            self.gsheetData = self.readgooglesheet()
            if  self.gsheetData.empty:
                # self.post.ProcessErrorLog(self, 1, f'self.gsheetData is empty')
                print(f'self.gsheetData is empty, check loadASIN method... ')

            for indices, row in self.gsheetData.iterrows():
                self.arr.append(str(row['CountryID']) + '|'+ str(row['ASIN']).strip()+ '|'+ str(row['ID']).strip())  

            
            
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
                        
    def generate_email_html(self, report_abuse_case_id, seller_support_case_id , all_child_asins, lab_report_status = None, email_case_id = '', subject = ' '):
            
        """
            Html template for Dangerous goods
        """
        try:
            if email_case_id :
                email_case_id_content = f"""
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">SAS Case ID:
                </span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">{email_case_id}<br>
                </p>
                """
                REQUIRE_FURTHER_PROOF_CONTENT = '''<span>3.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp; </span>
                </span><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">Require further proof ASIN is DF Flammable 
                </span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><br>'''

            else:
                email_case_id_content = ""
                REQUIRE_FURTHER_PROOF_CONTENT = ''
            
            if lab_report_status:
                
                body = f"""
                <div> <br><br>
                Dear Issue Assistance Team,
                <br> <br>
                RE: {subject} <br>
                <br>
                Please take note that the following Market Place listings is FLAMMABLE and incorrectly classified as Normal FBA.
                <br>
                ASIN: {all_child_asins}
                <br><br>
                We are also including the Lab Test Report which clearly says that the Product is FLAMMABLE.
                <br><br>

                </div>
                """
                issue_details_content = f"""

                <span><span>1.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;
                </span></span></span><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"> Opened case to Report Abuse <br>Unable to assist
                </span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph;text-indent:0in">
                <span><span style="color:black">ID <span lang="JA">–</span></span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"> {report_abuse_case_id}</span><span style="font-family:&quot;Arial&quot;,sans-serif"></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"><span>2.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Open case with Seller Support <br>Unable to assist as request is not in their Scope </span></span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black"><br>
                <br>
                <span>ID – </span>{seller_support_case_id} </span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"></span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
                
                {REQUIRE_FURTHER_PROOF_CONTENT}
                <br>
                <span>{email_case_id} </span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph;text-indent:0in">
                <span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><br>

                <span>{"4. " if REQUIRE_FURTHER_PROOF_CONTENT else '3. '}<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp; </span>
                </span><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">Submitting report in this email confirming that the ASIN is indeed Flammable
                </span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><br>
                <br>

                <br></span><span></span></p>
                """
                related_case_content = f"""
                <span>Complaint ID:  </span>{report_abuse_case_id}<span></span></span></p>
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;</span></span></p>
                
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">Seller Support Case ID:
                </span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">{seller_support_case_id}<br>
                
                {email_case_id_content}
                
                
                """
                desired_result_line = f"""
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in">
                <span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"><span> <span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;
                </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Hazard Identification Report also confirms that the product is Flammable and Flash point below 60C</span></span></p>
                <p style="margin-left:.5in;text-indent:0in"><span><span style="font-size:11.0pt">&nbsp;</span></span></p>
            
                """

            else:
                body = f"""
                <div> <br><br>
                Dear Issue Assistance Team,\n<br><br>
                RE: {subject} <br>
                <br> <br>
                Please take note that the following Market Place listings is FLAMMABLE and incorrectly classified as Normal FBA.   <br>
                <br>
                ASIN:  {all_child_asins}
                <br><br>
            
                </div>
                """

                issue_details_content = f"""

                <span><span>1.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;
                </span></span></span><span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"> Opened case to Report Abuse <br>Unable to assist
                </span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph;text-indent:0in">
                <span><span style="color:black">ID <span lang="JA">–</span></span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"> {report_abuse_case_id}</span><span style="font-family:&quot;Arial&quot;,sans-serif"></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"><span>2.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black">Open case with Seller Support <br>Unable to assist as request is not in their Scope </span></span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:black"><br>
                <br>
                <span>ID – </span>{seller_support_case_id} </span><span><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif"></span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph">
                
                {REQUIRE_FURTHER_PROOF_CONTENT}
                <br>
                <span> {email_case_id} </span></span></p>
                <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in;text-align:justify;text-justify:inter-ideograph;text-indent:0in">
                <span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><br>

            

                <br></span><span></span></p>
                """
                related_case_content = f"""
                <span>Complaint ID:  </span>{report_abuse_case_id}<span></span></span></p>
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;</span></span></p>
                
                <p style="margin-bottom:12.0pt;text-align:justify;text-justify:inter-ideograph">
                <span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">Seller Support Case ID:
                </span></span><span style="font-family:&quot;Arial&quot;,sans-serif;color:black">{seller_support_case_id}<br>
                
                {email_case_id_content}
                
                
                """

                desired_result_line = ''

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
            <p><span><span style="color:black">Alex Ho</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></p>
            </td>
            </tr>
            <tr style="height:17.25pt">
            <td width="320" style="width:240.0pt;border:solid #a3a3a3 1.0pt;border-top:none;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
            <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Seller Email</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
            </td>
            <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt;box-sizing:border-box;word-break:break-word">
            <p><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><a href="mailto:rebecca.dark@sti-aromas.com" target="_blank">rebecca.dark@sti-aromas.com</a></span><u><span style="font-family:&quot;Arial&quot;,sans-serif;color:#0563c1"></span></u></p>
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
            </span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Based on multiple claims on Seller product detail page’s and ingredient CAS numbers ASINs are Flammable.</span></span></p>
            <p style="margin-left:.5in;text-indent:0in"><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">&nbsp;</span></span></p>
            {desired_result_line}
            <p style="margin-right:0in;margin-bottom:12.0pt;margin-left:.5in">
            <span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"><span><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;
            </span></span></span></span><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">ASINs to be correctly classified as Dangerous Goods (DG) and sold under the DG Program <br> ASIN List: {all_child_asins} </span></span></p>
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
            <p><span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Yes included are some screen captures on Sellers Claims on the Detail Pages</span></span><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"><br>
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
            <p><span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black">Account Manager Email</span></b></span><b><span style="font-size:11.0pt;font-family:&quot;Arial&quot;,sans-serif;color:black"></span></b></p>
            </td>
            <td width="457" style="width:343.0pt;border-top:none;border-left:none;border-bottom:solid #a3a3a3 1.0pt;border-right:solid #a3a3a3 1.0pt;background:#f2f2f2;padding:.75pt .75pt .75pt .75pt;height:17.25pt">
            <p><span style="font-family:&quot;Arial&quot;,sans-serif;color:black"><a href="mailto:anramrod@amazon.com" target="_blank">anramrod@amazon.com</a></span></p>
            </td>
            </tr>
            </tbody>
            </table>
            
            <br><br>
            Thanks,
            <br><br>
            Rebecca\n<br><br>
            """
            
            return html

        except Exception as e:
            print('Issue in Creating HTML Template ', e)
            self.post.ProcessErrorLog(self, 2, f"  Issue in Creating HTML Template {e}  ")
    
    def send_email_SAS(self, asin, subject, file_path=None, file = None, report_abuse_case_id = None, seller_support_case_id = None, lab_report_status = None, email_case_id= '', sas_manager = False, follow_up_text = None):
        """
            Send email with Wrong Category node
        """

        text_sas_manaager = f"""Hi Andres,\n
Would need your assistance on the following SAS Issue Assistance cases as it has been more than 14 Days following up with SAS-IA but there is still no resolution.\n
Please find the list of ASINs below along with Case IDs from Report Abuse, Seller Support & SAS-IA \n
\nThanks,\n
Rebecca"""
        
        try:
            today =  date.today()
            #body = "This is an email with attachment sent from Python"
            sender_email = "rebecca.dark@sti-aromas.com"
            
            cc_email = []
            if sas_manager:
                receiver_email = 'anramrod@amazon.com'
                # receiver_email = ["dnndiz@amazon.com"]
                cc_email = [ "rebecca.dark@sti-aromas.com", "gaurav.k.gosain@sti-aromas.com", 'lizzypan@sti-aromas.com', 'mlopezif@amazon.com']
            else:
                receiver_email ="sas-issue-assistance@amazon.com" 
            password = '#Gya12341'
            

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(receiver_email) if isinstance(receiver_email, list) else receiver_email
            message["Cc"] = ", ".join(cc_email) if isinstance(cc_email, list)  else cc_email
            message["Subject"] = subject
            
            if follow_up_text:
                text = follow_up_text
                part1 = MIMEText(text, "plain")
                message.attach(part1)
            elif sas_manager:
                text = text_sas_manaager
                part1 = MIMEText(text, "plain")
                message.attach(part1)
            else:
                email_html = self.generate_email_html(report_abuse_case_id, seller_support_case_id, asin, lab_report_status = lab_report_status, email_case_id = email_case_id, subject=subject )
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
                ### we SEND THE PDF LAB REPORT HERE
                filename = os.path.basename(file)
                with open(file, 'rb') as attachment:
                    part2 = MIMEBase('application', 'octet-stream')
                    part2.set_payload(attachment.read())
                    encoders.encode_base64(part2)
                    part2.add_header('Content-Disposition', f'attachment; filename= SAS_{filename}')
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

    def read_gmail_account(self, subject, mailserver_credentials = None):
        
        import imaplib
        import email

        # Create an IMAP object
        mailserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)

        # Your Gmail credentials
        # username = "gya.ads.portfolio.ai.01@gmail.com"
        # password = "`A3Rmqm/DHBJWF}B"

        # mailserver.login('temporaryc83@gmail.com', 'ylkvhxzyejpnshww')
        # mailserver.login(username, password )
        # Log in to the server
        mailserver.login('gya.ads.portfolio.ai.01@gmail.com', 'yfbcmddjqfetveun')
        
        if mailserver_credentials:
            mailserver.login(mailserver_credentials[0], mailserver_credentials[1])
        # Select a mailbox or folder
        mailserver.select('INBOX')

        # Search for unread emails with a specific subject
        status, ids = mailserver.search(None, f'(SUBJECT "{subject}")')

        # Convert the list of IDs to a list of integers
        ids = [int(id) for id in ids[0].split()]
        ids = ids[::-1]
        # Loop through each email ID
        for id in ids:
            # Fetch the email message by ID
            status, data = mailserver.fetch(str(id), '(RFC822)')
            # Parse the email message into a Python object
            message = email.message_from_bytes(data[0][1])
            # Print some information about the email
        
            otp = message['Subject']
            # otp = otp[:6]
            # print(otp)
            print('From:', message['From'])
            print('Subject:', message['Subject'])
            print('Date:', message['Date'])
            
            # Get the email body
            if message.is_multipart():
                # The email body is a multipart message
                for part in message.walk():
                    # Find the HTML part
                    if part.get_content_type() == 'text/html':
                        # Get the payload and decode it
                        body = part.get_payload(decode=True).decode()
                        # Print the email body
                        print('Body:', body)
                        return body
                    
                    elif part.get_content_type() == 'text/plain':
                        # Get the payload and decode it
                        body = part.get_payload(decode=True).decode()
                        # Print the email body
                        print('Body:', body)
                        return body
                       
            else:
                # The email body is not a multipart message
                # Get the payload and decode it
                body = message.get_payload(decode=True).decode()
                # Print the email body
                print('Body:', body)
                return body
              
    def DownloadGoogleFile(self, filename ):
        #self._DefaultName = 'HEO030M14_PARENT'

        
        _filename = [ filename +'.pdf' ]
        time.sleep(2)
        try:
           
            CLIENT_SECRET_FILE = 'GoogleCredentials\client_sheet.json'
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']
                
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

            results = service.files().list(
                q=f"'16fm3LVKRRL_QXHDLGYV8cXMEVTqShdgj' in parents",    
                pageSize=1000, 
                fields="nextPageToken, files(id, name, mimeType, parents, trashed)"
            ).execute()
            items = results.get('files', [])
            items = pd.DataFrame(items)  
            items = items[ (items['name'].str.lower().isin(map(str.lower, _filename))) & (items['trashed'] == False) ]
            
            if not os.path.exists(self.Lab_Reports_path):
                os.makedirs(self.Lab_Reports_path)
                
            if os.path.exists(self.Lab_Reports_path + _filename[0])==True:
                os.remove(self.Lab_Reports_path + _filename[0])

            if len(items)==1:
                for _indices, _filedetails in items.iterrows(): 
                    request = service.files().get_media(fileId = _filedetails['id'])
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))
                    dfilespath = self.Lab_Reports_path +'\\'+ _filedetails['name']
                    if 1==1:
                        with io.open(dfilespath, "wb") as f:        
                            fh.seek(0)
                            f.write(fh.read())
                    else:
                        with io.open(dfilespath, "wb") as f:        
                            fh.seek(0)
                            f.write(fh.read())
                return dfilespath       
            else:                
                self.post.ProcessErrorLog(self, 2, "Error DownloadGoogleFile files count not match " + filename + ' ' + str(len(items))) 
                return False
            
            time.sleep(2)            
            return True  
        except Exception as err:                       
            self.post.ProcessErrorLog(self, 2, "Error DownloadGoogleFile " + filename + ' ' + str(err)) 
            return False 

    def recheck_email_case(self, asin ,  sas_ia=None, lab_report=None, sas_ia_report = None ):

        asin = asin  

        def search_with_keyword():

            try:
                report = None
                if lab_report:
                    report = "Lab_Report_SAS_Case"
                if sas_ia:
                    report = sas_ia_report 
                    
                subject = self.all_cases_dataset[ (self.all_cases_dataset['Product_Stage_ID'] == int(self.Stage_ID) ) & (self.all_cases_dataset['Type'] == report )]['Subject'].values   
                total_subjects = len(subject)
                if total_subjects > 1:
                    subject = subject[-1]
                    print('Going to search this subject for the ASIN', subject)
            
                if not subject and sas_ia:
                    self.post.ProcessErrorLog(self, 1, f'No subject found for the asin in all cases table   ');print(f'No subject found for the asin in all cases table   ')                
                    return False
                else: subject = subject[0] if total_subjects == 1 else subject
                date_str = ' '.join(subject.split('-')[-4:-1]).strip()
                date_obj = datetime.strptime(date_str.strip(), '%Y %m %d')
                date_of_case_id = date_obj.strftime('%B %d, %Y')
                date_of_case_id_obj = datetime.strptime(date_of_case_id, '%B %d, %Y')    
                
                keyword = subject
                for index, row in self.df_case_ids.iterrows():
                    if keyword in row['Subject Text']:
                        print("Subject present in row:", row)
                        case_id_number = row["Case ID"]
                        print(f'Got Case ID - {case_id_number} by subject in the original dataframe\n')
                        self.post.ProcessErrorLog(self, 1, f"Got Case ID - {case_id_number} by subject in the original dataframe ")
                        print(f'Current Status of this case id is {row["Case Status"]}')
                        self.post.ProcessErrorLog(self, 1, f"Current Status of this case id is {row['Case Status']}")
                        return case_id_number   
                    else:
                        print('Couldnt find the subject in the view case')
                        print('No Case Id number found matching as no subject found in the Dataframe .\n')
                        self.post.ProcessErrorLog(self, 1, 'No Case Id number found in the Dataframe.')
                        continue
            
            except Exception as err:  
                self._ManualLog = ""
                print("Error in Release",str(err)) 
                self.post.ProcessErrorLog(self, 2, "Error in Release email case - recheck_email_case() " + str(err)) 
                return f'error  {err}'

        result_of_case_id  = search_with_keyword()
        # if not result_of_case_id:
        #     result_of_case_id =  search_with_keyword('DG Violation Classify Flammable')
        #     if not result_of_case_id:
        #         result_of_case_id = search_with_keyword('Incorrect DG Classification of ASINs')
        return result_of_case_id

    def update_lab_report_case_id(self , single_entry = None ):
        """
           DG 
            - By Default = it will update BULK  entries 
            - By single_entry : will take - self.Gsheet_Data_current_row
        """
        try:   
            print("\nGetting the lab report Case Id number ")     
            list_of_subject_ = None; 
            asin = self._ASIN
            if single_entry:
                lab_id = self.Gsheet_Data_current_row['ID_Lab_Report_SAS_Case']
                if lab_id.values:
                    lab_id = int(lab_id.iloc[0])
                    case_row = self.all_cases_dataset[self.all_cases_dataset['ID'] == lab_id]
                    if case_row['Subject'].values and case_row['CaseID'].values[0] in ['', None]:
                        index_value = case_row.index.values[0]
                        subject_value = case_row['Subject'].values[0]
                        # list_of_subject_ = [( index_value, subject_value)]
                        stage_id = index_value

                        print(f"Checking - ASIN: {asin} -", f" ID: {stage_id} -", f' Subject: {subject_value}')
                        body = self.recheck_email_case(asin , lab_report=True)
                        print('body - ',body)
                        if body == 'error' : return 'error'
                        print("Body", body)
                        
                        if not body:
                            print(f"Asin {asin} Body not found for the email subject from the portal\n")
                            return False

                        print(f"\n Email body found for asin - {asin}  from the email subject from amazon portal, will update the DB.\n\n")
                        self.post.ProcessErrorLog(self, 1, f"Asin {asin} Body found from the email subject")
                        if asin and body:
                            self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = body, Subject = subject_value, CaseStatus = 'On Going', Status = 1, asin = asin)

                        self.post.ProcessErrorLog(self, 1, f'DB entry inserted successfully  for asin {asin} for the the lab report SAS Case  ')
                        print(f'DB entry inserted successfully for asin {asin} for the the lab report SAS Case   ')
                        return body
        
                    else:
                        self.post.ProcessErrorLog(self, 1, f' Subject case ID found - { case_row["CaseID"].values[0]}  ')
                        print(f'Subject case ID found - {case_row["CaseID"].values[0]}  ')
                        return case_row['CaseID'].values[0]

            else:
                list_of_subject_ = list(self.all_cases_dataset[
                    (self.all_cases_dataset['Type'] == 'Lab_Report_SAS_Case') &
                    (self.all_cases_dataset['Subject'].str.startswith('DG')) &
                    ((self.all_cases_dataset['CaseID'].isna()) | (self.all_cases_dataset['CaseID'] == ''))
                ][['ID', 'Product_Stage_ID', 'Subject']].itertuples(index=False, name=None))


            if not list_of_subject_:
                self.post.ProcessErrorLog(self, 1, f'No Lab Report Subjects Found...  ')
                print(f'No Lab Report Subjects Found...   ')
                return True
            
            print('\t\nUpdating all the Lab report Subjects\n')
            body = None
            asin = None
            for each_iteration in list_of_subject_:
                try:
                    stage_id = each_iteration[1]
                    condition_met = (
                        (self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "DG_Class"].values[0] != "DG") and
                        (self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "Monitor_Status"].values[0] != "Completed"))
                    if condition_met:
                        asin_values = self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "ASIN"].values
                        if asin_values: asin = asin_values[0]
                        self.Gsheet_Data_current_row = self.gsheetData[(self.gsheetData['ASIN'] == asin) ]
                        self.Stage_ID = stage_id 
                        subject = self.all_cases_dataset[ (self.all_cases_dataset['Product_Stage_ID'] == stage_id ) & (self.all_cases_dataset['Type'] == "Lab_Report_SAS_Case" )]['Subject'].values
                        if len(subject)> 1:
                            subject = subject[-1]
                        print(f"\n\nChecking - ASIN: {asin} -", f" ID: {stage_id} -", f' Subject: {subject}')
                        body = self.recheck_email_case(asin , lab_report=True)
                        
                except Exception as e: 
                    print(0)
                if body == 'error' : return 'error'
                if not body:
                    print(f"Asin {asin} Body not found for the email subject from the portal\n")
                    continue

                print(f"Email body found for asin - {asin}  from the email subject from amazon portal, will update the DB.\n\n")
                self.post.ProcessErrorLog(self, 1, f"Asin {asin} Body found from the email subject")
                if isinstance(subject, (list, np.ndarray)):
                    subject = ', '.join(map(str, subject))
                if asin and body:
                    self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = body, Subject = subject, CaseStatus = 'On Going', Status = 1, asin = asin)

                self.post.ProcessErrorLog(self, 1, f'DB entry inserted successfully  for asin {asin} for the the lab report SAS Case  ')
                print(f'DB entry inserted successfully for asin {asin} for the the lab report SAS Case   ')
        except Exception as e:
            self.post.ProcessErrorLog(self, 1, f'Issue in Updating Lab report case ID  ')
            print(f' Issue in Updating Lab report case ID  - error -> {e} ')
            return False

    def update_case_id(self, ID , multiple_entries_update = False, SAS_REPORT = None ):
        """
            Updating Email body subject with case id number once we get it from portal
            - By Default = it will update single entry 
            
            - for multiple entries -
                
                list(self.gsheetData_job_log[self.gsheetData_job_log['SAS - IA'].astype(str).str.startswith('DG')]['ASIN'].items())

        """
        try:
            print('\tUpdating all the SAS - IA Subjects\n')
            if multiple_entries_update:

                SAS_REPORTS = ["SAS-IA","SAS-IA_2" ]
                for SAS_REPORT in SAS_REPORTS:

                    index_asin_updating_SAS = list(self.all_cases_dataset[
                        (self.all_cases_dataset['Type'] == SAS_REPORT) &
                        (self.all_cases_dataset['Subject'].str.startswith('DG')) &
                        ((self.all_cases_dataset['CaseID'].isna()) | (self.all_cases_dataset['CaseID'] == ''))
                    ][['ID', 'Product_Stage_ID', 'Subject']].itertuples(index=False, name=None))
                    
                    print(f'\t\nUpdating all the {SAS_REPORT} reports Subjects\n')

                    body = None
                    asin = None

                    for each_entry in index_asin_updating_SAS:
                        try:
                            stage_id = each_entry[1]
                            condition_met = (
                                (self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "DG_Class"].values[0] != "DG") and
                                (self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "Monitor_Status"].values[0] != "Completed"))
                            asin_values = self.gsheetData.loc[self.gsheetData["Stage_ID"] == stage_id, "ASIN"].values
                            if asin_values: asin = asin_values[0]
                            self.Gsheet_Data_current_row = self.gsheetData[(self.gsheetData['ASIN'] == asin) ]
                            if condition_met:
                                stage_id = int(self.Gsheet_Data_current_row["Stage_ID"].values[0])
                                self.Stage_ID = stage_id
                                subject = self.all_cases_dataset[ (self.all_cases_dataset['Product_Stage_ID'] == stage_id ) & (self.all_cases_dataset['Type'] == SAS_REPORT  )]['Subject'].values[0]
                                print(f"\n\nChecking - ASIN: {asin} ", f"\nID: {stage_id} ", f'\nSubject: {subject}')
                                body = self.recheck_email_case(asin, sas_ia=True, sas_ia_report = SAS_REPORT )
                                print("Body", body)
                                if body == 'error' : return 'error'
                            else: print('Asin has been Marked DG', asin)
                        except Exception as e: 
                            print(0)

                        if not body:
                            print(f"Asin {asin} Body not found for the email subject from portal\n")
                            continue
                        else:
                            print(f"Asin {asin} Body found from the email subject from amazon portal, will update the cell.\n\n")
                            self.post.ProcessErrorLog(self,1,f"Asin {asin} Body found from the email subject")
                            self.create_update_data_PG_all_cases_table(caseType = SAS_REPORT, CaseID = body , CaseStatus = 'On Going', Status =1 )

            if not SAS_REPORT:
                SAS_REPORT = self.SAS_REPORT

            asin = self._ASIN
            
            
            body = self.recheck_email_case(asin , sas_ia=True, sas_ia_report = SAS_REPORT )
            print('body - ',body)
            if body == 'error' : return 'error'
            if not body:
                print(f"No case number found  for asin {asin} , will continue \n")
                self.post.ProcessErrorLog(self,1,f"No case number found  for asin {asin} , will continue")
                return False
            
            print(f"Case number found for ASIN {asin}  will update the cell.")
            self.post.ProcessErrorLog(self,1,f"Asin {asin} Body found from the email subject")


            self.create_update_data_PG_all_cases_table(caseType = SAS_REPORT, CaseID = body , CaseStatus = 'On Going', Status =1 )
            
            
            self.post.ProcessErrorLog(self, 1, f'DB entry inserted successfully for asin {asin} for the SAS case ID  ')
            print(f'DB entry inserted successfully for asin {asin} for the SAS case ID   ')


            return body
            
       
        except:
            self.post.ProcessErrorLog(self,1,'Issue in Updating SAS body email subject')
            self._ManualLog = "Issue in Updating Email body"

    def Update_Master_sheet(self, lab_report_columns = None ):
        
        try:
            self.gsheetData = self.readgooglesheet()
            self.Gsheet_Data_current_row = self.gsheetData[(self.gsheetData['ASIN'] == self._ASIN) ]
            all_values = self.Gsheet_Data_current_row.values.tolist()[0]
            asin = all_values[2]
            all_cases_dataset = self.all_cases_dataset[self.all_cases_dataset['Product_Stage_ID'] == self.Stage_ID]
            if all_cases_dataset.empty :
                self.post.ProcessErrorLog(self, 1, f'DG already Marked as completed without creating any case  ')
                print(f'DG already Marked as completed without creating any case  ')

                data = {
                    'Days': "1",
                    'Stage': "1",
                    'Monitor_Status': 'Completed',
                    'DG_Class': 'DG' }
                if lab_report_columns: data["Lab_Report"] = 'Yes'; data["Lab_Date"] = ''.join(lab_report_columns.values())
                self.insert_update_data_Stage_(data, Status = 1)
                self.post.ProcessErrorLog(self, 1, f'Stage Table Updated Successfully for ASIN {self._ASIN} for STAGE ID = {self.Stage_ID}')
                print(f'Stage Table Updated Successfully for ASIN {self._ASIN} for STAGE ID = {self.Stage_ID} ')
                return 1
                
            same_case = (self.all_cases_dataset['Product_Stage_ID'] == int(self.Stage_ID))

            
            
            self.post.ProcessErrorLog(self, 1, f'Updating asin {asin} In Stage Table ')
            print(f'Updating index asin {asin} In  Stage Table ')
            

            stage_number = 1
            first_stage = [ 'Report_Abuse_Backend', 'SAS-IA', 'Seller_Support_Case' ]
            second_stage = [ 'Lab_Report_SAS_Case' ]
            third_stage = ['SAS_Manager' ]
            all_cases_created = self.all_cases_dataset[ same_case &  (self.all_cases_dataset['Type'] )]['Type'].tolist()
            if all(stage in all_cases_created for stage in first_stage):
                stage_number = 1
            if all(stage in all_cases_created for stage in second_stage):
                stage_number = 2
            if all(stage in all_cases_created for stage in third_stage):
                stage_number = 3
         

            if not self.case_status_:
                self.case_status_ = 'On Going'
            if stage_number !=3:
                if all([case for case in all_cases_created if case == 'SAS-IA']) and self.Gsheet_Data_current_row['Lab_Report'].iloc[0].lower().startswith("yes"):
                   stage_number = 2            

            sas_ia_case_id = self.all_cases_dataset[ same_case &  (self.all_cases_dataset['Type'] == self.SAS_REPORT )]['Subject'].values 
            
            ### from the subject lets get the case number if available
            # case_number_sas_ia = self.all_cases_dataset[ same_case &  (self.all_cases_dataset['Type'] == sas_ia_report )]['CaseID'].values
            case_number_sas_ia = self.all_cases_dataset[ same_case &  (self.all_cases_dataset['Type'] == self.SAS_REPORT )]['CaseID'].values
            if len(case_number_sas_ia)>1:
                case_number_sas_ia = case_number_sas_ia[0]
            if len(sas_ia_case_id)>1:
                try:
                    sas_ia_case_id = sas_ia_case_id[0]
                    sas_ia_case_id = int(case_number_sas_ia)
                except:
                    print('No case Number found with the subject, thus no RPA job link')

            current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            data = {}
            
            dg_status = all_values[10]
            if dg_status.startswith('DG'):
                dg_status = 'DG'
                self.case_status_ = 'Completed'
            else:
                dg_status = 'Non DG'
                data['Check_Date'] = current_date
                if self.case_status_ !='Cancelled':
                    self.case_status_ = 'On Going' 

            ###  First initial SAS case created ! FIXED - DONT CHANGE
            initial_date = self.all_cases_dataset[ same_case &  (self.all_cases_dataset['Type'] == 'Seller_Support_Case' )]['Date'].values
            if len(initial_date) >= 2:
                initial_date = initial_date[-1]
            if len(initial_date) ==1:
                initial_date = initial_date[0]
            else:
                initial_date = all_values[5]
                

            start_date_asin = datetime.strptime(initial_date, '%Y-%m-%d %H:%M') 
            days_difference = str((datetime.now() - start_date_asin).days)


            if dg_status == 'DG':
                start_date = datetime.strptime(initial_date, '%Y-%m-%d %H:%M') 
                end_date = all_values[11]
                end_date = datetime.strptime(end_date,'%Y-%m-%d %H:%M' )
                days_difference = str((end_date - start_date ).days)
                
            if days_difference == '0' :
               days_difference = '1'
                
            rpa_link = ''
            if case_number_sas_ia:
               rpa_link = f"https://sellercentral.amazon.com/cu/case-dashboard/view-case?ref=sc_cd_lobby_vc_v3&ie=UTF&caseID={case_number_sas_ia}"
            
            data['Days'] = days_difference
            data['Filing_Activity'] = initial_date
            data['Rpa_Job_Log_Row'] = rpa_link
            data['DG_Class'] = dg_status
            data['Stage'] = stage_number
            data['Monitor_Status'] = self.case_status_
            ### if need to send END DATE IN DASHBOARD -> data["Check_Date"] = '2023-11-16 19:49'    
            if lab_report_columns: data["Lab_Report"] = 'Yes'; data["Lab_Date"] = ''.join(lab_report_columns.values())
            r = self.insert_update_data_Stage_(data, Status =1)  ; print( r)
            self.post.ProcessErrorLog(self, 1, f'Stage Table Updated Successfully for ASIN {asin}  ');print(f'Stage Table Updated Successfully for ASIN {asin}   ')
            return r
        except Exception as e:
            print(f' Issue in Updating Main sheet of DG - {e}')
            self.post.ProcessErrorLog(self, 2, f' Issue in Updating Main sheet of DG - {e}')
            return False

    def update_form_content(self,asin,  complaint_number, seller_support_case_number, SAS_IA_case_number='', SAS_Lab_report_case_number = ''):
        """
            new template is master excel form 
            which will be updated and send for each asin
        """
        try:
            new_template = f"{self.DownloadLocation}SAS_Core_Issue_Assistance_Form.xlsx"
            wb_source_new_template = xw.Book(new_template)
            sheet_source_new_template = wb_source_new_template.sheets['Sheet1']  

            SAS_CONTENT = ''
            RELATED_CASE_CONTENT = f'Complaint ID: {complaint_number} Seller Support Case ID: {seller_support_case_number} '
            
            ### If SAS IA Case number or Lab report Case number is given, use this Content
            if SAS_IA_case_number or SAS_Lab_report_case_number:
                SAS_CONTENT =f"""
3.    Require further proof ASIN is DF Flammable

ID - {SAS_IA_case_number}, {SAS_Lab_report_case_number if SAS_Lab_report_case_number else '' }

4.    Submitting report in this email confirming that the ASIN is indeed Flammable"""

                RELATED_CASE_CONTENT = RELATED_CASE_CONTENT + f""" SAS Case ID: {SAS_IA_case_number}, {SAS_Lab_report_case_number}"""

            ### else we use the below content
            sheet_source_new_template.range('B7').value = f"""
1.     Opened case to Report Abuse
Unable to assist

ID - {complaint_number}

2.    Open case with Seller Support
Unable to assist as request is not in their Scope

ID - {seller_support_case_number}

{SAS_CONTENT}

"""
        
            sheet_source_new_template.range('B9').value = f"""
1.    Based on multiple claims on Seller product detail page’s and ingredient CAS number ASINs is Flammable
2.    Hazard Identification Report also confirms that the product is Flammable and Flash point below 60C
3.    ASIN to be correctly classified as Flammable Dangerous Goods (DG) ASIN: {asin} """
        
            sheet_source_new_template.range('B10').value = f"{RELATED_CASE_CONTENT}"

            excel_updated_path = f"{self.dangerous_good_directory_path}/SAS_{asin}_Core_Issue_Assistance_Form.xlsx"
            wb_source_new_template.save(excel_updated_path)
            wb_source_new_template.app.quit()
        
            return excel_updated_path
        
        except Exception as e:
            print('Issue in Creating Form, will retry later...', e)
            self.post.ProcessErrorLog(self,1, 'Issue in Creating Form, will retry later... ', e)
            return False

    def check_case_status_(self, id ):
        try:
            if not id: print('no id given')
            self.driver.get(f'https://sellercentral.amazon.com/cu/case-dashboard/view-case?ref=sc_cd_lobby_vc_v3&ie=UTF&caseID={id}')
            time.sleep(5)
            reply_btn = self.driver.find_elements(By.CLASS_NAME,'view-case-reply-buttons-container')
            if len(reply_btn) <=0:
                self.case_status_ = False
                return False
            else:
                self.post.ProcessErrorLog(self, 1, f'Case On-going...');print(f'Case On-going...  ')
                print('')
                self.case_status_ = 'On Going'
                return self.case_status_
        except Exception as e:
            self.post.ProcessErrorLog(self, 1, f'Issue in checking status of the ID  ');print(f'Issue in checking status of the ID')
            return "error"

    def insert_update_data_Stage_(self, data, Status = 0, asin = None):
        """
            Updated / Inserts : public."DG_Product_Stage"
        """
        try:
            
            if not asin:
                asin = self._ASIN

            jsondata = data
            jsondata['stage_id'] = str(self.Stage_ID)
            if not Status:
                Status = 0   ### means we inserted a new entry if Status is not set
                jsondata['Product_Master_ID'] = str(self._PK_ID)
                jsondata['Monitor_Status'] = "On Going"
                print(f'Data Inserted Successfully for asin {self._ASIN} for Product Stage ID =  {self.Stage_ID}')
            para = {    
                    "data" : {"userid":2, 'source': jsondata, "ID": Status , "table": "Update_Report_Abuse" },
                    "type":"Insert" }
            jsondata = self.post.PostApiParaJson(para)
            return jsondata

        except Exception as e:
            content = f"Error updating data in table: {e}"
            print(content)
            self.post.ProcessErrorLog(self, 2, f" Error updating data in table: {e}")
            return False

    def create_update_data_PG_all_cases_table(self, caseType = None, CaseID = None, Subject = None, CaseStatus = 'On Going', Status = 0, asin = None, Date = None):
        """
            | Status  =  0 or 1
            |   Create an entry == 0
            |   Update an entry >= 1
        """
        if not asin:
            asin = self._ASIN
        if not self.Stage_ID: return False
        jsondata =    {
                    'Product_Stage_ID': str(self.Stage_ID),
                    'Type': caseType ,                            
                    'Subject': Subject,
                    'CaseID':CaseID,
                    'CaseStatus': CaseStatus,
                    "Date": Date if Date else None
                    }
        jsondata = {key: value for key, value in jsondata.items() if value is not None}
        asin = self.gsheetData[self.gsheetData["Stage_ID"] == self.Stage_ID]['ASIN'].values[0]
        if not Status:
            Status = 0   ### means we inserted a new entry if Status is not set
            print(f'Data Inserted Successfully for asin {self._ASIN} for  ASIN =  { asin } for caseType - {caseType} ')
            self.post.ProcessErrorLog(self, 1, f'Data Inserted Successfully for asin {self._ASIN} for  ASIN =  { asin } for caseType - {caseType}')
        else:
            print(f'Data  Updated Successfully for asin {asin} for  ASIN =  {  asin  } for caseType - {caseType}  ')
            self.post.ProcessErrorLog(self, 1, f' Data  Updated Successfully for asin {asin} for  ASIN =  {  asin  } for caseType - {caseType} ')
        para = {    
            "data" : {"userid":2, 'source': jsondata, "ID": Status , "table": "Update_final_stage_Abuse" },
            "type":"Insert" }
        jsondata = self.post.PostApiParaJson(para)
        print('jsondata', jsondata)
        return jsondata

    def inform_users_via_mail(self, subject, body, missing_lab_report = False, sas_manager = False):

        """
            Informing Users via Mail 
        """
        try:
            today =  date.today()
            #body = "This is an email with attachment sent from Python"
            sender_email = "rebecca.dark@sti-aromas.com"
            password = '#Gya12341'
            cc_email = []

            
            ### Test 
            receiver_email = "gyalabs.it29@gmail.com"
            
            ### inform USER 
            receiver_email = "lizzypan@sti-aromas.com" 
            cc_email = ["rebecca.dark@sti-aromas.com", "gaurav.k.gosain@sti-aromas.com"]

            ### missing lab reports mail
            if missing_lab_report: 
                receiver_email = 'cong@sti-aromas.com'
            
            ### SAS manager mail
            # if sas_manager:
            #     receiver_email = 'anramrod@amazon.com'

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

        except:
            return False 


    def create_directory(self, directory_path):
        """Creates a directory if it does not exist."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def copy_image(self, image_path, destination_directory_path):
        """Move an image to a destination directory."""
        shutil.copy(image_path, destination_directory_path)


    def getdatafromamazon(self):        

        
        try: 

            self.IsComplete = 0
            self.ID =  self.post.ProcessUpdate(self)   
           
            # self.IDList = self.IDList[80:]
            time.sleep(5)
            for indices, row in self.IDList.iterrows():  

                self.result_classification_product = None
                
                try:  

                    if ((self.StartDate + timedelta(hours=5)) <  datetime.now()):
                        self.post.ProcessErrorLog(self, 1, "Job Time Over")
                        return       
                            
                    if int(row['Status'])!=0:
                        continue
                    
                    ### store all the case ids in a dataframe
                    res = self.get_cases_in_df()
                    if not res:
                        self.post.ProcessErrorLog(self, 1, f'Cant proceed ahead, as dataframe of case ids not implemented   ');print(f'Cant proceed ahead, as dataframe of case ids not implemented   ')
                        return False
                    
                    self.gsheetData = self.readgooglesheet()
                    self.post.ProcessErrorLog(self, 1, f'Added Logs In DG Violation - Updated Changes ')
                    _CountryID = int(row['Process_Name'].split('|')[0])
                    self._ASIN = row['Process_Name'].split('|')[1]
                    self._PK_ID = row['Process_Name'].split('|')[2]
                    self._ASIN = self._ASIN.strip()
                    # self._ASIN = "B01MUCO6ZU"
                    self.post.ProcessErrorLog(self, 1, f'Going for asin {self._ASIN}  ')
                    print(f'\nGoing for ASIN - {self._ASIN} , PK ID - {self._PK_ID} \n ')
                    Product = self.gsheetData[self.gsheetData['ASIN'].str.strip() == self._ASIN]['ProductName'].values[0]
                    brand = self.gsheetData[self.gsheetData['ASIN'].str.strip() == self._ASIN]['Brand'].values[0]
                    self.Gsheet_Data_current_row = self.gsheetData[(self.gsheetData['ASIN'] == self._ASIN) ]
                    ### Checks if File is found for this asin or not 
                    lab_report_file_status = 'Yes'  if str(self.gsheetData[(self.gsheetData['ASIN'] == self._ASIN) ]['Lab_Report'].iloc[0]).lower().startswith('yes') else False
                    self.complaint_number = None
                    lab_date = self.gsheetData[(self.gsheetData['ASIN'] == self._ASIN) ]['Lab_Date'].iloc[0]
                    # self._PK_ID = self.Gsheet_Data_current_row["ID"].values[0] 


                    
                    
                    """  For Bulk Updates incomment below entries """
                    ### Update all the case id number of lab reports in BULK !
                    # self.update_lab_report_case_id()

                    ### Update all the case id number of SAS Cases in BULK !
                    # self.update_case_id(1, multiple_entries_update = 1)

                    ### Update particular case id or their status from Product all cases table ### ~~~ just change the Case ID NUMBER ~~~
                    # r = self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case" , CaseID = "14840852491" ,  CaseStatus =  'On Going', Status = 1 )
                    # r = self.create_update_data_PG_all_cases_table(caseType = "SAS-IA",  CaseID = "14723696941" , CaseStatus =  'On Going', Status = 1 )
                    
                    
                    

                    if lab_report_file_status:
                        lab_report_columns = {'Yes': lab_date}   
                    ### Get the Previous Stage_ID if exists
                    self.Stage_ID = ( 0 if self.Gsheet_Data_current_row.empty else self.Gsheet_Data_current_row['Stage_ID'].iloc[0] )
                    if self.Gsheet_Data_current_row["Monitor_Status"].iloc[0] == "Completed" and self.all_cases_dataset[self.all_cases_dataset['Product_Stage_ID'] == self.Stage_ID].empty :
                        
                        result_ = self.check_status(self._ASIN)
                        if result_ == 'Error' or result_ == "Deactivated":
                            self.post.ProcessErrorLog(self, 1, f'Moving Ahead for next ASINs, Error in check status - {self._ASIN}  ')
                            print(f'Moving Ahead for next ASINs, Error in check status - {self._ASIN}   ')
                            if result_ == "Deactivated" and self.Gsheet_Data_current_row['DG_Class'].iloc[0] !="Deactivated":
                                data = {'DG_Class': 'Deactivated', "Monitor_Status": "Deactivated"}
                                result_of_insert = self.insert_update_data_Stage_(data, Status = 1 ) 
                                self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} marked Deactivated  ');print(f'ASIN {self._ASIN} marked Deactivated  ')
                                row["Status"] = 1
                                row['Process_Log']= '' 
                                self.updateRPAProcessLog(row)
                        else:
                            if result_:
                                self.Update_Master_sheet(lab_report_columns = lab_report_columns)
                                row["Status"] = 1
                                row['Process_Log']= '' 
                                self.updateRPAProcessLog(row)
                                continue 

                    ###  Insert NEW entry and get new Stage_ID only if previous Stage ID does not exist
                    # if  self._ASIN  not in self.gsheetData["ASIN"].tolist()   :
                    if not self.Stage_ID:
                        if  self.Gsheet_Data_current_row['Stage_ID'].iloc[0] not in self.all_cases_dataset["Product_Stage_ID"].tolist()  and self.Gsheet_Data_current_row['DG_Class'].iloc[0] !="Deactivated"  :
                            self.Stage_ID = 0
                            data = {    
                                'Check_Date': datetime.now().strftime('%Y-%m-%d %H:%M')  ,
                                'DG_Class': "Non DG",
                                'Job_Log_ID': self.ID,
                                "Lab_Report": "Yes" if lab_report_file_status else '', "Lab_Date": lab_date
                                }
                            data ={k:v for k,v in data.items() if v}
                            ID__ =  self.insert_update_data_Stage_(data)
                            self.Stage_ID = ID__.get('data').get('id')

                        
                            self.post.ProcessErrorLog(self, 1, f'Inserted New Entry for ASIN {self._ASIN} with new Stage ID {self.Stage_ID}  ')
                            print(f'Inserted New Entry for ASIN {self._ASIN} with new Stage ID {self.Stage_ID}   ')
                    
                
                    
                    ### If Asin already marked DG in amazon revenue portal, we move ahead, updating both RPA and Master sheet
                    self.post.ProcessErrorLog(self, 1, f' Case Check Status {self._ASIN}, will check in revenue portal amazon page if its DG')
                    self.case_status_ = ''

                    ### Reopen case with new stage ID if DG converted to NON DG else continue
                    status_of_asin = self.Gsheet_Data_current_row['DG_Class'].values
                    if status_of_asin:
                        status_of_asin = status_of_asin[0]
                        if status_of_asin.startswith('DG') :
                                result_ = self.check_status(self._ASIN)
                                if result_ == 'Error' or result_ == "Deactivated":
                                    self.post.ProcessErrorLog(self, 1, f'Moving Ahead for next ASINs, Error in check status - {self._ASIN}  ')
                                    print(f'Moving Ahead for next ASINs, Error in check status - {self._ASIN}   ')
                                    if result_ == "Deactivated" and self.Gsheet_Data_current_row['DG_Class'].iloc[0] !="Deactivated":
                                        data = {'DG_Class': 'Deactivated', "Monitor_Status": "Deactivated"}
                                        result_of_insert = self.insert_update_data_Stage_(data, Status = 1 ) 
                                        self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} marked Deactivated  ');print(f'ASIN {self._ASIN} marked Deactivated  ')
                                    
                                    row["Status"] = 1
                                    row['Process_Log']= '' 
                                    self.updateRPAProcessLog(row)
                                    continue
                                else:
                                    if result_ :
                                        print(f'Dangerous Goods asin {self._ASIN} already have been marked, recheked from Revenue portal as well, proceeding ahead with other asins')
                                        self.post.ProcessErrorLog(self, 1, f'Dangerous Goods asin {self._ASIN} already have been marked, recheked from Revenue portal as well, proceeding ahead with other asins')
                            
                                        row["Status"] = 1
                                        row['Process_Log']= '' 
                                        self.updateRPAProcessLog(row)
                                        continue
                                    else:
                                        print(f'Dangerous Good marked but now entered into 2 stage where it has turned into Non DG')
                                        self.post.ProcessErrorLog(self, 1, f'Dangerous Good marked but now entered into 2 stage where it has turned into Non DG')
                                        ### Inserting New entry for same ASIN with new Stage ID
                                        
                                        data = {    
                                            'Check_Date': datetime.now().strftime('%Y-%m-%d %H:%M')  ,
                                            'DG_Class': "Non DG",
                                            'Job_Log_ID': self.ID,                                            
                                            }
                                        if self.Gsheet_Data_current_row['Lab_Report'].values:
                                            if self.Gsheet_Data_current_row['Lab_Report'].iloc[0].lower().startswith('yes'):
                                                data['Lab_Report'] = 'Yes'
                                        ID__ =  self.insert_update_data_Stage_(data) 
                                        self.Stage_ID = ID__.get('data').get('id')
                                        self.reopen_case = True
                                        self.post.ProcessErrorLog(self, 1, f'Inserted New Entry for ASIN {self._ASIN} with new Stage ID {self.Stage_ID}  ')
                                        print(f'Inserted New Entry for ASIN {self._ASIN} with new Stage ID {self.Stage_ID}   ')
                                        
                        else:
                            print(f'Checking Status of ASIN {self._ASIN} ')
                            self.post.ProcessErrorLog(self, 1, f'Checking Status of ASIN {self._ASIN}')
                    
                    
                    ### Update ASIN status as DG & move, else proceed ahead with cases creation
                    result_ = self.check_status(self._ASIN)
                    if result_ == 'Error' or result_ == "Deactivated":
                        self.post.ProcessErrorLog(self, 1, f'Moving Ahead for next ASINs, Error in check status  {self._ASIN}  ')
                        print(f'Moving Ahead for next ASINs, Error in check status  {self._ASIN}   ')
                        
                        if result_ == "Deactivated" and self.Gsheet_Data_current_row['DG_Class'].iloc[0] !="Deactivated":
                            data = {'DG_Class': 'Deactivated', "Monitor_Status": "Deactivated" }
                            result_of_insert = self.insert_update_data_Stage_(data, Status = 1 ) 
                            self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} marked Deactivated  ');print(f'ASIN {self._ASIN} marked Deactivated  ')
                        row["Status"] = 1
                        row['Process_Log']= '' 
                        self.updateRPAProcessLog(row)
                        continue
                    
                    else:
                        self.gsheetData = self.readgooglesheet()
                        self.Gsheet_Data_current_row= self.gsheetData[(self.gsheetData['ASIN'] == self._ASIN) ]
                        existing_result = self.Gsheet_Data_current_row.values.tolist()
                        if result_:
                            if existing_result : existing_result = existing_result[0] 
                            data = {
                                'DG_Class': 'DG',
                                'Job_Log_ID': self.ID,
                                'Monitor_Status': 'Completed',
                                'Check_Date': existing_result[11]   if  existing_result[9] == 'Completed'\
                                    and existing_result[10] == 'DG' else  datetime.now().strftime('%Y-%m-%d %H:%M'),
                                "Lab_Report": lab_report_file_status if lab_report_file_status else '', "Lab_Date": lab_date }
                            result_of_insert = self.insert_update_data_Stage_(data, Status = 1 ) 
                            self.post.ProcessErrorLog(self, 1, f'result_of_insert for marking DG {result_of_insert} for ASIN {self._ASIN}  ');print(f'result_of_insert for marking DG {result_of_insert} for ASIN {self._ASIN}  ')
                            print("Updating SAS-IA and Lab report case Status as Completed")
                            self.create_update_data_PG_all_cases_table(caseType = "SAS-IA", CaseStatus =  'Completed', Status = 1 )
                            self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseStatus =  'Completed', Status = 1 )

                            print(f'Dangerous Goods asin {self._ASIN}  marked,  proceeding ahead with other asins')
                            self.post.ProcessErrorLog(self, 1, f'Dangerous Goods asin {self._ASIN} marked, proceeding ahead with other asins')
                            self.Update_Master_sheet(lab_report_columns = lab_report_columns)
                            row['Status']=1
                            row['Process_Log']= '' 
                            self.updateRPAProcessLog(row)
                            continue

                    
                    asins_directory_path = os.path.join(os.getcwd(), "asins")
                    self.create_directory(asins_directory_path)
                    
                    dir_name = f"{self._ASIN}__{datetime.today().strftime('%Y_%m_%d_%H_')}"
                    dir_ = os.path.join(asins_directory_path, dir_name)
                    self.create_directory(dir_)

                    dangerous_good_directory_path = os.path.join(dir_,f"dangerous_good_images_{self._ASIN}_{ datetime.today().strftime('%Y_%m_%d_%H_') }")
                    self.create_directory(dangerous_good_directory_path)
                    
                    self.dir_name = f"{self._ASIN}__{datetime.today().strftime('%Y_%m_%d_%H_')}"
                    self.dir_ = os.path.join(self.asins_directory_path, self.dir_name)
                    self.dangerous_good_directory_path = os.path.join(self.dir_,f"dangerous_good_images_{self._ASIN}_{ datetime.today().strftime('%Y_%m_%d_%H_') }")
        
                    
                    def click_images():

                        ### Run classification image processing function for each ss of the ASIN
                        # self.asins_directory_path = self.result_classification_product
                        
                        print(f'\nStarted with classification report for ASIN - {self._ASIN}')
                        self.post.ProcessErrorLog(self, 1, f'Started with classification report for ASIN - {self._ASIN}')
                        self.result_classification_product = self.classification_product()
                        if not self.result_classification_product:
                            self.ImageCaptcha()
                            self.result_classification_product = self.classification_product()

                        ### Count of files saved !
                        if self.result_classification_product:
                            print( f"Total {len(os.listdir(self.result_classification_product))} files collected to be sent." )
                            self.post.ProcessErrorLog(self, 1, f"Total {len(os.listdir(self.result_classification_product))} files collected to be sent. ")
                            
                            ### Create one ss of ASIN if no images found !
                            if len(os.listdir(self.result_classification_product)) <=0:
                                print(f"ASIN {self._ASIN} Not Found to be dangerous good product ,Will mark  DG purposely ")
                                self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} Not Found to be dangerous good product ,Will mark  DG purposely ')
                                self.driver.get("https://www.amazon.com/dp/" + self._ASIN)
                                time.sleep(2)
                                image_path = f"{self.dangerous_good_directory_path}/main_page__ss.png"
                                time.sleep(2)
                                pyautogui.screenshot(image_path)
                                time.sleep(1.5)
                                img = cv2.imread(image_path)
                                cv2.line(img,  (130,95) ,(600,95) , (0,0,255), 4)  ### mark the RED line on the URL
                                time.sleep(1.5)
                                cv2.imwrite(image_path, img)
                                print("Marked...")

                        return self.result_classification_product

                                
                    ### Checking previous cases of the ASIN
                    def common_filter( _type_):
                        
                        last_valid_index = None
                        case_ID_ = self.Gsheet_Data_current_row['ID_'+_type_] if not _type_.startswith('Product_Stage') else self.Gsheet_Data_current_row[_type_]

                        if len(case_ID_) <=1:
                                
                            if not case_ID_.empty  and  case_ID_.values:
                                case_ID_ = int(case_ID_.iloc[0])
                                if isinstance(case_ID_, list):
                                    if case_ID_:
                                        case_ID_ = case_ID_[0]
                                    else:
                                        case_ID_ = None
                                elif isinstance(case_ID_, np.ndarray):
                                    case_ID_ = case_ID_.item(0) if case_ID_.size else None
                                else:
                                    case_ID_ = case_ID_
                                case_check = (self.all_cases_dataset['Product_Stage_ID'] == self.Stage_ID)  & (self.all_cases_dataset['Type'] == _type_ )  & ( self.all_cases_dataset['ID'] == case_ID_ ) 
                                column_series = self.all_cases_dataset[case_check]
                                last_valid_index = column_series.last_valid_index()
                                
                        else:
                            case_ID_ = [i for i in case_ID_.values if i]
                            if case_ID_:
                                
                                if isinstance(case_ID_, list):
                                    if case_ID_:
                                        case_ID_ = case_ID_[-1]
                                    else:
                                        case_ID_ = None
                                elif isinstance(case_ID_, np.ndarray):
                                    case_ID_ = case_ID_.item(0) if case_ID_.size else None
                                else:
                                    case_ID_ = case_ID_

                                case_ID_ = int(case_ID_)
                                case_check = (self.all_cases_dataset['Product_Stage_ID'] == self.Stage_ID)  & (self.all_cases_dataset['Type'] == _type_ )  & ( self.all_cases_dataset['ID'] == case_ID_ ) 
                                column_series = self.all_cases_dataset[case_check]
                                last_valid_index = column_series.last_valid_index()

                        
                        if last_valid_index is not None:
                            return column_series.loc[case_check]   ### column_series[case_check]
                        else:
                            case_ID_ = ''
                            return pd.DataFrame()
                    
                    latest_Seller_support_Case = ''
                    
                    SAS_IA_filter = common_filter('SAS-IA')
                    Lab_Report_SAS_Case_filter = common_filter('Lab_Report_SAS_Case')
                    SAS_IA_2_filter = common_filter('SAS-IA_2')
                    SAS_Manager_filter = common_filter('SAS_Manager')
                    
                    SAS_IA_data = SAS_IA_filter.values[0] if not SAS_IA_filter.empty else []
                    
                    Lab_Report_SAS_Case_data = Lab_Report_SAS_Case_filter.values[0] if not Lab_Report_SAS_Case_filter.empty else []
                    LAB_REPORT_check_status_of_email_subject  = Lab_Report_SAS_Case_filter.iloc[0, 6] if not Lab_Report_SAS_Case_filter.empty else ''
                    
                    SAS_IA_2_data = SAS_IA_2_filter.values[0] if not SAS_IA_2_filter.empty else []
                    SAS_Manager_Data = SAS_Manager_filter.values[0] if not SAS_Manager_filter.empty else []
                    

                    ### Check if Stage ID already exists - get the latest SS case and report abuse case IDs
                    Check_monitor_status =  self.Stage_ID in self.all_cases_dataset['Product_Stage_ID'].values
                    current_datetime = datetime.now()
                    if  Check_monitor_status :
                       
                        self.complaint_number = common_filter('Report_Abuse_Backend')['CaseID'].values
                        if self.complaint_number:
                            self.complaint_number = str(self.complaint_number[0]) 
                            try:
                                self.complaint_number = self.complaint_number.split('__')[1]
                            except: self.complaint_number = self.complaint_number
                        else:
                            if isinstance(self.complaint_number, np.ndarray): self.complaint_number  = ', '.join(self.complaint_number)
                        
                        latest_Seller_support_Case = common_filter('Seller_Support_Case')['CaseID'].values
                        if latest_Seller_support_Case:
                            latest_Seller_support_Case = str(latest_Seller_support_Case[0])
                        else: 
                            if isinstance(latest_Seller_support_Case, np.ndarray): latest_Seller_support_Case  = ', '.join(latest_Seller_support_Case)
                    ### else we set the new row for the ASIN
                    else:
                        print(f"Asin {self._ASIN} Stage ID  not found in earlier entries, created a new entry for the same")
                        self.post.ProcessErrorLog(self,1,f'Asin {self._ASIN} Stage ID not found in earlier entries, created a new entry in RPA job log for the same')
                        latest_Seller_support_Case = ''
                        self.complaint_number = ''

                    time_last_case_id = datetime.now()
                    time_difference = timedelta(seconds=1) 
                    
                    lab_report_sas_case_time = ''
                    self.post.ProcessErrorLog(self, 1, f'Working on Stage ID = {self.Stage_ID} of asin {self._ASIN} ')
                    print(f'Working on Stage ID = {self.Stage_ID}  of asin {self._ASIN}; can check it in Table public."DG_Product_All_Cases" where "Product_Stage_ID" = {self.Stage_ID}   ')

                    ### Get the Lab report path 
                    def file_found_path():
                      
                        ### Check Master Table -  if Lab_Report column  is marked True , We shift the file to the file_path
                        
                        file_found = False           
                        # if  lab_report_file_status :
                        #     if lab_report_file_status.lower().startswith('yes'):
                        #         self.post.ProcessErrorLog(self, 1, f' File status of asin {self._ASIN} is marked True, file is found - {str(lab_report_file_status)} ')
                        #         print(f'File status of asin {self._ASIN} is marked True, file is found - {str(lab_report_file_status)}  ')
                                
                                
                        #         self.post.ProcessErrorLog(self, 1, f'In master sheet, Lab report status is marked Yes, lets check for the file ');print(f'In master sheet, Lab report status is marked Yes, lets check for the file  ')

                        try:
                            if not os.path.exists(self.Lab_Reports_path):
                                os.makedirs(self.Lab_Reports_path)

                            _FileName = f"http://20.124.105.108/static/assets/media/DG_case/{self._ASIN}.pdf"
                            name_file =   f"DG Report-{brand}-{self._ASIN}-{Product}-{datetime.today().strftime('%Y-%m-%d')}.pdf"
                            time.sleep(0.5) 
                            file_found = urllib.request.urlretrieve(_FileName , os.path.join(self.Lab_Reports_path, name_file)  )
                            file_found = file_found[0]
                            self.post.ProcessErrorLog(self, 1, f'File Found !')
                            print(f'File Found ! {file_found} ')    
                            lab_report_file_status = 'yes'

                            time.sleep(5)
                            

                        except Exception as e: 
                            self.post.ProcessErrorLog(self, 1, f'Lab Report File not found for the asin {self._ASIN} | Error: {e}')
                            print(f'Lab Report File not found for the asin {self._ASIN} | Error: {e}')
                            return False

                            # else:
                            #     self.post.ProcessErrorLog(self, 1, f'File not Marked "Yes" in master sheet, Thus, Wont find it in drive ')
                            #     print(f'File not Marked "Yes" in master sheet, Thus, Wont find it in drive   ')
                            #     self.post.ProcessErrorLog(self, 1, f'Pushing the file to dangerous good category directory  ');print(f'Pushing the file to dangerous good category directory   ')
                        
                        if file_found:
                            self.post.ProcessErrorLog(self, 1, f'DG Lab Report File found for Asin {self._ASIN} '); print(f'DG Lab Report File found for Asin {self._ASIN} ')
                            ### sending the lab report file from Lab reports directory to images directory 
                            file_found = os.path.basename(file_found)
                            source_file_path = os.path.join(self.Lab_Reports_path, file_found)
                            destination_path = os.path.join(self.dangerous_good_directory_path, file_found)
                            shutil.copyfile(source_file_path, destination_path)
                            self.post.ProcessErrorLog(self, 1, f'Lab Report File shifted to Dangerous good folder'); print(f'Lab Report File shifted to Dangerous good folder')
                       
                            return self.dangerous_good_directory_path
                        
                        else:
                            self.post.ProcessErrorLog(self, 1, f'File not present in drive ');print(f'\nFile not present in drive  ')
                            return False
                    result_file_found_path = file_found_path()

                    ### if lab report not received, inform lizzy after 20 days
                    if not result_file_found_path and self.Gsheet_Data_current_row["Date"].values[0]  :
                        date_string = self.Gsheet_Data_current_row["Date"].values[0]
                        date_format = '%Y-%m-%d %H:%M'
                        date_object = datetime.strptime(date_string, date_format)
                        current_date = datetime.now()
                        total_days =  (current_date - date_object  ).days
                        # if total_days == 1 or  total_days > 20:
                        ### send mail on MONDAY
                        if datetime.now().weekday() == 0:
                            
                            print("The Lab report file is missing for more than 20 days. Informing Cong regarding the same.")
                            self.post.ProcessErrorLog(self, 1, f' The Lab report file is missing for more than 20 days. Informing Cong regarding the same. ')
                            self.missing_lab_reports.append(self._ASIN)
                            
                            
                            # continue

                    
                    if result_file_found_path:
                        data = {    
                            "Lab_Report": "Yes" , "Lab_Date": lab_date
                            }
                        ID__ =  self.insert_update_data_Stage_(data, Status = 1)
                        print('File locked in DB successfully.\n')
                    else:data = {    "Lab_Report": None , "Lab_Date": lab_date};ID__ =  self.insert_update_data_Stage_(data, Status = 1); print('ID__ of non lab report', ID__)
                    
                    self.gsheetData = self.readgooglesheet()

                    Updated_Subject_case_ID = ''
                    time_last_sas_sent = ''
                    time_difference = ''
                    Updated_case_id = ''

                    ### Check latest sas-ia trailing case id number and time, else denote as null
                    def check_status__(SAS_REPORT):
                        try:
                            global Updated_Subject_case_ID
                            global time_last_sas_sent
                            global time_difference
                            result = None
                            try:
                                Updated_Subject_case_ID = common_filter(SAS_REPORT  )['CaseID'].values
                                time_last_sas_sent = common_filter (SAS_REPORT  )['Date'].values
                            except:
                                Updated_Subject_case_ID = ''
                                time_last_sas_sent = ''  
                            ### Strip the time of the latest SAS CASE -  SENT 
                            if time_last_sas_sent:
                                time_last_sas_sent = datetime.strptime ( time_last_sas_sent[0] , '%Y-%m-%d %H:%M')  
                                time_difference = current_datetime -  time_last_sas_sent
                            if SAS_case_Email_subject:
                                Updated_case_id = SAS_case_Email_subject[0]
                            if Updated_Subject_case_ID:
                                Updated_Subject_case_ID = Updated_Subject_case_ID[0]
                            try:
                                int(Updated_Subject_case_ID)
                                is_number = True
                            except:
                                is_number = False
                            
                            ### if SAS case  was sent on FRIDAY, Increase the time period to 4 if saturday then 3
                            difference_of_days = 2
                            if time_last_sas_sent.weekday() == 4:
                                difference_of_days = 4 
                            if time_last_sas_sent.weekday() == 5:
                                difference_of_days = 3

                            ### (IF NO CASE ID NUMBER) - FIND FROM THE SUBJECT - Find CASE ID NUMBER and its current status 
                            if not is_number  and Updated_case_id and not Updated_Subject_case_ID:
                                Updated_case_id = self.update_case_id(self.Stage_ID, SAS_REPORT = SAS_REPORT )  if not SAS_REPORT.startswith('Lab') else self.update_lab_report_case_id(single_entry  = True)                 
                                if Updated_case_id == 'error' : return 'error'
                                if Updated_case_id:
                                    Updated_Subject_case_ID = Updated_case_id
                                    result = self.check_case_status_(Updated_case_id)
                                    if result == 'error':
                                        self.post.ProcessErrorLog(self, 1, f'Result of checking case status not confirmed, will check later in next run...  ')
                                        print(f'Result of checking case status not confirmed, will check later in next run...   ')
                                        return "error"
                                    self.post.ProcessErrorLog(self, 1, f'Result of case id is {self.case_status_} ')
                                    print(f'Result of case id is {self.case_status_}  '); return self.case_status_
                                else:
                                    
                                    ### (IF NO CASE ID NUMBER)  If Subject given and we dont get any CASE ID, wait for 2 days if not WEEKEND
                                    if not time_difference > timedelta(days = difference_of_days )  :
                                        self.case_status_ = True
                                        self.post.ProcessErrorLog(self, 1, f'No word from Amazon for the Subject yet, wait {difference_of_days} days...  {SAS_case_Email_subject[0]} ');print(f'No word from Amazon for the Subject yet, wait {difference_of_days} days...  {SAS_case_Email_subject[0]} ')
                                        self.post.ProcessErrorLog(self, 1, f'Current Status is On going for SAS {SAS_REPORT} ');print(f'Current Status is On going for SAS {SAS_REPORT} ')
                                        return self.case_status_
                                    
                                    else: 
                                        try:
                                           
                                            self.driver.get("https://sellercentral.amazon.com/cu/case-lobby?ref=xx_caselog_count_home")
                                            sleep(3)
                                            table = self.driver.find_element(by = By.XPATH, value='//*[@role="rowgroup"]')
                                            tablerows = table.find_elements(by = By.XPATH, value='//*[@role="row"]')
                                            searchcaseid = tablerows[0].find_element(by = By.XPATH, value='//*[@type="search"]')
                                            searchcaseid.send_keys(self._ASIN)
                                            sleep(2)
                                            searchbtn = tablerows[0].find_elements(by = By.XPATH, value='//*[@label="Go"]')
                                            searchbtn[0].click()
                                            sleep(2)
                                            self.driver.execute_script("document.body.style.zoom='60%'")

                                            self.post.ProcessErrorLog(self, 1, f'Creating the screenshot for the proof that SAS stage is closed with no reply from amazon.' )
                                            second_last_directory = os.path.dirname(os.path.normpath(self.dangerous_good_directory_path))
                                            today_date = datetime.now().strftime('%Y_%m_%d_%H_%M')
                                            image_stored_proof = os.path.join(second_last_directory, f'proof_{today_date}.png')
                                            self.driver.save_screenshot(image_stored_proof)
                                            self.post.ProcessErrorLog(self, 1, f'Stored proof of ss, which states, {self._ASIN} ASIN -  SAS CASE is closed  ');print(f'Stored proof of ss, which states, {self._ASIN} ASIN -  SAS CASE is closed  ')
                                        except Exception as e:
                                            self.post.ProcessErrorLog(self, 1, f'Couldn"t store the proof image, as issue in cliking image , error => {e}  ');print(f'Couldn"t store the proof image, as issue in cliking image , error => {e}  ')
                                            

                                        self.post.ProcessErrorLog(self, 1, f'Current Status is Closed for SAS {SAS_REPORT} - as no reply from AMAZON from past {difference_of_days} days ');print(f'Current Status is Closed for SAS - {SAS_REPORT},as no reply from AMAZON from past {difference_of_days} days ')
                                        failed_marked = self.create_update_data_PG_all_cases_table(caseType = SAS_REPORT,  CaseStatus = 'Failed', CaseID = 'Case ID not Found' ,  Status = 1 )
                                        self.post.ProcessErrorLog(self, 1, f'Stage is closed, failed marked status - {str(failed_marked)} ')
                                        print(f'Stage {SAS_REPORT} is closed, failed marked status - {str(failed_marked)} ')
                                        

                                        return False
                            
                            ### (IF CASE ID NUMBER) - FIND THE STATUS From CASE ID NUMBER
                            else: 
                                if Updated_Subject_case_ID:
                                    result = self.check_case_status_(Updated_Subject_case_ID)
                                    if result == 'error':
                                        self.post.ProcessErrorLog(self, 1, f'Result of checking case status not confirmed, will check later in next run...  ')
                                        print(f'Result of checking case status not confirmed, will check later in next run...   ')
                                        return "error"
                                    if result:
                                        print(f'Current Status is On going  for {SAS_REPORT}  for self.case_status_ \t =', self.case_status_)
                                        self.post.ProcessErrorLog(self, 1, f'Current Status is On going  for {SAS_REPORT} for case id is {self.case_status_} ')
                                        date_object = datetime.strptime(self.driver.find_elements(By.CLASS_NAME,'inline-contact')[-2].text.split('\n')[2], '%m/%d/%Y')
                                        current_date = datetime.now()
                                        if current_date - date_object > timedelta(days=14):
                                            self.SAS_Manager_asins_list[self._ASIN] = None
                                        return self.case_status_
                                    
                                    else: 
                                        ### (IF CASE ID NUMBER AND CASE IS CLOSED ) 
                                        if Updated_Subject_case_ID and not result:
                                            self.post.ProcessErrorLog(self, 1, f'Current Status is Closed for SAS {SAS_REPORT} ');print(f'Current Status is Closed for SAS {SAS_REPORT} ')
                                            return False
                                             
                        except:
                            return False


                    ### Checks the Latest trailing mail from SAS-IA 2, LAB REPORT SAS CASE, SAS-IA 1
                    threshold = timedelta(hours = self.Sas_create_time)
                    result_ = False
                    SAS_REPORT = ''
                    SAS_case_Email_subject = ''
                    self.Current_Stage = None
                    
                    ### check Stage 1 email SAS-IA sent
                    if  len(SAS_IA_data)>=1 :
                        SAS_REPORT = 'SAS-IA'
                        SAS_case_Email_subject = common_filter('SAS-IA' )['Subject'].values  if len(SAS_IA_data) >= 1 else None
                        result_of_check_status = check_status__(SAS_REPORT) if not SAS_case_Email_subject[0].startswith("Failed")  else None
                        if result_of_check_status == 'error':
                            continue
                        else:
                            if result_of_check_status:
                                self.Current_Stage = 1
                                self.SAS_REPORT = SAS_REPORT
                            else:
                                print(f"\tStage of {SAS_REPORT} is closed, Marked as Failed  ")

                    ### check Stage 2 email SAS-IA sent
                    if len(Lab_Report_SAS_Case_data)>=1  and not self.Current_Stage :
                        SAS_REPORT = 'Lab_Report_SAS_Case'
                        lab_report_sas_case_ID = common_filter('Lab_Report_SAS_Case' )['CaseID'].values
                        lab_report_sas_case_time = common_filter('Lab_Report_SAS_Case' )['Date'].values     
                        SAS_case_Email_subject = common_filter('Lab_Report_SAS_Case' )['Subject'].values
                        result_of_check_status = check_status__(SAS_REPORT) if not SAS_case_Email_subject[0].startswith("Failed")  else None
                        if result_of_check_status == 'error':
                            continue
                        else:
                            if result_of_check_status:
                                self.Current_Stage = 2
                                self.SAS_REPORT = SAS_REPORT
                            else:
                                print(f"\tStage of {SAS_REPORT} is closed, Marked as Failed  ")
                    
                    ### check Stage 3 email SAS-IA sent
                    if len(SAS_IA_2_data)>=1 and not self.Current_Stage:
                        SAS_REPORT = 'SAS-IA_2'
                        SAS_case_Email_subject =  common_filter('SAS-IA_2' )['Subject'].values 
                        result_of_check_status = check_status__(SAS_REPORT) if not SAS_case_Email_subject[0].startswith("Failed")  else None
                        if result_of_check_status == 'error':
                            continue
                        else:
                            if result_of_check_status:
                                self.Current_Stage = 3
                                self.SAS_REPORT = SAS_REPORT
                            else:
                                print(f"\tStage of {SAS_REPORT} is closed, Marked as Failed  ")


                    ### conclude the report which Stage SAS-IA sent !
                    self.SAS_REPORT = SAS_REPORT
                    self.gsheetData = self.readgooglesheet()
                    Updated_case_id = ''
                    _Subject_case_ID = ''

                    if self._ASIN in self.SAS_Manager_asins_list and self.case_status_ and self.complaint_number and latest_Seller_support_Case :
                        
                        case_id_number = [i for i in self.driver.find_elements(By.CLASS_NAME,'text-secondary') if i.text]
                        if case_id_number:
                            case_id_number = case_id_number[0].text.split('ID')[1].strip()
                            self.SAS_Manager_asins_list[self._ASIN] =[self.complaint_number, latest_Seller_support_Case, case_id_number ]
                            self.post.ProcessErrorLog(self, 1, f'Added ASIN to SAS manager MAIL  ');print(f'Added ASIN to SAS manager MAIL  ')
                    
                    else:
                        self.post.ProcessErrorLog(self, 1, f'ASINs not exceeding threshold to be sent for SAS MANAGER  ')
                        print(f'ASINs not exceeding threshold to be sent for SAS MANAGER  ')

                    
                    if not Updated_Subject_case_ID or time_last_sas_sent:
                        try:
                            Updated_Subject_case_ID = common_filter(self.SAS_REPORT  )['CaseID'].values
                            time_last_sas_sent = common_filter (self.SAS_REPORT  )['Date'].values
                            Updated_case_id = Updated_Subject_case_ID
                        except:
                            Updated_Subject_case_ID = ''
                            time_last_sas_sent = '' 

                    if time_last_sas_sent:
                        time_last_sas_sent = datetime.strptime ( time_last_sas_sent[0] , '%Y-%m-%d %H:%M')  
                        time_difference = current_datetime -  time_last_sas_sent
                    
                    else:
                        time_difference = timedelta(seconds=1)  
                    
                    ### Update the Reply content Body
                    if Updated_Subject_case_ID : 
                        _Subject_case_ID = Updated_Subject_case_ID[0]                
                   
                    if self.Current_Stage and self.SAS_REPORT and self.case_status_ and _Subject_case_ID: 
                        print("Updating the Reply and Mail content Body...")
                        self.driver.get(f"https://sellercentral.amazon.com/cu/case-dashboard/view-case?ref=sc_cd_lobby_vc_v3&ie=UTF&caseID={_Subject_case_ID}")
                        time.sleep(5)
                        
                        ### Updating Latest text in Reply content column
                        latest_text = None
                        try:
                            latest_text = self.driver.find_elements(By.CLASS_NAME, 'inline-contact')[0].find_elements(By.CLASS_NAME, "contact-content")
                            if latest_text: latest_text = latest_text[0]
                            latest_text = latest_text.text.split('==========')[0]
                        except:
                            print('No content found')
                        
                        try: 
                            result_chat_gpt_output = self.chat_gpt_output(latest_text)
                            mail_content = result_chat_gpt_output
                            
                            def send_revert_to_amazon():
                                try:
                                    ### click reply button
                                    try:
                                        self.driver.find_elements(By.XPATH,'//kat-button[@label="Reply"]')[0].click()
                                    except:
                                        reply_btn = 'document.querySelector("#replyCase > div > div > kat-button:nth-child(1)").click()'
                                        self.driver.execute_script(reply_btn)
                                    
                                    time.sleep(3)


                                    ### send text in the input text box
                                    try:
                                        self.driver.find_elements(By.CLASS_NAME, 'hill-text-area')[0].send_keys(text_input_box)
                                    except:
                                        txt_area = f'document.querySelector("#replyCase > div > div > form > div > div > kat-tabs > kat-tab > kat-box > div > div.hill-primary-input-container > div > kat-textarea").value = "{text_input_box}"'
                                        self.driver.execute_script(txt_area)
                                    
                                    time.sleep(3)
                                    
                                    ### send button clicked
                                    try:
                                        btn = self.driver.find_elements(By.ID,'reply-email-button')[0]
                                        if btn.is_enabled():
                                            btn.click()
                                        else:
                                            send_btn = self.driver.find_elements(By.ID,'hill-submit-button')[0]
                                            if send_btn.is_enabled():
                                                send_btn.click()
                                    except: 
                                        self.post.ProcessErrorLog(self, 1, f' send button not clickable ... ');print(f' send button not clickable ...  ')
                                        return False
                                        
                                    return True
                                except:
                                    self.post.ProcessErrorLog(self, 1, f'Issue in sending the revert to amazon, after confirmation   ')
                                    print(f'Issue in sending the revert to amazon, after confirmation   ')
                                    return False


                            ### Updating DB with both the content 
                            data = { "Reply_Content": latest_text , 
                                    "Mail_Content": mail_content}
                            r = self.insert_update_data_Stage_(data, Status = 1 )
                            self.post.ProcessErrorLog(self, 1, f'Reply Content & Mail Content Updated for ASIN, {r} ')
                            print(f'Reply Content & Mail Content Updated for ASIN, {r} ')
                            confirmation_ = self.Gsheet_Data_current_row['Confirmation'].iloc[0]
                            if confirmation_ and latest_text and mail_content: 
                                result_of_revert = send_revert_to_amazon()
                                if result_of_revert:
                                    self.post.ProcessErrorLog(self, 1, f'Reverted to amazon with confirmation text  ');print(f'Reverted to amazon with confirmation text ')
                            else:
                                self.post.ProcessErrorLog(self, 1, f"Reply content - {str(bool(latest_text))}| Mail Content - {str(bool(mail_content))} | Confirmation - {str(bool(confirmation_))}  ")
                                print(f"Reply content - {str(bool(latest_text))}| Mail Content - {str(bool(mail_content))} | Confirmation - {str(bool(confirmation_))}  ")
                        except: 
                            self.post.ProcessErrorLog(self, 1, f'Issue in confirmation column, updating both the content text - check reply content body   ')
                            print(f'Issue in confirmation column, updating both the content text - check reply content body   ')

                    print('Current Stage of the ASIN is ', self.Current_Stage)
                    self.post.ProcessErrorLog(self, 1, f'  Current Stage of the ASIN is  {self.Current_Stage} ')
                    
     
                    ### Confirmed that product is DG from our end
                    self.dangerous_good[self._ASIN] = True
                    Stage_1_email = None; Stage_2_email = None; Stage_3_email = None

                    ### SAS - IA Stage 1  Continued ...  Stage 2 SAS-IA  - if   is On going...
                    if self.Current_Stage == 1 and result_file_found_path and self.case_status_ and  len(Lab_Report_SAS_Case_data)<1 and len(SAS_IA_2_data)<1  :
                        try:
                            filename = os.path.basename(result_file_found_path)
                            file = [i for i in os.listdir(result_file_found_path) if i.endswith('.pdf')][0]
                            see_more_buttons = [self.driver.find_elements(By.CLASS_NAME, 'link')[-1]]
                            for button in see_more_buttons:
                                try:
                                    if button.text.split('\n')[1].endswith('more'):
                                        self.driver.execute_script("arguments[0].click();", button)
                                    time.sleep(2)
                                except Exception as e:
                                    print(f"Error clicking 'See More' button: {e}")
                            time.sleep(3)
                        

                            
                            if file.split(self._ASIN)[0] in self.driver.page_source and '.pdf' in self.driver.page_source:
                                
                                self.post.ProcessErrorLog(self, 1, f'PDF file already sent in Stage 1'  )
                                print(f'PDF file already sent in Stage 1  ')
                            
                            else:

                                text_input_box = """
We look forward to hearing from you shortly. Please take note the lab report shows that the product has a flash point of 50C and is classified as a
Flammable Liquid.
This is a Flammable DG product.
Test report confirming the product is flammable - Is Attached
Thanks
Alex"""
                                add_attn_file_path = result_file_found_path

                                ### click reply button
                                try:
                                    self.driver.find_elements(By.XPATH,'//kat-button[@label="Reply"]')[0].click()
                                except:
                                    reply_btn = 'document.querySelector("#replyCase > div > div > kat-button:nth-child(1)").click()'
                                    self.driver.execute_script(reply_btn)
                                
                                time.sleep(3)


                                ### send text in the input text box
                                try:
                                    self.driver.find_elements(By.CLASS_NAME, 'hill-text-area')[0].send_keys(text_input_box)
                                except:
                                    txt_area = f'document.querySelector("#replyCase > div > div > form > div > div > kat-tabs > kat-tab > kat-box > div > div.hill-primary-input-container > div > kat-textarea").value = "{text_input_box}"'
                                    self.driver.execute_script(txt_area)
                                time.sleep(3)


                                ### add attachments
                                add_attachments_btn = 'return document.querySelector("#replyCase > div > div > form > div > div > kat-tabs > kat-tab > kat-box > div > div.hill-attachments-input-container > div.hill-attachments-input-container > div > input[type=file]");'
                                result = self.driver.execute_script(add_attachments_btn)
                                self.driver.execute_script("arguments[0].style.display = 'block';", result)
                                result.send_keys( add_attn_file_path )
                                self.driver.execute_script("arguments[0].style.display = 'none';", result)
                                
                                ### send button clicked
                                try:
                                    btn = self.driver.find_elements(By.ID,'reply-email-button')[0]
                                    if btn.is_enabled():
                                        btn.click()
                                    else:
                                        send_btn = self.driver.find_elements(By.ID,'hill-submit-button')[0]
                                        if send_btn.is_enabled():
                                            send_btn.click()
                                except: 
                                    self.post.ProcessErrorLog(self, 1, f' send button not clickable ... ');print(f' send button not clickable ...  ')
                                    continue
                        except:
                                continue
                    
                    ### Generate Backend reports  - REPORT ABUSE
                    subject_fail_condition_check_RA = False if self.complaint_number.startswith("Failed") else self.complaint_number
                    result_backend_abuse_ = None
                    if  self.dangerous_good  and not subject_fail_condition_check_RA :
                    
                        print(f'\nDangerous Good asin {self._ASIN} Found, with no previous last case id {self.Stage_ID} Started with Reporting them...')
                        self.post.ProcessErrorLog(self, 1, f' Dangerous Good asin {self._ASIN} Found, with no previous last case id {self.Stage_ID} Started with Reporting them ')

                        self.post.ProcessErrorLog(self, 1, 'Immediately Starting with Reporting Issue Backend ')
                        print('Immediately Starting with Reporting Issue Backend')
                        subject = f'DG Violation - {brand} - {self._ASIN} - Classify Flammable - {datetime.today().strftime("%Y-%m-%d")} - RA'
                        result_backend_abuse_ = self.reporting_issue_backend(subject); time.sleep(5)
                        
                        if result_backend_abuse_:    
                            print("Started with reading gmail account for the complaint number")
                            self.post.ProcessErrorLog(self, 1, ' Started with reading gmail account for the complaint number ')
                            
                            """ 
                                While loop where it will keep running the function 
                                after 1 min for total 10 minutes , 
                                until it gets the output 
                            """
                            
                            start_time = time.time()
                            while not self.complaint_number :
                                if time.time() - start_time > 600: # Check if 10 minutes have elapsed
                                    break
                                ## just from the subject, read the gmail body
                                body = self.read_gmail_account('Your Report of Policy Violation')
                                ### GET the Complaint Number from the body
                                lines = body.split('\n')
                                latest_complaint_id = None
                                preceding_text = ""

                                for line in lines:
                                    if "Complaint ID:" in line:
                                        if latest_complaint_id is None:
                                            latest_complaint_id = line.split(':')[1].strip()
                                        else:
                                            preceding_text += line + '\n'
                                print("Latest Complaint ID:", latest_complaint_id )
                                try:
                                    self.complaint_number = latest_complaint_id.split(':')[0]
                                except:
                                    self.complaint_number = latest_complaint_id
                          
                                ### check all the previous complaint number, we make sure we send the previous one !
                                report_abuse_backend_values = self.all_cases_dataset[self.all_cases_dataset['Type'] == 'Report_Abuse_Backend']['CaseID'].values
                                if self.complaint_number in [i for i in report_abuse_backend_values if i]:
                                        print("Already Have this complaint number, lets wait for the New one")
                                        self.post.ProcessErrorLog(self, 1, f"Already Have this complaint number stored for previous Asin, lets wait for the New one")
                                        self.post.ProcessErrorLog(self, 1, f"Amazon said it couldnt find violation on this scenerio, searching  in Submission mail now ")
                                        
                                        body = self.read_gmail_account('Thank you for your submission.')
                                        ### GET the Complaint Number from the body
                                        lines = body.split('\n')
                                        latest_complaint_id = None
                                        preceding_text = ""

                                        for line in lines:
                                            if "Complaint ID:" in line:
                                                if latest_complaint_id is None:
                                                    latest_complaint_id = line.split(':')[1].strip()
                                                else:
                                                    preceding_text += line + '\n'
                                        print("Latest Complaint ID:", latest_complaint_id, '-->' )
                                        try:
                                            self.complaint_number = latest_complaint_id.split(':')[0]
                                        except:
                                            self.complaint_number = latest_complaint_id
                                        if self.complaint_number in [i for i in report_abuse_backend_values if i]:
                                            self.complaint_number = None

                                print("Complaint Number is Unique for this ASIN ==  proceeding to store it - ", self.complaint_number);self.post.ProcessErrorLog(self, 1, f'Complaint Number is Unique for this ASIN ==  proceeding to store it -  {self.complaint_number} ')
                                time.sleep(60)
                            
                            if self.complaint_number :
                                print("Complaint number:", self.complaint_number)
                                self.post.ProcessErrorLog(self, 1, f"Latest Complaint ID: {self.complaint_number} FOR ASIN {self._ASIN}")
                               
                                self.create_update_data_PG_all_cases_table(caseType = "Report_Abuse_Backend", CaseID = self.complaint_number , Subject = subject, CaseStatus = 'Completed',  Date = datetime.now().strftime('%Y-%m-%d %H:%M') )
                            else:
                                self.post.ProcessErrorLog(self, 1, "No new complaint number found in 10 minutes, Issue in Report Backend ") 
                                self.create_update_data_PG_all_cases_table(caseType = "Report_Abuse_Backend", CaseID = f"Failed , Couldn't sent the complaint number" , Subject = subject, Date = datetime.now().strftime('%Y-%m-%d %H:%M') , CaseStatus = 'Failed' )
                                row['Status']=1; row['Process_Log']= '' ; self.updateRPAProcessLog(row)
                                continue
                        
                            
                     
                        else:
                            self._ManualLog = 'Complaint number not generated Successfully- BACKEND Report ISSUE__'

                        ###   FRONTEND REPORT  ###
                        # self.post.ProcessErrorLog(self, 1, 'Updated the Report Abuse Backend. Now, Started with Reporting Issue Frontend ')
                        # print('Immediately Started with Reporting Issue Frontend')
                        # result_front_end_report =  self.front_end_asin_report(self._ASIN)
                        # result_front_end_report = True
                        # if result_front_end_report:
                        #     Report_Abuse_Status_frontend = self.gsheetData_job_log.columns.get_loc('Report Abuse FrontEnd') + 1
                        #     cellsASIN.append(Cell(row= index+2 , col = Report_Abuse_Status_frontend  , value =  f'Reported Abused_Frontend_Reported__' + datetime.today().strftime('%Y-%m-%d %H:%M') ))
                        # else:
                        #     Report_Abuse_Status_frontend = self.gsheetData_job_log.columns.get_loc('Report Abuse FrontEnd') + 1
                        #     cellsASIN.append(Cell(row= index+2 , col = Report_Abuse_Status_frontend  , value =  f'FAILED'  ))
                    
                    ### Seller Support - SS Case if Backend created 
                    subject_fail_condition_check_SS = False if latest_Seller_support_Case.startswith("Failed") else latest_Seller_support_Case
                    try:
                        if  result_backend_abuse_ and not subject_fail_condition_check_SS:
                            
                            ### generate images
                            if not self.result_classification_product:
                                result_classification_product = click_images() 
                                self.result_classification_product = result_classification_product

                            self.post.ProcessErrorLog(self, 1, 'Immediately Started with Seller Support Case ')
                            print('Immediately Started with Seller Support Case')
                            if self.result_classification_product:
                                all_child_asins = self._ASIN
                                subject = f'DG Violation - {brand} - {self._ASIN} - Classify Flammable - {datetime.today().strftime("%Y-%m-%d")} - SS'
                                images_files_only_directory = [os.path.join(result_classification_product, image_file) for image_file in os.listdir(result_classification_product) if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                                new_directory_path = os.path.join(result_classification_product, 'images_only');os.makedirs(new_directory_path, exist_ok=True)
                                [  shutil.copy(file, new_directory_path) for file in images_files_only_directory ]
                                seller_support_case_id = self.seller_support_case(self._ASIN, new_directory_path, all_child_asins, subject = subject )   

                                self.create_update_data_PG_all_cases_table(caseType = "Seller_Support_Case", Date = datetime.now().strftime('%Y-%m-%d %H:%M'), CaseID = seller_support_case_id , Subject = subject, CaseStatus = 'Completed' if seller_support_case_id else 'On Going' )
                                latest_Seller_support_Case = seller_support_case_id
                            else:
                                self.post.ProcessErrorLog(self, 1, 'Issue in clicking images, will proceed next time for the seller support...')
                            
                    except Exception as err:
                        self.post.ProcessErrorLog(self, 1, f' Issue in Seller Support, {str(err)} ')
                        self.create_update_data_PG_all_cases_table(caseType = "Seller_Support_Case", Date = datetime.now().strftime('%Y-%m-%d %H:%M'), CaseID = "Failed" , Subject = subject, CaseStatus =  "Failed" )
                        self.post.ProcessErrorLog(self, 1, 'Seller support Case not generated -Issue-')
                    
                    ### STAGE 1 -- SAS - IA 1 -- if Backend and Seller Support Cases created 
                    check_status_of_email_subject = ''
                    if  SAS_case_Email_subject:
                        if isinstance(SAS_case_Email_subject, np.ndarray): check_status_of_email_subject  = ', '.join(SAS_case_Email_subject)
                    else: check_status_of_email_subject  = SAS_case_Email_subject
                    
                    subject_fail_condition_check_IA = False if  check_status_of_email_subject.startswith("Failed") else check_status_of_email_subject
                    

                    if  self.complaint_number   and  not result_  and  self.complaint_number  and latest_Seller_support_Case and not SAS_case_Email_subject and datetime.now().weekday() <=7 and not self.reopen_case and not subject_fail_condition_check_IA  and not result_file_found_path :
                        
                        brand = self.gsheetData[ (self.gsheetData['ASIN'] )== self._ASIN    ]['Brand'].values[0]
                        self.post.ProcessErrorLog(self, 1, 'Immediately Creating SAS for the same. ')
                        try:
                            excel_file_path = self.update_form_content(self._ASIN, self.complaint_number, latest_Seller_support_Case  )
                            
                            if not self.result_classification_product:
                                result_classification_product = click_images()
                                self.result_classification_product = result_classification_product
                            
                            if excel_file_path and result_classification_product:
                                file_path  = result_classification_product
                                subject = f'DG Violation - {"1" if not result_file_found_path else "2"} - {brand} - {self._ASIN} - Classify Flammable - {datetime.today().strftime("%Y-%m-%d")} - IA'
                                result_of_email = self.send_email_SAS(self._ASIN, subject, file_path = file_path, report_abuse_case_id = self.complaint_number, 
                                                    seller_support_case_id = latest_Seller_support_Case, lab_report_status = False)
                                
                                time.sleep(1.5) 
                                if result_of_email:   
                                    Stage_1_email = True
                                    self.create_update_data_PG_all_cases_table(caseType = "SAS-IA", CaseID = "" , Date = datetime.now().strftime('%Y-%m-%d %H:%M'), Subject = subject, CaseStatus =  "On-Going" )
                                    
                                    print(f'Created and sent the SAS Case as for the latest ASIN {self._ASIN} !! ')
                                    self.post.ProcessErrorLog(self, 1, f"Created and sent the SAS Case as for the latest ASIN {self._ASIN} !! ")  
                                else:
                                    print(f'Issue in Creating the Email for the SAS Case - the latest ASIN {self._ASIN} !! ')
                                    self.post.ProcessErrorLog(self, 1, f"Issue in Creating the Email for the SAS Case - the latest ASIN {self._ASIN} !! ")  

                                    self.create_update_data_PG_all_cases_table(caseType = "SAS-IA", CaseID = "" , Date = datetime.now().strftime('%Y-%m-%d %H:%M'), Subject = "Failed", CaseStatus =  "Failed" )
                                    
                            else:
                                self.post.ProcessErrorLog(self, 1, f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path !! ")  
                        
                        except Exception as e:
                            self.post.ProcessErrorLog(self, 1, f"Issue in Sending SAS for asin {self._ASIN} !! - {e} ")   
                            print(f"Issue in Sending SAS for asin {self._ASIN} !! - {e} ")
                    
                    else:
                        print(f"\nASIN {self._ASIN} \n| complaint number = {self.complaint_number} \n| latest_Seller_support_Case = {latest_Seller_support_Case } \n| Email subject = {str(SAS_case_Email_subject)} for SAS REPORT - {str(SAS_REPORT)}  \n| Email Case ID = {Updated_Subject_case_ID} Mentioned    ")
                        self.post.ProcessErrorLog(self, 1, f"ASIN {self._ASIN} | complaint number = {self.complaint_number} | latest_Seller_support_Case = {latest_Seller_support_Case } | Email subject = {str(SAS_case_Email_subject)} for SAS REPORT - {str(SAS_REPORT)}  | Email Case ID = {Updated_Subject_case_ID}   Mentioned ")
                    
                    
                    ### STAGE 2 -- SAS - IA 2 -- Lab Report SAS Case Creation if previous case cancelled
                    ### if subject of Lab case = "Failed", Lab status is failed , re send email, else any subject is present, continue ahead
                    subject_fail_condition_check_IA_Lab = False if  LAB_REPORT_check_status_of_email_subject.startswith("Failed") else LAB_REPORT_check_status_of_email_subject
                    if self.complaint_number  and result_file_found_path and datetime.now().weekday() <=7 and not self.case_status_ and not Stage_1_email and not subject_fail_condition_check_IA_Lab  :
                        
                        if not self.result_classification_product:
                            result_classification_product = click_images()
                            self.result_classification_product = result_classification_product
                            
                  
                        if result_file_found_path and result_classification_product:

                            file_path = result_classification_product
                            self.post.ProcessErrorLog(self, 1, f"File of lab report found, Initiating with Lab Report SAS Case ")
                            
                            ### Read amazon reply for our subject for sending the EMAIL - SAS
                            sas_email_subject_number = ''
                            try:
                                sas_email_subject_number = int(Updated_Subject_case_ID[0])
                                is_number = True
                            except :
                                is_number = False
                            if not is_number and sas_email_subject_number:
                                SAS_case_Email_subject = str(SAS_case_Email_subject[0])
                                subject = SAS_case_Email_subject
                                sas_email_subject_number = self.update_lab_report_case_id(single_entry= True ) 
                                
                            if sas_email_subject_number:
                                self.check_case_status_(sas_email_subject_number)

                            if not sas_email_subject_number: sas_email_subject_number = ''

                            excel_file_path = self.update_form_content(self._ASIN, self.complaint_number, latest_Seller_support_Case, sas_email_subject_number  )
                            self.post.ProcessErrorLog(self, 1, f"Excel file {excel_file_path} sent to Dangerous good directory ")
                            
                            if excel_file_path:

                                try:
                                    subject = f'DG Violation - 2 - {brand} - {self._ASIN} - Classify Flammable - {datetime.today().strftime("%Y-%m-%d")} - IA'
                                    result_of_email_send = self.send_email_SAS(self._ASIN, subject, file_path = file_path, report_abuse_case_id = self.complaint_number, 
                                                        seller_support_case_id = latest_Seller_support_Case, lab_report_status = True, email_case_id = sas_email_subject_number )
                                    time.sleep(1.5)    
                                    
                                    if result_of_email_send:
                                        result__= self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = '', Subject = subject, CaseStatus = 'On Going', Date = datetime.now().strftime('%Y-%m-%d %H:%M') )
                                        print('result of lab report case locked', result__)
                                        print(f'Created and sent the SAS Case as for the latest ASIN {self._ASIN} !! ')
                                        self.post.ProcessErrorLog(self, 1, f' Will proceed to move ahead for giving lab report case  ')
                                    else:
                                        self.post.ProcessErrorLog(self, 1, f'Issue in sending Email for ASIN {self._ASIN}   ')
                                        print(f'Issue in sending Email  ASIN {self._ASIN}  ')
                                        self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = '', Subject = subject, CaseStatus = 'Failed' , Date = datetime.now().strftime('%Y-%m-%d %H:%M'))
                                except Exception as err:
                                    self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = '', Subject = "Failed , Couldn't sent the SAS", CaseStatus = 'Failed' , Date = datetime.now().strftime('%Y-%m-%d %H:%M'))
                                    self.post.ProcessErrorLog(self, 1, f'Issue in sending Lab report, {str(err)}  ')
                                    print(f'Issue in sending Lab report   ')

                                self.Update_Master_sheet(lab_report_columns = lab_report_columns)
                                row['Status']=1
                                row['Process_Log']= '' 
                                self.updateRPAProcessLog(row)
                                continue
                            else:
                                self.post.ProcessErrorLog(self, 1, f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path !! ")  
                            
                    ### Re-OPEN Case for STAGE 2 SAS-IA       STAGE 2 Reponed with STAGE 3 included   
                    threshold = timedelta(hours = self.Sas_create_time)

                    condition_of_timing = time_difference > threshold
                    if not self.case_status_ and not condition_of_timing : 
                        condition_of_timing = True


                    if not self.case_status_ and SAS_case_Email_subject and result_file_found_path  and datetime.now().weekday() <=7  and condition_of_timing :
                        
                        self.post.ProcessErrorLog(self, 1, 'Time difference Exceeded Threshold of 24 hours from the previous SAS,  Again Creating SAS for the same. ')
                        print('Time difference Exceeded Threshold of 24 hours from the previous SAS,  Again Creating SAS for the same.')
                        
                        if not self.result_classification_product:
                            result_classification_product = click_images()
                            self.result_classification_product = result_classification_product
                             
                        if not Updated_case_id and len(SAS_IA_data)>=1 : Updated_case_id = SAS_IA_data[-2] if SAS_IA_data[-2] else SAS_IA_2_data[-2]
                        if isinstance(Updated_case_id, np.ndarray):
                            Updated_case_id = ', '.join(Updated_case_id.astype(str))
                            if Updated_case_id == 'Case ID not Found':
                               Updated_case_id = ''
                        try:
                            excel_file_path = self.update_form_content(self._ASIN, self.complaint_number, latest_Seller_support_Case, SAS_IA_case_number = Updated_case_id   )
                            if excel_file_path and result_classification_product: 
                                file_path  = result_classification_product
                                subject = f'DG Violation - 2 - {brand} - {self._ASIN} - Classify Flammable - {datetime.today().strftime("%Y-%m-%d")} - IA'
                                self.send_email_SAS(self._ASIN, subject, file_path = file_path, report_abuse_case_id = self.complaint_number, 
                                                    seller_support_case_id = latest_Seller_support_Case, email_case_id = Updated_case_id,  lab_report_status = False)
                                time.sleep(1.5)    
                                print(f'Created and sent the SAS Case AGAIN as for the latest ASIN {self._ASIN} !! ')
                                
                                self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = '', Subject = subject, Date = datetime.now().strftime('%Y-%m-%d %H:%M') , CaseStatus = 'On Going' )

                            else:
                                self.post.ProcessErrorLog(self, 1, f"Issue in creating form for asin {self._ASIN}, will retry again, check method excel_file_path !! ")  
                                self.create_update_data_PG_all_cases_table(caseType = "Lab_Report_SAS_Case", CaseID = "Failed, Couldn't sent the SAS", Subject = subject, Date = datetime.now().strftime('%Y-%m-%d %H:%M') , CaseStatus = 'Failed' )

                        except Exception as e:
                            self.post.ProcessErrorLog(self, 1, f"Issue in Sending SAS for asin {self._ASIN} !! - {e} ")   
                            print(f"Issue in Sending SAS for asin {self._ASIN} !! - {e} ")
                            self._ManualLog = 'SAS-IA failed'              
                    else:
                        print(f"ASIN {self._ASIN} Not Found to exceeding Threshold timelimit for SAS to be sent Again ! ")
                        self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} Not Found to exceeding Threshold timelimit for SAS to be sent Again ! ')

                    self.post.ProcessErrorLog(self, 1, f"RPA Job LOG Sheet updated for ASIN {self._ASIN}  ")
                    print(f'RPA Job LOG Sheet updated for ASIN {self._ASIN} ')
                    self.Update_Master_sheet(lab_report_columns = lab_report_columns)
                    time.sleep(2)
                    row['Status'] = 1
                    row['Process_Log']= '' 
                    self.updateRPAProcessLog(row)
                    print("Complete", self._ASIN) 
                    print('\n\nCurrent cases of this asin\n', self.all_cases_dataset[self.all_cases_dataset['Product_Stage_ID'] == self.Stage_ID].values)
                
                except Exception as err: 
                
                    print("Exception  ", self._ASIN, str(err)) 
                    time.sleep(2)
                    row['Status']=2
                    row['Process_Log']= str(err)
                    self.updateRPAProcessLog(row)   
                    self.post.ProcessErrorLog(self, 1, "Exception " + self._ASIN +' ' + str(err) )
                    self._ManualLog = "ERROR" + str(err)
                    country_list=['US']
           


            print(f'Managerer list  {str(self.SAS_Manager_asins_list)}')
            self.post.ProcessErrorLog(self, 1, f' Managerer list  {str(self.SAS_Manager_asins_list)} ')
            

            
            def SAS_manager_template():
                try:
                    new_template = f"{self.DownloadLocation}DG Violation - SAS Manager - ASIN Email Format.xlsx"
                    wb_source_new_template = xw.Book(new_template)
                    sheet = wb_source_new_template.sheets['Sheet1']  

                    column_names = ['Sr. NO', 'ASIN', 'Report Abuse', 'Seller Support', 'SAS-IA']
                    row_index = 2                         
                    for i, (asin, values) in enumerate(self.SAS_Manager_asins_list.items()):
                        sheet.range(f'A{row_index}').value = [i + 1, asin] + values
                        row_index += 1
                    excel_updated_path = f'{self.dangerous_good_directory_path}\\SAS_Manager_data_{ datetime.today().strftime("%Y-%m-%d") }.xlsx'
                    wb_source_new_template.save(excel_updated_path)
                    wb_source_new_template.app.quit()
                    return excel_updated_path    
                except:
                    return False

            
            
            ### STAGE 3 -- SAS - IA 3 -- After 7 days - Send to SAS Manager with SAS IA if previous case cancelled
            
            if self.SAS_Manager_asins_list:
                count = len(list(set(self.SAS_Manager_asins_list)))
                try:
                    excel_file_path = SAS_manager_template()

                    if excel_file_path:
                        subject = f'SAS Manager - Sub - {count}  ASINs Resolution Not Found by SAS-IA - { datetime.today().strftime("%Y-%m-%d") }'
                        result_of_email = self.send_email_SAS(self._ASIN, subject, file = excel_file_path, report_abuse_case_id = self.complaint_number, 
                                                        seller_support_case_id = latest_Seller_support_Case, sas_manager = True)
                        
                        for asin in self.SAS_Manager_asins_list:
                            self.Stage_ID = self.gsheetData[(self.gsheetData['ASIN'] == asin) ]['Stage_ID'].iloc[0]
                            
                            if result_of_email:
                                result__ = self.create_update_data_PG_all_cases_table(caseType = "SAS_Manager", asin = asin,  CaseID = '', Subject = subject, Date = datetime.now().strftime('%Y-%m-%d %H:%M') ,CaseStatus = 'On Going'  )
                                time.sleep(1.5)    
                                print(f'Created and sent the mail for SAS manager  for the latest ASIN {self._ASIN} with result {str(result__)} ')
                                self.post.ProcessErrorLog(self, 1,f'Created and sent the mail for SAS manager  for the latest ASIN {self._ASIN} with result {str(result__)} ')
                            else:
                                print(f"Issue in Sending SAS for SAS manager {self._ASIN} !!  ")
                                self.post.ProcessErrorLog(self, 1,f'Issue in Sending SAS for SAS manager {self._ASIN} !! ')
                                self.create_update_data_PG_all_cases_table(caseType = "SAS_Manager", asin = asin,  CaseID = '', Subject = subject, Date = datetime.now().strftime('%Y-%m-%d %H:%M') ,CaseStatus = "Failed SAS_Manager"  )

                    else:
                        self.post.ProcessErrorLog(self, 1, f"Issue in Creating Excel file path for SAS MANAGER  - {e} ")  
                                
                except Exception as e:
                    self.post.ProcessErrorLog(self, 1, f"Issue in Sending SAS for for SAS with MANAGER  - {e} ")  
            else:
                self.post.ProcessErrorLog(self, 1, f'No ASINs crossed threshold time period - to be sent to SAS-Manager  ');print(f'No ASINs crossed threshold time period - to be sent to SAS-Manager  ')
          
            
#             def follow_up_mails():
                
#                 self.readgooglesheet()
#                 text = None
#                 text_no_change = """
# Hi Andres,\n
# Thank you for your co-operation on the follow up.\n
# Would appreciate, if you can please look into this\n\n
# thanks,
# Rebecca"""
#                 # follow_up_mails = self.all_cases_dataset[
#                 #     (self.all_cases_dataset["Type"] == 'SAS_Manager') &
#                 #     (self.all_cases_dataset['Subject'].str.startswith('SAS Manager'))
#                 # ][["ID", 'Date', "Subject"]]
#                 follow_up_mails = self.all_cases_dataset[self.all_cases_dataset['Subject'].duplicated(keep=False) &
#                                                  (self.all_cases_dataset["Type"] == 'SAS_Manager') &
#                                                  (self.all_cases_dataset['Subject'].str.startswith('SAS Manager'))
#                                                ][["ID", 'Date', "Subject"]]

#                 ### self.all_cases_dataset[self.all_cases_dataset['Subject'].isin(follow_up_mails['Subject'])]

#                 total_count_sent = int(follow_up_mails['Subject'].iloc[0].split(' ')[5])

#                 # print(follow_up_mails)
                
#                 current_df = self.gsheetData[self.gsheetData['ID_SAS_Manager'].isin(follow_up_mails['ID'].tolist() )]

#                 date_sent = follow_up_mails['Date'].iloc[0]
#                 date_sent = datetime.strptime(date_sent, '%Y-%m-%d %H:%M')
#                 current_date = datetime.now()
#                 days_difference = (current_date - date_sent).days

#                 if days_difference > 7 and  (current_df['DG_Class'] == 'Non DG').any() :
                
#                     dg_count = current_df[current_df['DG_Class'].str.startswith('DG')]['DG_Class'].count()
#                     non_dg_count = current_df[current_df['DG_Class'].str.startswith('Non DG')]['DG_Class'].count()
                    

#                     if total_count_sent == non_dg_count:
#                         text = text_no_change
#                         current_df = current_df
#                     else:
#                         text_minor_change = f"""
# Hi Andres,\n
# Thank you for your co-operation on the follow up.\n
# {dg_count} ASINs have been moved to DG, Would appreciate your help with {non_dg_count} ASINS.
# Please find the list of updated ASINs below along with Case IDs from Report Abuse, Seller Support & SAS-IA\n\n
# thanks,
# Rebecca"""
#                         text = text_minor_change
#                         current_df = current_df[current_df['DG_Class'] == 'Non DG']

                    
#                     try:
#                         matching_ids_dict = {}
#                         column_ids = current_df[['ID_Report_Abuse_Backend', 'ID_Seller_Support_Case', 'ID_SAS-IA_2']].stack().tolist()
#                         for index, row in current_df.iterrows():
                            
#                             asin = row['ASIN']
#                             case_ids = row[['ID_Report_Abuse_Backend', 'ID_Seller_Support_Case', 'ID_SAS-IA_2']].tolist()
#                             case_id_values = self.all_cases_dataset[self.all_cases_dataset['ID'].isin(column_ids)]
#                             case_ids_values_current_row = case_id_values[case_id_values['ID'].isin(case_ids)]['CaseID'].tolist()                            
#                             matching_ids_dict[asin] = case_ids_values_current_row


#                         self.SAS_Manager_asins_list = matching_ids_dict
                        
#                         excel_file_path = SAS_manager_template()
                    
#                         subject = f'SAS Manager - Sub - {len(current_df)}  ASINs Resolution Not Found by SAS-IA - { datetime.today().strftime("%Y-%m-%d") }'
#                         result_of_email = self.send_email_SAS(self._ASIN, subject, file = excel_file_path, sas_manager = True, follow_up_text = text)
#                         if result_of_email:
#                             self.post.ProcessErrorLog(self, 1, f'Email sent Successfully to SAS Manager for the follow up mail.   ');print(f'Email sent Successfully to SAS Manager for the follow up mail.   ')
#                         else:
#                             self.post.ProcessErrorLog(self, 1, f'Email failed - In order to send mail to SAS Manager for the follow up.  ');print(f'Email failed - In order to send mail to SAS Manager for the follow up.  ')
                   
#                     except Exception as e:
#                         self.post.ProcessErrorLog(self, 1, f"Issue in Sending SAS for for SAS Manager Follow Up  - {e} ")  

#             # follow_up_mails()

            ### Informing User for Missing Lab Reports Notification 
            def generate_email_html_user_info(lab_report_missing_list, gsheetData):
                """Generates an HTML table with missing Lab Report information for each ASIN.

                Args:
                    lab_report_missing_list: A list of ASINs that are missing Lab Report information.
                    gsheetData: A pandas DataFrame containing relevant product information.

                Returns:
                    The generated HTML string.
                """

                combined_asin_dict = {asin: [False] for asin in set(lab_report_missing_list)}

                starting_body = f"""
                    Hi Cong, <br><br>

                    This is to inform you that following ASINs have missing Lab Reports:<br><br>
                """

                ending_body = f"""<br><br>
                    Would appreciate it if you could please help with uploading the Lab Reports to the DG Violation System:
                    Link to DG Violation System - http://20.124.105.108/reportabuse/<br>
                    Thanks,<br> """

                l_template = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Dangerous Goods Issue Assistance</title>
                    <style>
                        table th {{
                        background-color: yellow;
                        }}
                        td.yes {{
                        font-weight: bold;
                        color: green;
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
                        <th>Lab Report</th>
                        </tr>
                        {"".join([
                        f"<tr>"
                        f"<td>{i+1}</td>"
                        f"<td>{asin}</td>"
                        f"<td>{gsheetData[(gsheetData['ASIN'] == asin)]['ProductName'].values[0] if asin in gsheetData['ASIN'].values else ''}</td>"
                        f"<td>{'Required'}</td>"
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
                self.missing_lab_reports, self.gsheetData)
            if datetime.now().weekday() == 0:
                self.inform_users_via_mail(f"DG VIOLATION: Unavailable Lab report for ASINs", html, missing_lab_report = True )
                self.post.ProcessErrorLog(self, 1, "Informed user for missing Lab reports")
                self.update_lab_report_case_id()

            
            

           
                        
            
            print("getdatafromamazon","ASIN VL prepared successfully!")   
            self.post.ProcessErrorLog(self, 1, "Processed Sucessfully")
            self.IsComplete = 1
            ### Delete all directories in the end
            # shutil.rmtree(self.asins_directory_path)
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
        
            # time.sleep(1)
            # elems = self.driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
            # url = elems.get_attribute('src')                            
            # urllib.request.urlretrieve(url, "Captcha.jpg")
            # img = cv2.imread(r"Captcha.jpg")
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # noise=cv2.medianBlur(gray,3)
            # thresh = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # reader = easyocr.Reader(['en'], gpu=True)
            # result = reader.readtext(img,paragraph=False)
            # df=pd.DataFrame(result)
            # print(df[1][0])
            # time.sleep(1)
            # elems = self.driver.find_element_by_id('captchacharacters')
            # elems.send_keys(df[1][0])
            # time.sleep(2)
            # elems = self.driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')    
            # elems.click()

            # time.sleep(5)
            # title = self.driver.title
            # captcha = self.driver.find_elements_by_link_text('Try different image')
            # if title=='Server Busy' or len(captcha)>0:
            #     return True
            # else:
            #     return False 

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

            print("Amazon Dangerous_goods Category ", str(CountryID), str (RPAPID))  
           
            
            
            #self.IDList =  self.IDList[self.IDList['Process_Name'].isin(['1|B075MBKTTY'])]



            print("Amazon Dangerous_goods", str(CountryID), str (RPAPID))  
            if self.ID == 0:
                self.loadASIN()
            else:
                self.gsheetData = self.readgooglesheet()
            
            self.IDList = self.post.ProcessLogGetLast(self)
            #self.IDList =  self.IDList[self.IDList['Process_Name'].isin(['1|B075MBKTTY'])]
            

            while len(self.IDList.loc[self.IDList['Status']==0]) != 0:
                
                print('Current Count ', str(CurrentCount))            
                
                if CurrentCount == CloseCount:
                    print('App Close')
                    break

                if ((self.StartDate + timedelta(hours=5)) <  datetime.now()):
                    self.post.ProcessErrorLog(self, 1, "Job Time Over")
                    break 


                CurrentCount= CurrentCount + 1




                time.sleep(5)
                self.openbrowser(1)                
                time.sleep(5)
                try:
                    self.ImageCaptcha()
                except: ...
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
                time.sleep(60)
            
            if len(self.IDList.loc[self.IDList['Status']==0]) == 0:
                self.post.ProcessErrorLog(self, 1, f' Records Finished ...  ');print(f' Records Finished ...  ')
                ... 
                # self.sendmessage()
     


            self.post.ProcessErrorLog(self, 1, "ProcessStart Sucessfully Completed !")
            
        except Exception as err:  
            print(err)
            self.post.ProcessErrorLog(self, 2, "ProcessStart " + str(err)) 

    def classification_product(self):

        

        def copy_image(image_path, destination_directory_path):
            """Move an image to a destination directory."""
            shutil.copy(image_path, destination_directory_path)
        
        asins_directory_path = os.path.join(os.getcwd(), "asins")
        self.create_directory(asins_directory_path)
        dir_name = f"{self._ASIN}__{datetime.today().strftime('%Y_%m_%d_%H_')}"
        dir_ = os.path.join(asins_directory_path, dir_name)
        
        if not os.path.exists(dir_):
            os.makedirs(dir_)

        dangerous_good_directory_path = os.path.join(dir_,f"dangerous_good_images_{self._ASIN}_{ datetime.today().strftime('%Y_%m_%d_%H_') }")
        self.create_directory(dangerous_good_directory_path)
        self.dir_name = f"{self._ASIN}__{datetime.today().strftime('%Y_%m_%d_%H_')}"
        self.dir_ = os.path.join(self.asins_directory_path, self.dir_name)
        self.dangerous_good_directory_path = os.path.join(self.dir_,f"dangerous_good_images_{self._ASIN}_{ datetime.today().strftime('%Y_%m_%d_%H_') }")
        

        def common_pattern_search(element):
            return re.search("^100%", element, re.IGNORECASE) or element == "1OO%" or element.startswith('1OO%') or element.endswith('1OO%')
        
        def replace_pattern(element):
            return element.replace('*','').replace('\n',' ').replace('.','').replace(';','').replace('00','OO').replace('0','O').replace(',','').replace('/','').strip()

        self.keyword = replace_pattern(self.keyword)

        try:

            lines = {}
            self.driver.get("https://www.amazon.com/dp/" + self._ASIN)
            time.sleep(2)
            title_value= self.driver.find_element (by=By.ID , value= 'titleSection')
            time.sleep(2)
            titletext = title_value.text
            description = self.driver.find_element (By.ID , value= "feature-bullets")
            descriptiontext = description.text
            time.sleep(2)
            lines = descriptiontext.split("\n")
            for bulletnumber in range(len(lines)):
                lines[bulletnumber] = "*" + lines[bulletnumber]
            text = "\n".join(lines)
            time.sleep(2)
            pd_text = self.driver.find_element(By.ID, value='productTitle')
            pd_text = pd_text.text
            bullet_points = lines 
    
            time.sleep(2)

            """   4 Checks being done for marking the product as dangerous good  """

            ### 1. Product heading Text
            print('\nChecking Keyword in Product Heading Text')
            self.post.ProcessErrorLog(self, 1, f' Checking Keyword in Product Heading Text ')
            split_lines_heading = pd_text.split(' ')
            product_txt = [ replace_pattern(i) for i in split_lines_heading ]
            i = [i for i in range(len(split_lines_heading)) if common_pattern_search(split_lines_heading[i]) ]
            if i: 
                i = i[0]
                if '100%' in split_lines_heading[i] or '1OO' in split_lines_heading[i]:
                    split_lines_heading[i] = '1OO%'
                product_txt = ' '.join( (split_lines_heading[i], split_lines_heading[i+1]) )
                product_txt = replace_pattern(product_txt)
                if product_txt == self.keyword:

                    print('keyword matched from product text, marking the ss for the same')
                    query = 'original_content = document.querySelector("#productTitle").textContent;'
                    query = query + 'return original_content'
                    self.driver.execute_script(query)
                    self.driver.execute_script("""  
                        const productTitleElement = document.querySelector("#productTitle");

                        if (productTitleElement) {
                            const lowercaseTitle = productTitleElement.textContent.toLowerCase();
                            if (lowercaseTitle.includes("100% pure")) {
                                productTitleElement.innerHTML = productTitleElement.innerHTML.replace(
                                    /100% pure/gi,
                                    "<span style='text-decoration: underline; text-decoration-color: red;'> 100% Pure</span>"
                                );
                            }
                        }

                    """)
                    
                    image_path = f"{self.dir_}/main_page__ss.png"
                    time.sleep(2)
                    pyautogui.screenshot(image_path)
                    time.sleep(1.5)
                    img = cv2.imread(image_path)
                    cv2.line(img,  (130,95) ,(600,95) , (0,0,255), 4)   ### mark the line on the URL
                    time.sleep(1.5)
                    cv2.imwrite(image_path, img)
                    time.sleep(1.5)
                    copy_image(image_path, dangerous_good_directory_path)

                    print('Keyword matched from " heading text ", Marked ASIN as dangerous good')
                    self.post.ProcessErrorLog(self, 1, f' Keyword matched from " heading text ", Marked ASIN as dangerous good ')
                    self.dangerous_good[self._ASIN] = True

            ### 2. Bullet points texts
            print('\nChecking Keyword in Bullet points')
            self.post.ProcessErrorLog(self, 1, f' Checking Keyword in Bullet points ')
            bullet_points = text.split(' ')
            bullet_points = [ replace_pattern(i) for i in bullet_points ]
            i = [i for i in range(len(bullet_points)) if   common_pattern_search(bullet_points[i]) ]
            if i:
                i = i[0]
                if '100%' in bullet_points[i] or '1OO' in bullet_points[i]:
                    bullet_points[i] = '1OO%'
                bullet_txt = ' '.join( (bullet_points[i], bullet_points[i+1]) )
                bullet_txt = bullet_txt.lower()
                if bullet_txt == self.keyword.lower():
                    print('Keyword matched from " bullet texts ", Marked ASIN as dangerous good')
                    
        
                    self.driver.execute_script(""" 
                        const listItems = document.querySelectorAll(".a-unordered-list.a-vertical.a-spacing-mini li");

                        if (listItems) {
                            listItems.forEach(item => {
                                if (item.textContent.toLowerCase().includes("100% pure")) {
                                    item.innerHTML = item.innerHTML.replace(/100% Pure/gi, "<span style='text-decoration: underline; text-decoration-color: red; text-decoration-thickness: 3px;'>$&</span>");
                                    item.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                }
                                console.log(item.textContent);
                                console.log('---');
                            });
                        }

                    """)
                    
                    
                    time.sleep(2)
                    image_path = f"{self.dangerous_good_directory_path}/keywords.png"
                    pyautogui.screenshot(image_path)
                    time.sleep(1.5)
                    self.post.ProcessErrorLog(self, 1, f' Keyword matched from " bullet texts ", Marked ASIN as dangerous good ')
                    self.dangerous_good[self._ASIN] = True

            ### 3. Texts in all Images
            print('\nChecking Keyword in Each Image')
            self.post.ProcessErrorLog(self, 1, f' Checking Keyword in Each Image ')

            if self.take_ss_of_images_asin():
                print('Screenshots taken for each image for ASIN',self._ASIN)
            else:
                return False
            
            self.post.ProcessErrorLog(self, 1, f' Screenshots taken for each image for ASIN {self._ASIN} stored in directory {dangerous_good_directory_path} ')
            
            images = os.listdir(dir_)
            for img in images:
                try:
                    time.sleep(1)
                    image_path = os.path.join(dir_, img)
                    if os.path.isdir(image_path):
                        continue
                    for word in ['main_page__ss', 'keywords','Ingredients']:
                        if word in image_path.split('\\')[-1].split('.')[0]:
                            continue
                    im = Image.open(image_path)
                    
                    system_coordinates_crop_image = (0, 0, 850, 1000)
                    self.post.ProcessErrorLog(self, 1, f' System Coordinates for the cropped image {system_coordinates_crop_image}  ')
                    im = im.crop(system_coordinates_crop_image)  ### local system coordinates | change to server's coordinates ###
                    temp_image = 'captcha.jpg'
                    img = cv2.imread(image_path)
                    original_img = img
                    img = img[0:1000, 0:850] 
                    cv2.imwrite(f"{temp_image}", img)
                    time.sleep(2)
                    result = subprocess.run(f"python AmazonCap.py  {temp_image}", capture_output=True, text=True, universal_newlines=True)
                    print('\nImage path', image_path)
                    result = result.stdout
                    data = ast.literal_eval(result)
                    df=pd.DataFrame(data)
                    res = ', '.join(df[1])
                    res = res.split(' ')
                    words = [(res[i], res[i+1]) for i in range(len(res)) if common_pattern_search(replace_pattern(res[i])) ]
                    print(words)
                    if words:
                        # for word in words:
                        words = words[0]
                        image_txt = replace_pattern(' '.join(words))
                        self.post.ProcessErrorLog(self, 1, f' Checking image text with keyword  {image_txt, self.keyword, image_txt == self.keyword} ')
                        print(image_txt.lower(), self.keyword.lower(), image_txt.lower() == self.keyword.lower())
                        if self.keyword.lower() == image_txt.lower():
                            strings = df[1].tolist()
                            keyword_strings = [string for string in strings if common_pattern_search(replace_pattern(string)) ]
                            if keyword_strings:
                                keyword_coordinates = []
                                for keyword_string in keyword_strings:
                                    row_index = df.index[df[1] == keyword_string].tolist()[0]
                                    coordinate = df.iloc[row_index, 0]
                                    keyword_coordinates.append(coordinate)
                                coordinates = keyword_coordinates[0]
                                coordinates[2] = tuple(coordinates[2])
                                coordinates[3] = tuple(coordinates[3])
                                cv2.line(img,  coordinates[2] ,coordinates[3] , (0,0,255), 4)
                                cv2.imwrite(image_path, original_img)
                                copy_image(image_path, dangerous_good_directory_path)
                                print(f'Keyword matched from the Image  {image_path}, Marked the asin as dangerous good')
                                self.post.ProcessErrorLog(self, 1, f'Keyword matched from the Image  {image_path}, Marked the asin as dangerous good' )
                                self.dangerous_good[self._ASIN] = True
                except Exception as e:
                    print('Issue in processing image', img)
                    continue    

            
            self.post.ProcessErrorLog(self, 1, f' Conversion done for each image for ASIN {self._ASIN} and stored the images in the directory ')
            

            ### 4. Ingredients
            print('\nChecking Keyword in Ingredients list')
            self.post.ProcessErrorLog(self, 1, f' Checking Keyword in Ingredients list ')
            try:
                Ingredients_text  = self.driver.find_element(By.CSS_SELECTOR, '.a-section.a-spacing-extra-large.bucket').text
                Ingredients_text = replace_pattern(Ingredients_text.split('Legal')[0].split('Ingredients')[1])
            except:
                return self.dangerous_good_directory_path
            Ingredients_text = Ingredients_text.split(' ')
            Ingredients_text = [(Ingredients_text[num],Ingredients_text[num+1]) for num in range(len(Ingredients_text))  if common_pattern_search(Ingredients_text[num]) ]
            if Ingredients_text:
                Ingredients_text = ' '.join(Ingredients_text[0]).lower()
                self.keyword = self.keyword.lower()
                if self.keyword == Ingredients_text:
                        
                    self.driver.execute_script(""" try {
                            
                        const contentDivs = document.querySelectorAll(".a-section.content");

                            if (contentDivs) {
                                contentDivs.forEach(div => {
                                    try {
                                        console.log(div.innerHTML);
                                        console.log('---');

                                        // Example modification for "90 days"
                                        // if (div.innerHTML.toLowerCase().includes("90 days")) {
                                        //     div.innerHTML = div.innerHTML.replace(/90 days/gi, "<span style='text-decoration: underline; text-decoration-color: red; text-decoration-thickness: 3px;'>90 days</span>");
                                        //     div.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                        // }

                                        // Modification for "100% pure"
                                        if (div.innerHTML.toLowerCase().includes("100% pure")) {
                                            div.innerHTML = div.innerHTML.replace(/100% pure/gi, "<span style='text-decoration: underline; text-decoration-color: red; text-decoration-thickness: 3px;'>$&</span>");
                                            div.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                        }
                                    } catch (error) {
                                        console.error("Error processing contentDiv:", error);
                                    }
                                });
                            }
                        } catch (error) {
                            console.error("Error finding contentDivs:", error);
                        }

                    """)
            
                    time.sleep(1.5)
                    image_path = f"{self.dangerous_good_directory_path}/Ingredients.png"
                    pyautogui.screenshot(image_path)
                    time.sleep(1.5)
                    print('Keyword matched from Images texts, Marked ASIN as dangerous good')
                    self.post.ProcessErrorLog(self, 1, f' Keyword matched from Images texts, Marked ASIN as dangerous good ')
                    self.dangerous_good[self._ASIN] = True
                else:
                    print(0)
            self.post.ProcessErrorLog(self, 1, f' Classification report completed for ASIN {self._ASIN} ')
            self.post.ProcessErrorLog(self, 1, f' Returing directory path containing image with dangerous good {self.dangerous_good_directory_path} ')
            
            print("Checked everything, returning with the reports\n")
            return self.dangerous_good_directory_path

        except Exception as e:
            print(f"Issue in Classification report {e}")
            self.post.ProcessErrorLog(self, 2, f"Issue in Classification report {e}")
            self._ManualLog = 'Error in Classification Product'
            return False

    def take_ss_of_images_asin(self):
        
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            self.driver.execute_script("window.scrollBy(0, 400)") 
            image_buttons = self.driver.find_elements(By.CLASS_NAME, value = 'imageThumbnail')
            for idx, button in enumerate(image_buttons):
                if button.is_displayed():
                    print(button.is_displayed())
                    button.click()
                    time.sleep(2)
                    # Find the image element inside the large image container
                    li = self.driver.find_element(by=By.CLASS_NAME, value='itemNo'+ str(idx))
                    img_url = li.find_element(by=By.TAG_NAME, value='img').get_attribute("src")
                    titlename = f"TF_{idx+1}_F.jpg"
                    filename = f'{self._ASIN}_' + titlename
                    print(filename)
                    image = f"{self.dir_}/{filename}"
                    self.driver.save_screenshot(image)
                    time.sleep(1)
                else:
                    print(f"Image button {idx}  not displayed, trying again")
                    self.post.ProcessErrorLog(self, 1,f"Image button  {idx}  not displayed, trying again")
                    time.sleep(1)
                    button.click()
                    
                    if button.is_displayed():
                        li = self.driver.find_element(by=By.CLASS_NAME, value='itemNo'+ str(idx))
                        img_url = li.find_element(by=By.TAG_NAME, value='img').get_attribute("src")
                        titlename = f"TF_{idx+1}_F.jpg"
                        filename = f'{self._ASIN}_' + titlename
                        print(filename)
                        image = f"{self.dir_}/{filename}"
                        self.driver.save_screenshot(image)
                        time.sleep(1)
                    else:
                        print(f"Image button still not displayed, skipping image {idx} ")
                        self.post.ProcessErrorLog(self, 1,"Not all Images displayed correctly")
                        return False

            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(3)
            return "Successfull in Taking Screenshots."

        except Exception as e:
            print("Error in taking ss of the asin")
            self.post.ProcessErrorLog(self, 2,"Error in taking ss of the asin")
            self._ManualLog = 'Error in taking ss'
            return False

    def reporting_issue_backend(self, subject):

        try:
            self.driver.get("https://sellercentral.amazon.com/abuse-submission/index.html?ref=ahd_asf")
            
            time.sleep(5)

            self.driver.find_element(By.ID,'/abuse-submission/form/duplicate-listing')            


            self.driver.find_element(By.ID,'/abuse-submission/form/duplicate-listing').click()
            self.driver.find_element(By.LINK_TEXT,"Content on detail page is incorrect or not allowed as per Amazon's policy").click()
            other_btn = 'btn = document.querySelector("#katal-id-18").click()'
            self.driver.execute_script(other_btn)
            print('other button clicked ')

            time.sleep(5)
            # provide_asin = f'document.querySelector("#asins-input").shadowRoot.querySelector("#katal-id-5").value = "https://www.amazon.com/dp/{self._ASIN}" '
            # self.driver.execute_script(provide_asin)
            # self.driver.execute_script('document.querySelector("#asins-input").shadowRoot.querySelector("#katal-id-5").click()')
            self.driver.find_elements(By.CLASS_NAME,'asf-kat-input')[0].send_keys(f"https://www.amazon.com/dp/{self._ASIN}/")
            self.driver.find_element(By.ID,'asins-add-item-button').click()
            time.sleep(5)
            
            self.driver.find_elements(By.CLASS_NAME,'asf-kat-input')[1].send_keys(subject)
            # provide_concern_text = f'document.querySelector("#PDP_VIOLATES_AMZ_POLICIES_INCORRECT_CONTENT > div > div:nth-child(7) > div > kat-input").shadowRoot.querySelector("#katal-id-6").value= "100% Pure Image"'
            # self.driver.execute_script(provide_concern_text)

            content = f"""Please Investigate
ASIN(s): {self._ASIN} is Flammable and a Dangerous Goods but currently being sold and shipped as Normal FBA.

There are multiple claims on Detail Page Images, Title & Packaging that the product is 100% Pure and consist of 1 single Ingredient.

Which is well below the US & IATA allowed NON DG classification.
Product should be classified as DG"""
            
            time.sleep(5)
            self.driver.find_element(By.NAME, 'issue-description').send_keys(content)
            time.sleep(2)
            # self.driver.find_elements(By.CLASS_NAME,'asf-kat-input')[0].send_keys(Keys.ENTER)
            
            submit_btn = 'document.querySelector("#submit-button").shadowRoot.querySelector("button").click()'
            self.driver.execute_script(submit_btn)
   
            print('submit button clicked')
            self.post.ProcessErrorLog(self, 1, f"  submit button clicked, for reporting issue backend, lets wait for the mail for the complaint number  ") 
            return "submit button clicked"
            
            
        except Exception as err: 
            
            self.post.ProcessErrorLog(self, 2, f"  reporting_issue_backend issue {err} ") 
            print("reporting_issue_backend ", str(err))
            self._ManualLog = 'Error in reporting Issue Backend'
            return False

    def front_end_asin_report(self,asin):
        
        try:

            """
                Report an issue for the asin from the front end page
            """

            self.driver.get(f'https://www.amazon.com/dp/{asin}')
            self.driver.find_element(By.CLASS_NAME,'_tell-amazon-desktop_style_tell_amazon_link__1KW5z').click()
            time.sleep(2)
            other_btn = 'btn = document.querySelector("#tellAmazon_firstLevelDropdown").click()'
            self.driver.execute_script(other_btn)
            time.sleep(1)
            try:
                self.driver.find_element(By.XPATH, "//li[@tabindex='0' and @role='option' and @aria-labelledby='tellAmazon_firstLevelDropdown_6' and @class='a-dropdown-item']/a").click()
            except:
                self.driver.find_element(By.CSS_SELECTOR, "[aria-labelledby='tellAmazon_firstLevelDropdown_6']").click()

            report_case_text =f"""Title: ASINs are Flammable - Should be classified as DG

Please Investigate the listed ASIN:
{asin}

as it should be classified as Flammable Dangerous Goods but currently being sold and shipped as Normal FBA.

There are multiple claims on Detail Page Images, Title & Packaging that the product is 100% Pure and consist of 1 single Ingredient, the CAS Nos for these ingredients are below 60C

Which is well below the US & IATA allowed NON DG classification. 
Products should be classified as DG Flammable"""

            self.driver.find_element(By.XPATH,"//textarea[@id='tellAmazon_details']").send_keys(report_case_text)
            try:
                self.driver.find_element(By.ID,"tellAmazon_submitButton-announce").click()
            except:
                self.driver.execute_script('document.querySelector("#tellAmazon_submitButton > span > input").click()')
            print('submit button clicked')
            self.post.ProcessErrorLog(self,1,'submit button clicked')
            return True
        except Exception as err:  
            
            self.post.ProcessErrorLog(self, 2, f"  front_end_asin_report issue {err} ")
            print("front_end_asin_report ", str(err))
            self._ManualLog = 'Error in reporting Issue Frontend'
            return False

    def seller_support_case(self, asin, file_path, all_child_asins=[], subject = None ):

        try:    
            

            self.driver.get("https://sellercentral.amazon.com/home?mons_sel_dir_mcid=amzn1.merchant.d.ADVSOBI7NLBGFP3CTZPHOFNEOKCA&mons_sel_mkid=A1F83G8C2ARO7P&mons_sel_dir_paid=amzn1.pa.d.ACK2GASJ5Y6PL7M4KUAMRCL7EO2A&ignore_selection_changed=true&mons_redirect=change_domain")
            sleep(3)

            #self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.get("https://sellercentral.amazon.com/help/hub/support/INTENT_CTI_PSS")
            sleep(5)
            
            # if all_child_asins:
            print("TxT for Dangerous goods")
            txt ="Please Investigate, \n\n"
            txt = txt + f"ASIN(s): {all_child_asins} is Flammable and a Dangerous Goods but currently being sold and shipped as Normal FBA.\n"
            txt = txt + f"There are multiple claims on Detail Page Images, Title & Packaging that the product is 100% Pure and consist of 1 single Ingredient.\n"
            txt = txt + "Which is well below the US & IATA allowed NON DG classification.\n"
            txt = txt + "\nProduct should be classified as DG"
            txt = txt.replace('@ASIN', asin)
            print(txt)
            self.post.ProcessErrorLog(self, 1, txt)
            self.driver.execute_script("window.scrollBy(0, 1000)") 

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
            except : ...
            try:
                ## Account related
                self.driver.execute_script( 'document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div > div > div:nth-child(2) > div > div.button-options > kat-button:nth-child(1) > div > div").click()' )
                time.sleep(5)
                self.driver.execute_script("window.scrollBy(0, 1000)") 
            except : ...

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
            
            ### add attachments
            time.sleep(5)
            for _file in os.listdir(file_path):
                _file = os.path.join(file_path,_file)
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
                    lbl = autoit.control_send(dialog_window_title, "Edit1", _file)
                    print('Edit ', lbl)
                    self.post.ProcessErrorLog(self, 1, f'Edit ')
                    time.sleep(2)
                    lbl = autoit.control_click(dialog_window_title, "Button1")
                    print('Button1 ', lbl)
                    self.post.ProcessErrorLog(self, 1, f'Button1 ')
                    print(_file,' Image added')
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
            caseid = 'caseid = document.querySelector("#mons-body-container").contentWindow.document.querySelector("#root > div > section.kat-col.body > section > kat-box > div.meld-transcript > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div > div.meld-case-created-outer-container > div > div > p:nth-child(2) > a").textContent ; '
            caseid += 'return caseid ;'
            caseid = self.driver.execute_script(caseid)
            print('Case ID number =\t',caseid)
            self.post.ProcessErrorLog(self, 1, f" Case ID number = {caseid } ")
            _ManualLog = caseid
            self._ManualLog = caseid

            return _ManualLog
        
        except Exception as err:  
            print('seller_support_case  issue ',str(err))
            self.post.ProcessErrorLog(self, 2, f"  seller_support_case issue  {err}")
            _ManualLog = "Error Case Log PSS"
            return False

    def check_status(self,asin):
        
        """
            Check if itss DG or Not 
        """

        try:

            """ 
                Confirm the status of asin if [product is converted into Dangerous good
            """


            self.driver.get('https://sellercentral.amazon.com/revcal')
            time.sleep(4)

            # # ### give the asin in the textbox
            self.driver.find_element(By.CLASS_NAME,'input-asin').click()
            time.sleep(1)
            actions = ActionChains(self.driver) 
            time.sleep(1)
            actions.send_keys(asin )
            time.sleep(1)
            actions.send_keys(Keys.ENTER)
            time.sleep(1)
            actions.perform()
            time.sleep(3)
            if 'No products in your catalog matched your search, please select a product from other products on Amazon or try searching again with different inputs.' in self.driver.page_source:self.post.ProcessErrorLog(self, 1, f'ASIN {self._ASIN} has been deactivated  ');print(f'ASIN {self._ASIN} has been deactivated  ');return "Deactivated"
            self.driver.execute_script("window.scrollBy(0, 400)") ;time.sleep(2)
            ### fullfillment cost button
            self.driver.execute_script('document.querySelector("#ProgramCard > div.program-card-box-under > div.program-card-box-top > div.cost-section > div > kat-expander:nth-child(2)").shadowRoot.querySelector("div.wrapper > button > div.header__toggle > slot > kat-icon").shadowRoot.querySelector("i").click()')
            time.sleep(10)
            
            # ## i button click
            self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/kat-box[1]/div[2]/div[1]/div[3]/div/kat-expander[2]/div[2]/div[1]/kat-link[2]').click()
            time.sleep(10)

            ### product identifier program
            query = 'word = document.querySelector("body > div.fee-explainer-tooltip-template > iframe").contentWindow.document.querySelector("body > section > div > kat-box > kat-tabs > kat-tab:nth-child(1) > div > div:nth-child(1) > dl > div:nth-child(1)").textContent;'
            query = query + 'return word'
            word = self.driver.execute_script(query)
            word = word.replace("Programs:",'')
            
            
            if word.startswith("Dangerous"):
                print(f"{word} | Product {asin} has been classified as dangerous good")
                return True
            print(f"{word} | Product not listed as dangerous good - {asin} ")
            return False
        
        
        except Exception as e:
            print('Issue in check_status method ', e)
            self.post.ProcessErrorLog(self, 2, f"  Issue in check_status method {e}  ")
            self._ManualLog = 'Error in Checking Status of the asin'
            return 'Error'
            
    def chat_gpt_output(self, _input):
        from openai import OpenAI
        import json

        client = OpenAI(api_key='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')

        f = open('data.json')
        _JsonData = json.load(f)


        _JsonData.append({"role": "user", "content":  _input})

        response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages = _JsonData,

        )

        output = response.choices[0].message.content 
        output=  output.replace('[Your Name]','Rebecca Dark') 
        # _JsonData.append({"role": "assistant", "content": output})
        print(output)
        return output


    def get_cases_in_df(self):
        
        try:

            self._ManualLog = ''
            self.driver.get("https://sellercentral.amazon.com/cu/case-lobby?ref=xx_caselog_count_home")
            sleep(3)
            
            table = self.driver.find_element(by = By.XPATH, value='//*[@role="rowgroup"]')
            tablerows = table.find_elements(by = By.XPATH, value='//*[@role="row"]')
            searchcaseid = tablerows[0].find_element(by = By.XPATH, value='//*[@type="search"]')
            
            
            searchcaseid.send_keys("DG Violation Classify Flammable")
            sleep(2)
            searchbtn = tablerows[0].find_elements(by = By.XPATH, value='//*[@label="Go"]')
            searchbtn[0].click()
            sleep(2)

            condition = True

            
            # Function to check if a given date is a weekend (Saturday or Sunday)
            def is_weekend(date):
                return date.weekday() in [5, 6]  # 5 represents Saturday, and 6 represents Sunday

            # Function to calculate the adjusted current date
            def calculate_adjusted_current_date(date_text):
                date_obj = datetime.strptime(date_text, '%B %d, %Y')
                difference = datetime.now() - date_obj
                adjusted_difference = difference + timedelta(days=sum(1 for day in range(difference.days + 1) if is_weekend(date_obj + timedelta(days=day))))
                return datetime.now() - adjusted_difference
            
            last_row_date = self.driver.find_elements(By.CLASS_NAME, 'hill-case-lobby-search-results-panel-creationDate')[-1].text
            last_row_date  = last_row_date .split('at')[0].strip()

            adjusted_current_date = calculate_adjusted_current_date(last_row_date)

            data_list = []
            Next_condition = True
            while 1:
                last_row_date = self.driver.find_elements(By.CLASS_NAME, 'hill-case-lobby-search-results-panel-creationDate')[-1].text
                last_row_date = last_row_date.split('at')[0].strip()

                time.sleep(1)
                print('\nLast row date of the Page -', last_row_date, '\t &  Our adjusted date - ', adjusted_current_date, '\n')
                current_window_handle = self.driver.current_window_handle
                self.driver.switch_to.window(current_window_handle)  
                all_cases_view_button = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-view-case-button')
                creation_date_shown = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-search-results-panel-creationDate')
                case_ids_shown = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-search-results-panel-caseId')
                short_description = self.driver.find_elements(By.CLASS_NAME,'hill-case-lobby-search-results-panel-shortDescription')
                
                print(1)

                if all_cases_view_button:
                    self.driver.switch_to.window(current_window_handle)
                    time.sleep(1)

                    for view_button_, creation_date, case_id, short_desc in zip(all_cases_view_button, creation_date_shown, case_ids_shown, short_description):
                        timeline_creation_date = creation_date.text.split('at')[0].strip()
                        date_text_obj = datetime.strptime(timeline_creation_date, '%B %d, %Y') 
                        if date_text_obj <= adjusted_current_date :
                            print('Current Date\t', date_text_obj, ' is <= | Thus LIMIT REACHED \t', adjusted_current_date, '\n')
                            Next_condition = False
                            break
                        else:
                            time.sleep(2)
                            short_desc_text = short_desc.text
                            row_data = {
                                'Creation Date' : creation_date.text,
                                'Case ID' : case_id.text ,
                                "Short Description": short_desc_text}
                            view_button_.send_keys(Keys.CONTROL + Keys.RETURN)
                            time.sleep(2)

                            while True:
                                try:
                                    self.driver.switch_to.window(self.driver.window_handles[-1])
                                    break  
                                except StaleElementReferenceException:
                                    print("Stale element exception, retrying for this row")
                                    continue

                            time.sleep(3)
                            see_more_buttons = [self.driver.find_elements(By.CLASS_NAME, 'link')[-1]]
                            for button in see_more_buttons:
                                try:
                                    if button.text.split('\n')[1].endswith('more'):
                                        self.driver.execute_script("arguments[0].click();", button)
                                    time.sleep(2)
                                except Exception as e:
                                    print(f"Error clicking 'See More' button: {e}")

                            subject_text = self.driver.find_elements(By.CLASS_NAME, 'contact-content')[-1].text
                            print(2)
                            subject_text = subject_text.strip().replace('\n', ' ')
                            row_data['Subject Text'] = subject_text
                            print('Got the Subject text of the email')
                            
                            time.sleep(3)
                            reply_btn = self.driver.find_elements(By.CLASS_NAME,'view-case-reply-buttons-container')
                            if len(reply_btn) <=0:
                                print(f'Case closed   ')
                                row_data['Case Status'] = "Closed"
                            else:
                                print('Case is Active - ', short_desc_text, '\n')
                                row_data['Case Status'] = "Open"
                            self.driver.close()
                            print(3)
                            self.driver.switch_to.window(current_window_handle)
                            data_list.append(row_data)

                    if Next_condition:
                        next_button = self.driver.execute_script('return document.querySelector("#root > div > div.hill-case-lobby-tabs-container > kat-box > div:nth-child(2) > div:nth-child(3) > kat-table > kat-table-body > kat-table-row > kat-table-cell:nth-child(2) > kat-pagination").shadowRoot.querySelector("nav > span:nth-child(3) > kat-icon")')
                        next_button.click()  
                        time.sleep(1)
                        self.driver.switch_to.window(current_window_handle)    
                            
                    else:
                        self.df_case_ids = pd.DataFrame(data_list)
                        self.df_case_ids = self.df_case_ids.drop_duplicates()  
                        return self.df_case_ids 

        except Exception as e:
            print("error in getting the outputs from dataframe", e)
            return False


''' 
Run specific Asins from self.IDList

    CLIENT_SECRET_FILE = 'GoogleCredentials\client_sheet.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
        
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    results = service.files().list(
        q=f"'16fm3LVKRRL_QXHDLGYV8cXMEVTqShdgj' in parents",    
        pageSize=1000, 
        fields="nextPageToken, files(id, name, mimeType, parents, trashed)"
    ).execute()
    items = results.get('files', [])
    items = pd.DataFrame(items)   
    my_asin_list  = [i.split('.pdf')[0].split('-')[2] for i in items['name'] ]  
    
    
    self.IDList = self.post.ProcessLogGetLast(self)

    ### Specific asins 
    my_asin_list =  f"""B08ZLLHZ72, B08YKG2K1Z""".split(',')
    
    self.IDList.iloc[0]
    self.IDList['Process_Name'].tolist()
    self.IDList = self.IDList[47:]
    
    ### for multiple asins

my_asin_list = """B08YL2ZSX2
B08YL9QZ5T
B09HCB2FSL
B08ZLKB98C
B08ZLLHZ72
B088TCL5WQ
B08ZLHWX5Z
B09HC1CQRX
""".split('\n')

entries  = {num[1]: num[2] for num in self.IDList["Process_Name"].str.split("|")} 

self.IDList['Process_Name'] = ['1|' + i + f'|{entries.get(i)}' if index < len(my_asin_list) else '' for index, i in enumerate(my_asin_list)] + [''] * (len(self.IDList) - len(my_asin_list))

    ### ASINS not marked yes but lab report present

    # get items code from top of it .
    df = self.gsheetData
    asins_with_lab_report = [i.split('.pdf')[0].split('-')[2] for i in items['name']]
    not_marked_yes = df.loc[df['ASIN'].isin(asins_with_lab_report) & (df['Lab Report'] != 'yes'), 'ASIN'].tolist()
    print(not_marked_yes)




    '''

