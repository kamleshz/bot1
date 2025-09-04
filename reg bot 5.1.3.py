import pandas as pd
import numpy as np
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
from xlsx2html import xlsx2html
import xlsxwriter
import tkinter.filedialog as fd
import time
import os
import easygui
import sys
import datetime
import getpass
from PyPDF2 import PdfMerger,PdfReader
from pathlib import Path
import pdfkit
import math
import re
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook
import pyperclip
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import os
import requests
import json


root = Tk()

canvas1 = tk.Canvas(root, width = 180, height = 80)
canvas1.pack()
canvas4 = tk.Canvas(root, width = 180, height = 80)
canvas4.pack()
canvas5 = tk.Canvas(root, width = 180, height = 80)
canvas5.pack()
canvas6 = tk.Canvas(root, width = 180, height = 80)
canvas6.pack()
canvas2 = tk.Canvas(root, width = 180, height = 80)
canvas2.pack()
canvas3 = tk.Canvas(root, width = 180, height = 150)
canvas3.pack()



##def hello ():
##    global errors
##    global invoicee
##    global roww
##    global driver
##    today = date.today()
##    try:
##        driver = webdriver.Chrome()
##    except:
##        driver = webdriver.Edge()
##    driver.maximize_window()
##    driver.implicitly_wait(15)
##    driver.get('https://eprplastic.cpcb.gov.in/#/plastic/home')
##    time.sleep(1)
    
##    mail = easygui.enterbox("Enter Email ")
##    passs = easygui.enterbox("Enter Password")
##    #mail = 'goelabhishk@gmail.com'
##    #passs = 'Abhi@1234'
##    email = driver.find_element(by=By.XPATH, value='//*[@id="username"]')
##    email.send_keys(mail)
##    password = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
##    password.send_keys(passs)
##    login = driver.find_element(by=By.XPATH, value='//*[@id="signIn"]')
##    login.click()
##    time.sleep(4)
##    
##    otpp = easygui.enterbox("enter otp")
##    otp = driver.find_element(by=By.XPATH, value='//*[@id="loginUserID"]').send_keys(otpp)
##    driver.implicitly_wait(15)
##    continu = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-plastic/div/app-admin-login/div/div/div/div[2]/div[2]/div/div[2]/form/div[2]/button').click()
##    errors = []
##    invoicee = []
##    roww=[]
##    c=-1


def hello ():
    global errors
    global invoicee
    global roww
    global driver
    today = date.today()
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get('https://eprplastic.cpcb.gov.in/#/plastic/home')
    time.sleep(1)
    
    mail = easygui.enterbox("Enter Email ")
    passs = easygui.enterbox("Enter Password")
    action = ActionChains(driver)
    action.click(on_element = driver.find_element(by=By.XPATH, value='//*[@id="user_name"]')).perform()
    action.click(on_element = driver.find_element(by=By.XPATH, value='//*[@id="password_pass"]')).perform()
    driver.find_element(by=By.XPATH, value='//*[@id="user_name"]').send_keys(mail)
    driver.find_element(by=By.XPATH, value='//*[@id="password_pass"]').send_keys(passs)


    errors = []
    invoicee = []
    roww=[]
    c=-1



    
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')    
    start = time.time()
    if(login_select.lower() =="a"):
        producer()
    elif(login_select.lower() =="b"):
        brand_owner()
    elif(login_select.lower() =="c"):
        importer()
    else:
        print("PLEASE ENTER CORRECT CHOICE")
    end = time.time()
    print("The time of execution of program is :",
      (end-start), "s")
    if(len(errors)>0):
        now = datetime.datetime.now()
        df2 = pd.DataFrame({'Errors': errors,
                           'Invoice no': invoicee,
                           'Row no':roww,
                   })
        df2.to_excel('errors'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print(df2)
    else:
        print("ALL DATA INPUT SUCCESS")
    


def ahead3():
    global errors
    global invoicee
    global driver
    global roww
    driver = driver
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')
    driver.implicitly_wait(15)
    errors = []
    invoicee = []
    roww=[]
    c=-1
    start = time.time()
    if(login_select.lower() =="a"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/producer-list')
        driver.refresh()
        producer()
    elif(login_select.lower() =="b"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/bo-list')
        driver.refresh()
        brand_owner()
    elif(login_select.lower() =="c"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/importer-list')
        driver.refresh()
        importer()
    else:
        print("PLEASE ENTER CORRECT CHOICE")
    end = time.time()
    print("The time of execution of program is :",
      (end-start), "s")
    if(len(errors)>0):
        now = datetime.datetime.now()
        df2 = pd.DataFrame({'Errors': errors,
                           'Invoice no': invoicee,
                           'Row no':roww,
                   })
        df2.to_excel('errors'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print(df2)
    else:
        print("ALL DATA INPUT SUCCESS")

def error():
    if(len(errors)>0):
        now = datetime.datetime.now()
        df2 = pd.DataFrame({'Errors': errors,
                           'Invoice no': invoicee,
                           'Row no':roww,
                   })
        df2.to_excel('errors'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print(df2)
    else:
        print("ALL DATA INPUT SUCCESS")


def custom_wait_clickable_and_click(elem, attempts=20):
    count = 0
    a='no success'
    while count < attempts:
        try:
            if(a!='success'):
                elem.click()
                a='success'
            elif(a=='success'):
                break
        except:
            time.sleep(1)
            count = count + 1

def pdf_gen(a,b,c,d,e,f,g,h,i,j):
    my_doc = SimpleDocTemplate("table.pdf", pagesize = letter)
    my_obj = []
    # defining Data to be stored on table
    my_data = [
       ["Information", 'Details'],
       ["EPR Invoice no.", a],
       ["Customer Registeration Type", b],
       ["Entity Type", c],
       ["Name of Entity", d],
       ["Plastic Material Type", e],
       ["Other Plastic Material Type", f],
       ["Category of Plastic", g],
       ["Financial Year", h],
       ["Quantity (TPA)", i],
       ["GST Paid", j],
    ]
    # Creating the table with 3 rows
    my_table = Table(my_data, 1 * [3.5 * inch], 11 * [0.5 * inch])
    # setting up style and alignments of borders and grids
    my_table.setStyle(
       TableStyle(
           [
               
               ("ALIGN", (-1, -1), (-1, -1), "LEFT"),
               ("VALIGN", (-1, -1), (-1, -1), "BOTTOM"),
               ("ALIGN", (-1, -1), (-1, -1), "LEFT"),
               ("VALIGN", (-1, -1), (-1, -1), "BOTTOM"),
               ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
               ("BOX", (0, 0), (-1, -1), 1, colors.black),
               ('BACKGROUND',(0,0),(1,0),colors.lightblue),
           ]
       )
    )
    my_obj.append(my_table)
    my_doc.build(my_obj)


def pdf_upload():
    global errors
    global invoicee
    global roww
    now = datetime.datetime.now()
    directory = str(now.strftime("final_pdf"+"%d%m%Y %H%M%S"))
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)

    os.mkdir(path)  
    parent_dir = path.replace('\\','/')
    parent_dir


    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a newly created record file')
    files = fd.askopenfilenames(parent=root, title='Choose merged pdf files')
    root.destroy()
    df = pd.DataFrame(list(files), columns =['file_path'])
    df1 = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df1.columns = (x.lower() for x in df1.columns)
    df['file_name']=0
    for i in range(len(df)):
        file2 = df['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0].split(".PDF")[0]
        df['file_name'][i]=file_name
    for i in range(len(df1)):
        print(i)
        pdf_gen(df1['epr invoice number'][i], df1['registration type'][i], df1['entity type'][i], df1['name of entity'][i], df1['plastic material type'][i], df1['other plastic material type'][i], df1['category of plastic'][i], df1['financial year'][i], round(df1['quantity (tpa)'][i], 3), df1['gst paid'][i])
        #plastic packaging qty, %of recyl plastic
        #remove entity type
        mergedObject = PdfMerger()
        mergedObject.append(PdfReader("table.pdf", 'rb'))
        pdf_file_index = df[df['file_name']==df1['pdf_filename'][i]].index[0]
        mergedObject.append(PdfReader(df['file_path'][pdf_file_index], 'rb'))
        filename = parent_dir+'/'+df1['pdf_filename'][i] + '.pdf'
        mergedObject.write(filename)

    print("ALL FILES GENERATED SUCCESSFULLY, PLEASE CHECK YOUR FOLDER-",parent_dir)

# def pdf_upload2():
#     driver.implicitly_wait(3)
#     global errors
#     global invoicee
#     errors = []
#     invoicee = []
#     #Finding epr invoice number using scrapping
#     ssa=easygui.enterbox("OPEN THE PAGE ON PORTAL WHERE YOU WANT TO UPLOAD PDF AND THEN PRESS OK")
#     job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
#     soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
#     a=soup.find_all("span",class_="ng-star-inserted")
#     z=[]
#     for i in a:
#     #     print(i.text.replace("\n","").strip())
#         z.append(i.text.replace("\n","").strip())

#     EPR=[]

#     i=0
#     while i<len(z):
#         EPR.append(z[i+14])
#         i=i+19

#     df3 = pd.DataFrame({
#                    'epr_no': EPR,
#                    })
#     print(df3)
    
#     #Upload Invoice / GST E-Invoice
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose a record file')
#     file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
#     root.destroy()
#     df1 = pd.DataFrame(list(file2), columns =['file_path'])
#     df1['file_name']=0
#     for i in range(len(df1)):
#         file2 = df1['file_path'][i].split("/")
#         file_name = file2[-1].split(".pdf")[0]
#         file_name = file_name.split(".PDF")[0]
#         df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
#     for i in range(0,50):
#     # for i in range(1):
#         try:
#             IndexForUpload = df[df['epr invoice number']==int(df3['epr_no'][i])].index[0]
#             click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(i+1)+']/td[17]/span')))
#             custom_wait_clickable_and_click(click)
#             upload_file = driver.find_element(by=By.XPATH, value='//*[@id="salesInvoiceUpload"]')
#             pdfindex = df1[df1['file_name']==str(df['pdf_filename'][IndexForUpload])].index[0]
#             pdf_file = df1['file_path'][pdfindex]
#             upload_file.send_keys(pdf_file)
#             time.sleep(2)
#             upload = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[1]')))
#             custom_wait_clickable_and_click(upload)                              
#             time.sleep(1)
#         except:
#             errors.append('Invoice upload error')
#             invoicee.append(str(df['Invoice Number'][i]))
#             try:
#                 close = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[2]').click()
#             except:
#                 pass
def pdf_upload2():
    root = tk.Tk()
    root.withdraw()

    # Open file dialog to select base file
    file_path = fd.askopenfilename(parent=root, title='Choose base file')

    # Open file dialog to select multiple PDF files
    pdf_paths = fd.askopenfilenames(parent=root, title='Choose PDF files')  # List of selected PDF file paths

    # Close the Tkinter root window after file selection
    root.destroy()

    # Process the selected files
    df = pd.read_excel(file_path)
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)

    date_from_value = driver.find_element(By.ID, 'date_from').get_attribute('value')
    date_to_value = driver.find_element(By.ID, 'date_to').get_attribute('value')

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    def find_pdf_by_filename(pdf_paths, pdf_filename):
        for pdf_path in pdf_paths:
            if os.path.basename(pdf_path) == f"{pdf_filename}.pdf":
                return pdf_path
        return None

    def upload_pdf_path(pdf_path, pdf_filename, sales_inc_id, registration_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': f'login-token={login_token}',
        }
        payload = {'section': 'upload_filepath'}
        files = [
            ('file', (f"{pdf_filename}.pdf", open(f'{pdf_path}', 'rb'), 'application/pdf'))
        ]
        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)
        path = response.json()["data"]["path"]

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/uploaded_invoice_receipts"

        payload = json.dumps({
            "type": registration_type.lower(),
            "path": f"{path}",
            "sales_inc_id": sales_inc_id
        })
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response)
        status = response.json()["status"]
        print(status, pdf_filename, sales_inc_id)

    def scrape_dashboard_data(pdf_paths):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_materials_sold"
        
        payload = json.dumps({
            "page": 1, 
            "records": 10000, 
            "filters": {}, 
            "page_count": 50, 
            "page_no": 1, 
            "no_of_records": 50, 
            "search_text": "", 
            "from_date": f"{date_from_value}", 
            "to_date": f"{date_to_value}", 
            "sortData": ""
        })
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        rows = response.json()["data"]["tableData"]["bodyContent"]

        entry_count = 0  # Counter for successfully uploaded entries
        
        for row in rows:
            registration_type = row["registration_type"]
            sales_inc_id = row["sales_inc_id"]
            b166 = int(row["invoice_no"])
            b177 = row["gst_e_invoice"]
            b188 = row["status"]

            if b188 == "pending":
                matching_row = df[df['epr invoice number'] == b166]

                if not matching_row.empty:  # Check if matching_row has data
                    pdf_filename = matching_row.iloc[0]['pdf_filename']

                    pdf_path = find_pdf_by_filename(pdf_paths, pdf_filename)
                    if pdf_path:
                        print(f"PDF found: {pdf_path}")
                        upload_pdf_path(pdf_path, pdf_filename, sales_inc_id, registration_type)
                        entry_count += 1  # Increment the counter after a successful upload
                else:
                    print(f"No matching record found for invoice number {b166}")

        print(f"Total entries processed: {entry_count}")  # Print the total count at the end

    scrape_dashboard_data(pdf_paths)
            
def producer():
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    
    errors = []
    
    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
    root.destroy()
    add1 = driver.find_elements(by=By.CLASS_NAME, value='btn-secondary')
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    count=0
    if(select.lower()=='b'):
        df['epr invoice number'] = "na"
        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            quantity = str(df['quantity (tpa)'][i])
            gst_no = df['gst number'][i]
            gst_paid = str(df['gst paid'][i])
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            account_no = df['bank account no'][i]
            ifsc = df['ifsc code'][i]
            cat_1 = df['cat-1 container capacity'][i]
            if cat_1:
                if cat_1.lower() == "Containers > 0.9L and < 4.9 L".lower():
                    container_type = 1
                elif cat_1.lower() == "Containers > 4.9 L".lower():
                    container_type = 2
                elif cat_1.lower() == "Containers < 0.9 L".lower():
                    container_type = 0
                else:
                    container_type = 5
            else:
                container_type = 5

            result = entity_type(entity, state, category, material_type)

            if result:
                entity_value, state_value, category_value, material_type_value = result

            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_sale_receipts"
            if registration_type.lower() == "unregistered":
                payload = json.dumps({
                    "type": registration_type.lower(),
                    "entity_type": entity_value,
                    "registered_entity_id": None,
                    "name": name,
                    "address": entity_address,
                    "entity_state_id": state_value,
                    "mobile": int(entity_mobile),
                    "financial_year": financial_year,
                    "gst_number": gst_no,
                    "account_no": account_no,
                    "ifsc": ifsc,
                    "gst_paid": gst_paid,
                    "quantity": quantity,
                    "gst_e_invoice": gst_e_invoice,
                    "plastic_category": category_value,
                    "recycled_plastic": recycled_plastic,
                    "container_type": container_type,
                    "plastic_type": material_type_value,
                    "epr_registration_number": None,
                    "invoice": "",
                    "company_id": 11579,
                    "not_registered": False,
                    "other_type": other_type if other_type else "",
                })
                response = requests.post(url, headers=headers, data=payload, verify=False)
                invoice_number = response.json().get("data", {}).get("invoice_number")

                if not invoice_number:
                    errors.append({
                        "gst_e_invoice": gst_e_invoice,
                        "status": "Your data is not uploaded."
                    })
                else:
                    print(f"Invoice number generated: {invoice_number}")
                
            else:
                registered_entity_id = entity_register_id(entity_value, name)
                if registered_entity_id:
                    payload = json.dumps({
                        "type": registration_type.lower(),
                        "financial_year": financial_year,
                        "account_no": account_no,
                        "ifsc": ifsc,
                        "gst_paid": gst_paid,
                        "quantity": quantity,
                        "gst_e_invoice": gst_e_invoice,
                        "plastic_category": category_value,
                        "recycled_plastic": recycled_plastic,
                        "entity_type": entity_value,
                        "registered_entity_id": registered_entity_id,
                        "container_type": container_type,
                        "plastic_type": material_type_value,
                        "state": state_value,
                        "entity_state_id": state_value,
                        "address": "xyz",
                        "mobile": entity_mobile,
                        "gst_number": "27AAACY3846K1ZX",
                        "epr_registration_number": None,
                        "invoice": "",
                        "company_id": 11579,
                        "not_registered": False,
                        "other_type": other_type if other_type else ""
                    })
                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")

    #     i=-1
    #     while i < len(df)-1:
    #         print(i+2)
    #         fy=14
    #         driver.implicitly_wait(20)
    #         i=i+1
    #         #Add button
    #         try:
    #             time.sleep(0.5)
    #             add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div[2]/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
    #             custom_wait_clickable_and_click(add)
    #             time.sleep(1)
    #             #registration type
    # ##                try:
    #             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
    #             cl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #             custom_wait_clickable_and_click(cl)
    # #                     time.sleep(0.5)
    # ##                except:
    # ##                    errors.append('registeration error')
    # ##                    invoicee.append(str(df['invoice number'][i]))
    # ##                    roww.append(i+2)
    # ##                    pass

    #             if(df['registration type'][i].lower()=='registered'):
    #                 #Type
    #                 cl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
    #                 custom_wait_clickable_and_click(cl)


    #                 #financial year
    #                 try:
    #                     fy=0
    #                     time.sleep(0.5)
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
    # #                     time.sleep(0.5)
    #                 except:
    #                     errors.append('financial year error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #bank account no 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
    #                 except:
    #                     errors.append('bank account no error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #ifsc code 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
    #                 except:
    #                     errors.append('ifsc code error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #gst paid
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
    #                 except:
    #                     errors.append('gst paid error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #Total Quantity (Tons)
    #                 try:
    #                     qty = round(float(df['quantity (tpa)'][i]), 3)
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
    #                 except:             
    #                     errors.append('Total Quantity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #invoice number
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
    #                 except:                                     
    #                     errors.append('invoice number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    # #                     #Upload Invoice / GST E-Invoice
    # #                     try:
    # #                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
    # #                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
    # #                         pdf_file = df1['file_path'][pdf_file_index]
    # #                         upload_file.send_keys(pdf_file)
    # #                         time.sleep(1)
    # #                     except:
    # #                         errors.append('Invoice upload error')
    # #                         invoicee.append(str(df['invoice number'][i]))
    # #                         pass

    #                 #category of plastic
    #                 try:
    #                     if(df['category of plastic'][i].lower()=='cat iv'):
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                 #% of recycled plastic packaging
    #                         try:
    #                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
    #                         except:
    #                             errors.append('% of recycled plastic packaging error')
    #                             invoicee.append(str(df['invoice number'][i]))
    #                             pass    
    #                 except:
    #                     errors.append('category of plastic error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #entity type
    #                 try:
    #                     if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                         #cat-1 container capacity nn
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)

    #                 except:
    #                     errors.append('entity type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass


    #                 #plastic material type
    #                 try:
    #                     if(df['plastic material type'][i].lower()=='others'):
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
    #                         #other plastic material type nn
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #                 except:
    #                     errors.append('plastic material type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #Name of the Entity registered
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 time.sleep(5)


    # #                     #address nn
    # #                     try:
    # #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
    # #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys(df['address'][i])

    # #                     except:
    # #                         errors.append('Name of the Entity error')
    # #                         invoicee.append(str(df['invoice number'][i]))
    # #                         pass

    # #                     #state nn
    # #                     try:
    # #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/span[1]')))
    # #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    # #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
    # #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    # #                         custom_wait_clickable_and_click(cl)
    # #                     #   time.sleep(2)
    # #                     except:
    # #                         errors.append('state error')
    # #                         invoicee.append(str(df['invoice number'][i]))
    # #                         pass

    # #                     #GST nn
    # #                     try:
    # #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
    # #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
    # #                     except:
    # #                         errors.append('GST error')
    # #                         invoicee.append(str(df['invoice number'][i]))
    # #                         pass
    # #                     break

    # ########################################################################################################################
    #             else:

    #                 #Name of the Entity Unregistered
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #address
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #state
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         time.sleep(0.5)
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(2)
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('state error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #mobile number
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('mobile number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #financial year
    #                 try:
    #                     time.sleep(0.5)
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
    # #                     time.sleep(0.5)
    #                 except:
    #                     errors.append('financial year error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #GST
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
    #                 except:
    #                     errors.append('GST error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #bank account no
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
    #                 except:
    #                     errors.append('bank account no error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #ifsc code
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
    #                 except:
    #                     errors.append('ifsc code error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #gst paid
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
    #                 except:
    #                     errors.append('gst paid error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #Total Quantity (Tons)
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
    #                 except:
    #                     errors.append('Total Quantity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #Invoice number
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
    #                 except:
    #                     errors.append('invoice number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    # #                     #Upload Invoice / GST E-Invoice
    # #                     try:
    # #                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
    # #                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
    # #                         pdf_file = df1['file_path'][pdf_file_index]
    # #                         upload_file.send_keys(pdf_file)
    # #                         time.sleep(1)
    # #                     except:
    # #                         errors.append('Invoice upload error')
    # #                         invoicee.append(str(df['invoice number'][i]))
    # #                         roww.append(i+2)
    # #                         pass

    #                 #category of plastic
    #                 try:
    #                     if(df['category of plastic'][i].lower()=='cat iv'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                 #% of recycled plastic packaging
    #                         try:
    #                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
    #                         except:
    #                             errors.append('% of recycled plastic packaging error')
    #                             invoicee.append(str(df['invoice number'][i]))
    #                             roww.append(i+2)
    #                             pass    
    #                 except:
    #                     errors.append('category of plastic error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass

    #                 #entity type
    #                 try:
    #                     if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                         #cat-1 container capacity
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)

    #                 except:
    #                     errors.append('entity type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass


    #                 #plastic material type
    #                 try:
    #                     if(df['plastic material type'][i].lower()=='others'):
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
    #                         #other plastic material type
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #                 except:
    #                     errors.append('plastic material type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
    #                     pass


    #             #Submit
    #             try:
    #                 if(fy<14):
    #                     cl=WebDriverWait(driver, 3).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
    #                     custom_wait_clickable_and_click(cl)
    #                     time.sleep(0.5)
    #                     cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     time.sleep(1)
    #                     try:
    #                         try:
    #                             pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
    #                             pop.click()
    #                         except:
    #                             pass
    #                         close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span'))).click()
    # #                             custom_wait_clickable_and_click(close)  
    # #                             errors.append('Submit error')
    # #                             invoicee.append(str(df['invoice number'][i]))
    # #                             roww.append(i+2)
    #                     except:
    #                         pass
    #                 else:
    #                     raise error
    #             except:
    # ##                    try:
    #                 errors.append('Confirm error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 roww.append(i+2)
    #                 try:
    #                     close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
    #                     custom_wait_clickable_and_click(close)
    #                 except:
    #                     driver.refresh()
    #                     driver.refresh()
    #                     driver.implicitly_wait(15)
    #                     time.sleep(1)
    #                     close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    #                     custom_wait_clickable_and_click(close)
    #     #                 time.sleep(0.5)
    #                     nxt = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    #                     custom_wait_clickable_and_click(nxt)       

    #         except:
    #             driver.refresh()
    #             driver.refresh()
    #             driver.implicitly_wait(15)
    #             time.sleep(1)
    #             close = WebDriverWait(driver, 3).until(
    # EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    #             custom_wait_clickable_and_click(close)
    # #                 time.sleep(0.5)
    #             nxt = WebDriverWait(driver, 3).until(
    # EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    #             custom_wait_clickable_and_click(nxt)
    #             time.sleep(2)
    # ##                errors.append('add button error')
    # ##                invoicee.append(str(df['invoice number'][i]))
    #             i=i-1
    #             pass




    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select.lower()=='a'):
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=1
            driver.implicitly_wait(15)
            i=i+1
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            a = str(df['date of invoice'][i])[:8]
            d = a[:4] + '/' + a[4:6] + '/' + a[6:]
            datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
            datetime1 = datetime0.date()
            year = datetime.date.strftime(datetime1, '%Y-%m-%d')
            quantity = df['quantity (tpa)'][i]
            gst_no = df['gst number'][i]
            gst_paid = df['gst paid'][i]
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            pdf_filename = df['pdf_filename'][i]

            try:
                pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
            except:
                pdf_file_index = 0

            if pdf_file_index != 0:
                pdf_file = df1['file_path'][pdf_file_index]
                try:
                    invoice = pdf_path(pdf_file, pdf_filename)
                except:
                    invoice = ""
                if invoice:
                    result = entity_type(entity, state, category, material_type)

                    if result:
                        entity_value, state_value, category_value, material_type_value = result
                        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                        payload = json.dumps({
                            "registration_type": registration_type.lower(),
                            "entity_type": entity_value,
                            "registered_entity_id": None,
                            "registration_number": None,
                            "entity_state_id": state_value,
                            "entity_address": entity_address,
                            "entity_mobile": entity_mobile,
                            "plastic_type": material_type_value,
                            "plastic_category": category_value,
                            "financial_year": financial_year,
                            "year": year,
                            "quantity": quantity,
                            "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                            "gst_no": gst_no,
                            "gst_paid": float(gst_paid),
                            "invoice": invoice,
                            "invoice_number": None,
                            "entity_country": "India",
                            "name": name,
                            "address": "",
                            "gst_e_invoice": gst_e_invoice,
                            "user_id": 15677,
                            "company_id": 15677,
                            "other_type": other_type if other_type else "",
                        })

                        response = requests.post(url, headers=headers, data=payload, verify=False)
                        invoice_number = response.json().get("data", {}).get("invoice_number")

                        # Check if invoice number was generated
                        if not invoice_number:
                            errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
                        else:
                            print(f"Invoice number generated: {invoice_number}")
                else:
                    errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })


            



# def producer():
#     action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-producer-list/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
#     custom_wait_clickable_and_click(action)
#     time.sleep(1)
#     close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#     custom_wait_clickable_and_click(close)
#     time.sleep(1)
#     nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#     custom_wait_clickable_and_click(nxt)
#     select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose base file')
#     file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
#     root.destroy()
#     add1 = driver.find_elements(by=By.CLASS_NAME, value='btn-secondary')
#     df1 = pd.DataFrame(list(file2), columns =['file_path'])
#     df1['file_name']=0
#     for i in range(len(df1)):
#         file2 = df1['file_path'][i].split("/")
#         file_name = file2[-1].split(".pdf")[0]
#         df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
#     df = df.astype(str)
#     df.columns = [x.lower() for x in df.columns]
#     count=0
#     if(select.lower()=='b'):
#         i=-1
#         while i < len(df)-1:
#             print(i+2)
#             fy=14
#             driver.implicitly_wait(20)
#             i=i+1
#             #Add button
#             try:
#                 time.sleep(0.5)
#                 add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div[2]/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
#                 custom_wait_clickable_and_click(add)
#                 time.sleep(1)
#                 #registration type
#     ##                try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
#                 cl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)
#     #                     time.sleep(0.5)
#     ##                except:
#     ##                    errors.append('registeration error')
#     ##                    invoicee.append(str(df['invoice number'][i]))
#     ##                    roww.append(i+2)
#     ##                    pass

#                 if(df['registration type'][i].lower()=='registered'):
#                     #Type
#                     cl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
#                     custom_wait_clickable_and_click(cl)


#                     #financial year
#                     try:
#                         fy=0
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #bank account no 
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #ifsc code 
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #gst paid
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Total Quantity (Tons)
#                     try:
#                         qty = round(float(df['quantity (tpa)'][i]), 3)
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
#                     except:             
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #invoice number
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
#                     except:                                     
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#     #                     #Upload Invoice / GST E-Invoice
#     #                     try:
#     #                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#     #                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#     #                         pdf_file = df1['file_path'][pdf_file_index]
#     #                         upload_file.send_keys(pdf_file)
#     #                         time.sleep(1)
#     #                     except:
#     #                         errors.append('Invoice upload error')
#     #                         invoicee.append(str(df['invoice number'][i]))
#     #                         pass

#                     #category of plastic
#                     try:
#                         if(df['category of plastic'][i].lower()=='cat iv'):
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                     #% of recycled plastic packaging
#                             try:
#                                 driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                             except:
#                                 errors.append('% of recycled plastic packaging error')
#                                 invoicee.append(str(df['invoice number'][i]))
#                                 pass    
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #entity type
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity nn
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass


#                     #plastic material type
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                             time.sleep(0.5)
#                             #other plastic material type nn
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Name of the Entity registered
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     time.sleep(5)


#     #                     #address nn
#     #                     try:
#     #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
#     #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys(df['address'][i])

#     #                     except:
#     #                         errors.append('Name of the Entity error')
#     #                         invoicee.append(str(df['invoice number'][i]))
#     #                         pass

#     #                     #state nn
#     #                     try:
#     #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/span[1]')))
#     #                         custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#     #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
#     #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#     #                         custom_wait_clickable_and_click(cl)
#     #                     #   time.sleep(2)
#     #                     except:
#     #                         errors.append('state error')
#     #                         invoicee.append(str(df['invoice number'][i]))
#     #                         pass

#     #                     #GST nn
#     #                     try:
#     #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
#     #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
#     #                     except:
#     #                         errors.append('GST error')
#     #                         invoicee.append(str(df['invoice number'][i]))
#     #                         pass
#     #                     break

#     ########################################################################################################################
#                 else:

#                     #Name of the Entity Unregistered
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #address
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #state
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             time.sleep(0.5)
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
#                             cl=WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(2)
#                         else:
#                             pass
#                     except:
#                         errors.append('state error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #mobile number
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
#                         else:
#                             pass
#                     except:
#                         errors.append('mobile number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #financial year
#                     try:
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #GST
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
#                     except:
#                         errors.append('GST error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #bank account no
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #ifsc code
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #gst paid
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #Total Quantity (Tons)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
#                     except:
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #Invoice number
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
#                     except:
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#     #                     #Upload Invoice / GST E-Invoice
#     #                     try:
#     #                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#     #                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#     #                         pdf_file = df1['file_path'][pdf_file_index]
#     #                         upload_file.send_keys(pdf_file)
#     #                         time.sleep(1)
#     #                     except:
#     #                         errors.append('Invoice upload error')
#     #                         invoicee.append(str(df['invoice number'][i]))
#     #                         roww.append(i+2)
#     #                         pass

#                     #category of plastic
#                     try:
#                         if(df['category of plastic'][i].lower()=='cat iv'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                     #% of recycled plastic packaging
#                             try:
#                                 driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                             except:
#                                 errors.append('% of recycled plastic packaging error')
#                                 invoicee.append(str(df['invoice number'][i]))
#                                 roww.append(i+2)
#                                 pass    
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #entity type
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass


#                     #plastic material type
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                             time.sleep(0.5)
#                             #other plastic material type
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass


#                 #Submit
#                 try:
#                     if(fy<14):
#                         cl=WebDriverWait(driver, 3).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
#                         custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
#                         cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
#                         custom_wait_clickable_and_click(cl)
#                         time.sleep(1)
#                         try:
#                             try:
#                                 pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
#                                 pop.click()
#                             except:
#                                 pass
#                             close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span'))).click()
#     #                             custom_wait_clickable_and_click(close)  
#     #                             errors.append('Submit error')
#     #                             invoicee.append(str(df['invoice number'][i]))
#     #                             roww.append(i+2)
#                         except:
#                             pass
#                     else:
#                         raise error
#                 except:
#     ##                    try:
#                     errors.append('Confirm error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     try:
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                     except:
#                         driver.refresh()
#                         driver.refresh()
#                         driver.implicitly_wait(15)
#                         time.sleep(1)
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#         #                 time.sleep(0.5)
#                         nxt = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#                         custom_wait_clickable_and_click(nxt)       

#             except:
#                 driver.refresh()
#                 driver.refresh()
#                 driver.implicitly_wait(15)
#                 time.sleep(1)
#                 close = WebDriverWait(driver, 3).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#                 custom_wait_clickable_and_click(close)
#     #                 time.sleep(0.5)
#                 nxt = WebDriverWait(driver, 3).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#                 custom_wait_clickable_and_click(nxt)
#                 time.sleep(2)
#     ##                errors.append('add button error')
#     ##                invoicee.append(str(df['invoice number'][i]))
#                 i=i-1
#                 pass




    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select.lower()=='a'):
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=1
            driver.implicitly_wait(15)
            i=i+1
            #Add button
            try:
                time.sleep(0.5)
                driver.implicitly_wait(15)
                add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div[2]/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(add)
                time.sleep(1)
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
                r_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(r_select)
    #             except:
    #                 errors.append('add button error')
    #                 pass

                #entity type
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    time.sleep(0.5)
                    et=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(et)
    #                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #state
                try:
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
    #                     time.sleep(2)
                except:
                    errors.append('state error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #address
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #mobile number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #category of plastic
                try:
                    if(df['category of plastic'][i].lower()=='cat iv'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                    else:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                #% of recycled plastic packaging
                        try:
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(str(df['recycled plastic %'][i]))
                        except:
                            errors.append('% of recycled plastic packaging error')
                            invoicee.append(str(df['invoice number'][i]))
                            roww.append(i+2)
                            pass    
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #financial year
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #DATE
                try:
                    a = str(df['date of invoice'][i])[:8]
                    d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                    datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                    datetime1 = datetime0.date()
                    datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Total Plastic Quantity
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #GST
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #gst paid
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
                except:
                    errors.append('gst paid error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #invoice number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
                except:
                    errors.append('invoice number error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Upload Invoice / GST E-Invoice
                try:
                    upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
                    pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
                    pdf_file = df1['file_path'][pdf_file_index]
                    upload_file.send_keys(pdf_file)
                    time.sleep(1)

                except:
                    errors.append('Invoice upload error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #plastic material type
                try:
                    if(df['plastic material type'][i].lower()=='others'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                        #other plastic material type
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
                    else:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                except:
                    errors.append('plastic material type error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Submit
                try:
                    if(fy>1):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                        custom_wait_clickable_and_click(cl)
                        time.sleep(0.5)
                        try:
                            try:
                                pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                                pop.click()
                            except:
                                pass
                            close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                            custom_wait_clickable_and_click(close)
                            errors.append('Submit error')
                            invoicee.append(str(df['invoice number'][i]))
                            roww.append(i+2)
                        except:
                            pass
                    else:
                        raise error
                except:
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
    ##                    try:
    ##                        pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
    ##                        pop.click()
    ##                    except:
    ##                        pass
                    close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    time.sleep(1)
            except:
                driver.refresh()
                driver.refresh()
                driver.implicitly_wait(15)
                time.sleep(1)
                close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
                time.sleep(0.5)
                nxt = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
                custom_wait_clickable_and_click(nxt)
    ##                errors.append('add button error')
    ##                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass

            


# def brand_owner():
#     global errors
#     global invoicee
#     global roww
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose base file')
#     file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
#     root.destroy()
#     df1 = pd.DataFrame(list(file2), columns =['file_path'])
#     df1['file_name']=0
#     for i in range(len(df1)):
#         file2 = df1['file_path'][i].split("/")
#         file_name = file2[-1].split(".pdf")[0]
#         df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
#     df = df.astype(str)
#     df.columns = [x.lower() for x in df.columns]
#     df['date of invoice']=df['date of invoice'].astype(str)
#     #     df['date of invoice'] = df['date of invoice'].apply(lambda x: x.replace("-", "/"))
#     driver.implicitly_wait(15)
#     continu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-bo-list/div[1]/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
#     custom_wait_clickable_and_click(continu)
#     time.sleep(0.5)
#     action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#     custom_wait_clickable_and_click(action)
#     time.sleep(0.5)
#     nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#     custom_wait_clickable_and_click(nxt)
#     i=-1
#     while i < len(df)-1:
#         print(i+2)
#         fy=1
#         driver.implicitly_wait(15)
#         i=i+1
#         #Add button
#         try:
#             time.sleep(1)
#             driver.implicitly_wait(15)
#             r_type = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
#             custom_wait_clickable_and_click(r_type)
#             time.sleep(1)
#             r_click = driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
#             r_select = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#             custom_wait_clickable_and_click(r_select)

#     #         except:
#     #             errors.append('add button error')
#     #             break



#             #Name of the Entity unregistred
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
#                 #driver.find_element(by=By.XPATH, value='').click()
#             except:
#                 errors.append('Name of the Entity error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #state
#             try:
#                 time.sleep(0.5)
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
#                 cl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)
# #                 time.sleep(2)
#             except:
#                 errors.append('state error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #address
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
#             except:
#                 errors.append('Name of the Entity error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #mobile number
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
#             except:
#                 errors.append('mobile number error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass



#             #financial year
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
#                 cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)
#                 fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[1]').text)
# #                 time.sleep(0.5)
#             except:
#                 errors.append('financial year error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #DATE
#             try:
#                 a = str(df['date of invoice'][i])[:8]
#                 d = a[:4]+'/'+a[4:6]+'/'+a[6:]
#                 datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
#                 datetime1 = datetime0.date()
#                 datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #Total Plastic Quantity
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #GST
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #gst paid
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
#             except:
#                 errors.append('gst paid error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #invoice number
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
#             except:
#                 errors.append('invoice number error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #Upload Invoice / GST E-Invoice
#             try:
#                 upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                 pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                 pdf_file = df1['file_path'][pdf_file_index]
#                 upload_file.send_keys(pdf_file)
#                 time.sleep(1)

#             except:
#                 errors.append('Invoice upload error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #category of plastic
#             try:
#                 if(df['category of plastic'][i].lower()=='cat iv'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1)
#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                     cl=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1)
#     #         #% of recycled plastic packaging
#     #                 try:
#     #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(int(df['recycled plastic %'][i]))
#     #                 except:
#     #                     errors.append('% of recycled plastic packaging error')
#     #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span').click()                    
#     #                     pass    
#             except:
#                 errors.append('category of plastic error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #entity type
#             try:
#                 if(df['category of plastic'][i].lower()=='cat i'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)
#                     #cat-1 container capacity
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1)
#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)

#             except:
#                 errors.append('entity type error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             #plastic material type
#             try:
#                 time.sleep(1)
#                 if(df['plastic material type'][i].lower()=='others'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     #other plastic material type
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
#     #                 try:
#     #                     #financial year and date
#     #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#     #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]').click()
#     #                     time.sleep(0.5)
#     #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
#     #                 except:
#     #                     pass
#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#             except:
#                 errors.append('plastic material type error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
#                 pass

#             try:
#                 if(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()=='cat i'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(datetime2)
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                 elif(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()!='cat i'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#                 elif(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others'):
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#             except:
#                 pass

#             #Submit
#             try:
#                 if(fy==0):
#                     cl=WebDriverWait(driver, 2).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
#                     custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
#                     try:
#                         try:
#                             pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
#                             pop.click()
#                         except:
#                             pass
#                         close = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                         errors.append('Submit error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                     except:
#                         pass
#                 else:
#                     raise error

#             except:
#                 errors.append('Submit error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 roww.append(i+2)
# ##                try:
# ##                    pop = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
# ##                    pop.click()
# ##                except:
# ##                    pass
#                 close = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
#                 custom_wait_clickable_and_click(close)
#         except:
#             driver.refresh()
#             driver.refresh()
#             driver.implicitly_wait(15)
#             time.sleep(1)
#             close = WebDriverWait(driver, 2).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#             custom_wait_clickable_and_click(close)
#             time.sleep(0.5)
#             nxt = WebDriverWait(driver, 2).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#             custom_wait_clickable_and_click(nxt)
# ##            errors.append('add button error')
# ##            invoicee.append(str(df['invoice number'][i]))
#             i=i-1
#             pass
            


        

def brand_owner():
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    errors = []

    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
    root.destroy()
    add1 = driver.find_elements(by=By.CLASS_NAME, value='btn-secondary')
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    count=0
    if(select.lower()=='b'):
        df['epr invoice number'] = "na"
        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            quantity = str(df['quantity (tpa)'][i])
            gst_no = df['gst number'][i]
            gst_paid = str(df['gst paid'][i])
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            account_no = df['bank account no'][i]
            ifsc = df['ifsc code'][i]
            cat_1 = df['cat-1 container capacity'][i]
            if cat_1:
                if cat_1.lower() == "Containers > 0.9L and < 4.9 L".lower():
                    container_type = 1
                elif cat_1.lower() == "Containers > 4.9 L".lower():
                    container_type = 2
                elif cat_1.lower() == "Containers < 0.9 L".lower():
                    container_type = 0
                else:
                    container_type = 5
            else:
                container_type = 5

            result = entity_type(entity, state, category, material_type)

            if result:
                entity_value, state_value, category_value, material_type_value = result

            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_sale_receipts"
            if registration_type.lower() == "unregistered":
                payload = json.dumps({
                    "type": registration_type.lower(),
                    "entity_type": entity_value,
                    "registered_entity_id": None,
                    "name": name,
                    "address": entity_address,
                    "entity_state_id": state_value,
                    "mobile": int(entity_mobile),
                    "financial_year": financial_year,
                    "gst_number": gst_no,
                    "account_no": account_no,
                    "ifsc": ifsc,
                    "gst_paid": gst_paid,
                    "quantity": quantity,
                    "gst_e_invoice": gst_e_invoice,
                    "plastic_category": category_value,
                    "recycled_plastic": recycled_plastic,
                    "container_type": container_type,
                    "plastic_type": material_type_value,
                    "epr_registration_number": None,
                    "invoice": "",
                    "company_id": 11579,
                    "not_registered": False,
                    "other_type": other_type if other_type else "",
                })
                response = requests.post(url, headers=headers, data=payload, verify=False)
                invoice_number = response.json().get("data", {}).get("invoice_number")

                if not invoice_number:
                    errors.append({
                        "gst_e_invoice": gst_e_invoice,
                        "status": "Your data is not uploaded."
                    })
                else:
                    print(f"Invoice number generated: {invoice_number}")
                
            else:
                registered_entity_id = entity_register_id(entity_value, name)
                if registered_entity_id:
                    payload = json.dumps({
                        "type": registration_type.lower(),
                        "financial_year": financial_year,
                        "account_no": account_no,
                        "ifsc": ifsc,
                        "gst_paid": gst_paid,
                        "quantity": quantity,
                        "gst_e_invoice": gst_e_invoice,
                        "plastic_category": category_value,
                        "recycled_plastic": recycled_plastic,
                        "entity_type": entity_value,
                        "registered_entity_id": registered_entity_id,
                        "container_type": container_type,
                        "plastic_type": material_type_value,
                        "state": state_value,
                        "entity_state_id": state_value,
                        "address": "xyz",
                        "mobile": entity_mobile,
                        "gst_number": "27AAACY3846K1ZX",
                        "epr_registration_number": None,
                        "invoice": "",
                        "company_id": 11579,
                        "not_registered": False,
                        "other_type": other_type if other_type else ""
                    })
                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")

    elif(select.lower()=='a'):
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=1
            driver.implicitly_wait(15)
            i=i+1
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            a = str(df['date of invoice'][i])[:8]
            d = a[:4] + '/' + a[4:6] + '/' + a[6:]
            datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
            datetime1 = datetime0.date()
            year = datetime.date.strftime(datetime1, '%Y-%m-%d')
            quantity = df['quantity (tpa)'][i]
            gst_no = df['gst number'][i]
            gst_paid = df['gst paid'][i]
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            pdf_filename = df['pdf_filename'][i]
            print(pdf_filename)
            try:
                pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
            except:
                pdf_file_index = 0
            if pdf_file_index != 0:
                pdf_file = df1['file_path'][pdf_file_index]
                print(pdf_file)
                try:
                    invoice = pdf_path(pdf_file, pdf_filename)
                except:
                    invoice = ""
                print(invoice)
                if invoice:
                    result = entity_type(entity, state, category, material_type)

                    if result:
                        entity_value, state_value, category_value, material_type_value = result
                        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                        payload = json.dumps({
                            "registration_type": registration_type.lower(),
                            "entity_type": entity_value,
                            "registered_entity_id": None,
                            "registration_number": None,
                            "entity_state_id": state_value,
                            "entity_address": entity_address,
                            "entity_mobile": entity_mobile,
                            "plastic_type": material_type_value,
                            "plastic_category": category_value,
                            "financial_year": financial_year,
                            "year": year,
                            "quantity": quantity,
                            "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                            "gst_no": gst_no,
                            "gst_paid": float(gst_paid),
                            "invoice": invoice,
                            "invoice_number": None,
                            "entity_country": "India",
                            "name": name,
                            "address": "",
                            "gst_e_invoice": gst_e_invoice,
                            "user_id": 15677,
                            "company_id": 15677,
                            "other_type": other_type if other_type else "",
                        })
                        print(payload)
                        response = requests.post(url, headers=headers, data=payload, verify=False)
                        print(response.text)
                        invoice_number = response.json().get("data", {}).get("invoice_number")

                        # Check if invoice number was generated
                        if not invoice_number:
                            errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
                        else:
                            print(f"Invoice number generated: {invoice_number}")
                else:
                    errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })

# def importer():
#     driver.implicitly_wait(1)
#     global errors
#     global invoicee
#     global roww

# #     action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-importer-list/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
# #     custom_wait_clickable_and_click(action)
# #     time.sleep(1)
# #     close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
# #     custom_wait_clickable_and_click(close)
# #     time.sleep(1)
# #     nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
# #     custom_wait_clickable_and_click(nxt)
#     select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose base file')
#     file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
#     root.destroy()
#     df1 = pd.DataFrame(list(file2), columns =['file_path'])
#     df1['file_name']=0
#     for i in range(len(df1)):
#         file2 = df1['file_path'][i].split("/")
#         file_name = file2[-1].split(".pdf")[0]
#         df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
#     df = df.astype(str)
#     df.columns = [x.lower() for x in df.columns]
#     count=0
#     if(select.lower()=='b'):
#         driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
#         i=-1
#         while i < len(df)-1:
#             print(i+2)
#             fy=14
            
#             i=i+1
#             #Add button
#             try:
#                 time.sleep(1)
#                 add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
#                 custom_wait_clickable_and_click(add)
#             #registration type
# ##                try:
#                 time.sleep(1)
#                 driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
#                 cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)


#                 if(df['registration type'][i].lower()=='registered'):
#                     #Type
#                     cl = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
#                     custom_wait_clickable_and_click(cl)


#                     #financial year
#                     try:
#                         fy=14
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #bank account no 
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #ifsc code 
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #gst paid
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Total Quantity (Tons)
#                     try:
#                         qty = round(float(df['quantity (tpa)'][i]), 3)
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
#                     except:
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #invoice number
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
#                     except:
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Upload Invoice / GST E-Invoice
#                     try:
#                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                         pdf_file = df1['file_path'][pdf_file_index]
#                         upload_file.send_keys(pdf_file)
#                         time.sleep(1)
#                     except:
#                         errors.append('Invoice upload error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #category of plastic
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(1.5)
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #entity type
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[3]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity nn
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[3]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
                

#                     #plastic material type
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                             time.sleep(0.5)
#                             #other plastic material type nn
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
                
#                     #Name of the Entity registered
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     time.sleep(5)
                    
                    
# #                     #address nn
# #                     try:
# #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
# #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys(df['address'][i])

# #                     except:
# #                         errors.append('Name of the Entity error')
# #                         invoicee.append(str(df['invoice number'][i]))
# #                         pass

# #                     #state nn
# #                     try:
# #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/span[1]')))
# #                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(0.5)
# #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
# #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
# #                         custom_wait_clickable_and_click(cl)
# #                     #   time.sleep(2)
# #                     except:
# #                         errors.append('state error')
# #                         invoicee.append(str(df['invoice number'][i]))
# #                         pass

# #                     #GST nn
# #                     try:
# #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
# #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
# #                     except:
# #                         errors.append('GST error')
# #                         invoicee.append(str(df['invoice number'][i]))
# #                         pass
# #                     break
                    
# ########################################################################################################################
#                 else:
                
#                     #Name of the Entity unregistred
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
#                         #driver.find_element(by=By.XPATH, value='').click()
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #address
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #state
#                     try:
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                       time.sleep(2)
#                     except:
#                         errors.append('state error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #mobile number
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
#                     except:
#                         errors.append('mobile number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #financial year
#                     try:
#                         fy=14
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #GST
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
#                     except:
#                         errors.append('GST error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #bank account no
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(str(df['bank account no'][i]))
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #ifsc code
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #gst paid
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(str(df['gst paid'][i]))
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #Total Quantity (Tons)
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
#                     except:
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass



#                     #invoice number
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
#                     except:
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #Upload Invoice / GST E-Invoice
#                     try:
#                         upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                         pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                         pdf_file = df1['file_path'][pdf_file_index]
#                         upload_file.send_keys(pdf_file)
#                     except:
#                         errors.append('Invoice upload error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #category of plastic
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(1)
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass

#                     #entity type
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass


#                     #plastic material type
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                             #other plastic material type
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         roww.append(i+2)
#                         pass
# #                 break
#                 #Submit
#                 try:
#                     if(fy<14):
#                         cl=WebDriverWait(driver, 3).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
#                         custom_wait_clickable_and_click(cl)
#                         cl=WebDriverWait(driver, 3).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
#                         custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
#                         try:
#                             try:
#                                 pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
#                                 pop.click()
#                             except:
#                                 pass
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
#                             errors.append('Submit error')
#                             invoicee.append(str(df['invoice number'][i]))
#                             roww.append(i+2)
#                         except:
#                             pass
#                     else:
#                         raise error

#                 except:
#                     errors.append('Submit error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     try:
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                         pass
#                     except:
#                         driver.refresh()
#                         driver.refresh()
#                         driver.implicitly_wait(10)
#                         time.sleep(1)
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                         time.sleep(0.5)
#             except:
#                 driver.refresh()
#                 driver.refresh()
#                 driver.implicitly_wait(10)
#                 time.sleep(1)

#     ##                errors.append('add button error')
#     ##                invoicee.append(str(df['invoice number'][i]))
#                 i=i-1
#                 pass


#     #----------------------------------------------------------------------------------------------------------------------    
#     #----------------------------------------------------------------------------------------------------------------------    
#     #----------------------------------------------------------------------------------------------------------------------     
#     elif(select.lower()=='a'):
#         df['date of invoice']=df['date of invoice'].astype(str)
#         driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
#         i=-1
#         while i < len(df)-1:
#             print(i+2)
#             fy=14
            
#             i=i+1
#             #Add button
#             try:
#                 time.sleep(1)
#                 driver.implicitly_wait(15)
#                 r_type = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
#                 custom_wait_clickable_and_click(r_type)
# #                 time.sleep(0.5)
#                 r_click = driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
# #                 time.sleep(0.5)
#                 r_select = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(r_select)

#     #                 except:
#     #                     errors.append('add button error')
#     #                     break

#                 #entity type
#                 try:
#                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)
#                 except:
#                     errors.append('entity type error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #Name of the Entity unregistred
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
#                     #driver.find_element(by=By.XPATH, value='').click()
#                 except:
#                     errors.append('Name of the Entity error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #country
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/div/div/div[2]/input').send_keys(df['country'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
#                 except:
#                     errors.append('country error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #address
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
#                 except:
#                     errors.append('Name of the Entity error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #mobile number
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
#                 except:
#                     errors.append('mobile number error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #category of plastic
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1)
#                 except:
#                     errors.append('category of plastic error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #financial year
#                 try:
#                     fy=14
#                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
#                     fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
# #                     time.sleep(0.5)
#                 except:
#                     errors.append('financial year error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #DATE
#                 try:
#                     a = str(df['date of invoice'][i])[:8]
#                     d = a[:4]+'/'+a[4:6]+'/'+a[6:]
#                     datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
#                     datetime1 = datetime0.date()
#                     datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
#                 except:
#                     errors.append('GST error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #Total Plastic Quantity
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
#                 except:
#                     errors.append('GST error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #invoice number
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(df['invoice number'][i])
#                 except:
#                     errors.append('invoice number error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #Upload Invoice / GST E-Invoice
#                 try:
#                     upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                     pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                     pdf_file = df1['file_path'][pdf_file_index]
#                     upload_file.send_keys(pdf_file)

#                 except:
#                     errors.append('Invoice upload error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #plastic material type
#                 try:
#                     if(df['plastic material type'][i].lower()=='others'):
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(0.5)
#                         #other plastic material type
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
#                     else:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(0.5)
#                 except:
#                     errors.append('plastic material type error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     pass

#                 #Submit
#                 try:
#                     if(fy<14):
#                         cl=WebDriverWait(driver, 3).until(
#         EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
#                         custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
#                         try:
#                             try:
#                                 pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
#                                 pop.click()
#                             except:
#                                 pass
#                             driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
#                             errors.append('Submit error')
#                             invoicee.append(str(df['invoice number'][i]))
#                             roww.append(i+2)
#                         except:
#                             pass
#                     else:
#                         raise error

#                 except:
#                     errors.append('Submit error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
#                     try:
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                         pass
#                     except:
#                         driver.refresh()
#                         driver.refresh()
#                         driver.implicitly_wait(10)
#                         time.sleep(1)
#                         close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
#                         custom_wait_clickable_and_click(close)
#                         time.sleep(0.5)
#             except:
#                 driver.refresh()
#                 driver.refresh()
#                 driver.implicitly_wait(10)
#                 time.sleep(1)

#     ##                errors.append('add button error')
#     ##                invoicee.append(str(df['invoice number'][i]))
#                 i=i-1
#                 pass


# ###################################################################################################################################################################################
def importer():
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    errors = []

    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
    root.destroy()
    add1 = driver.find_elements(by=By.CLASS_NAME, value='btn-secondary')
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    count=0
    if(select.lower()=='b'):
        df['epr invoice number'] = "na"
        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            quantity = str(df['quantity (tpa)'][i])
            gst_no = df['gst number'][i]
            gst_paid = str(df['gst paid'][i])
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            account_no = df['bank account no'][i]
            ifsc = df['ifsc code'][i]
            cat_1 = df['cat-1 container capacity'][i]
            if cat_1:
                if cat_1.lower() == "Containers > 0.9L and < 4.9 L".lower():
                    container_type = 1
                elif cat_1.lower() == "Containers > 4.9 L".lower():
                    container_type = 2
                elif cat_1.lower() == "Containers < 0.9 L".lower():
                    container_type = 0
                else:
                    container_type = 5
            else:
                container_type = 5

            result = entity_type(entity, state, category, material_type)

            if result:
                entity_value, state_value, category_value, material_type_value = result

            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_sale_receipts"
            if registration_type.lower() == "unregistered":
                payload = json.dumps({
                    "type": registration_type.lower(),
                    "entity_type": entity_value,
                    "registered_entity_id": None,
                    "name": name,
                    "address": entity_address,
                    "entity_state_id": state_value,
                    "mobile": int(entity_mobile),
                    "financial_year": financial_year,
                    "gst_number": gst_no,
                    "account_no": account_no,
                    "ifsc": ifsc,
                    "gst_paid": gst_paid,
                    "quantity": quantity,
                    "gst_e_invoice": gst_e_invoice,
                    "plastic_category": category_value,
                    "recycled_plastic": recycled_plastic,
                    "container_type": container_type,
                    "plastic_type": material_type_value,
                    "epr_registration_number": None,
                    "invoice": "",
                    "company_id": 11579,
                    "not_registered": False,
                    "other_type": other_type if other_type else "",
                })
                response = requests.post(url, headers=headers, data=payload, verify=False)
                invoice_number = response.json().get("data", {}).get("invoice_number")

                if not invoice_number:
                    errors.append({
                        "gst_e_invoice": gst_e_invoice,
                        "status": "Your data is not uploaded."
                    })
                else:
                    print(f"Invoice number generated: {invoice_number}")
                
            else:
                registered_entity_id = entity_register_id(entity_value, name)
                if registered_entity_id:
                    payload = json.dumps({
                        "type": registration_type.lower(),
                        "financial_year": financial_year,
                        "account_no": account_no,
                        "ifsc": ifsc,
                        "gst_paid": gst_paid,
                        "quantity": quantity,
                        "gst_e_invoice": gst_e_invoice,
                        "plastic_category": category_value,
                        "recycled_plastic": recycled_plastic,
                        "entity_type": entity_value,
                        "registered_entity_id": registered_entity_id,
                        "container_type": container_type,
                        "plastic_type": material_type_value,
                        "state": state_value,
                        "entity_state_id": state_value,
                        "address": "xyz",
                        "mobile": entity_mobile,
                        "gst_number": "27AAACY3846K1ZX",
                        "epr_registration_number": None,
                        "invoice": "",
                        "company_id": 11579,
                        "not_registered": False,
                        "other_type": other_type if other_type else ""
                    })
                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")

    elif(select.lower()=='a'):
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=1
            driver.implicitly_wait(15)
            i=i+1
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            a = str(df['date of invoice'][i])[:8]
            d = a[:4] + '/' + a[4:6] + '/' + a[6:]
            datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
            datetime1 = datetime0.date()
            year = datetime.date.strftime(datetime1, '%Y-%m-%d')
            quantity = df['quantity (tpa)'][i]
            gst_no = df['gst number'][i]
            gst_paid = df['gst paid'][i]
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            pdf_filename = df['pdf_filename'][i]
            print(pdf_filename)
            try:
                pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
            except:
                pdf_file_index = 0
            if pdf_file_index != 0:
                pdf_file = df1['file_path'][pdf_file_index]
                print(pdf_file)
                try:
                    invoice = pdf_path(pdf_file, pdf_filename)
                except:
                    invoice = ""
                print(invoice)
                if invoice:
                    result = entity_type(entity, state, category, material_type)

                    if result:
                        entity_value, state_value, category_value, material_type_value = result
                        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                        payload = json.dumps({
                            "registration_type": registration_type.lower(),
                            "entity_type": entity_value,
                            "registered_entity_id": None,
                            "registration_number": None,
                            "entity_state_id": state_value,
                            "entity_address": entity_address,
                            "entity_mobile": entity_mobile,
                            "plastic_type": material_type_value,
                            "plastic_category": category_value,
                            "financial_year": financial_year,
                            "year": year,
                            "quantity": quantity,
                            "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                            "gst_no": gst_no,
                            "gst_paid": float(gst_paid),
                            "invoice": invoice,
                            "invoice_number": None,
                            "entity_country": "India",
                            "name": name,
                            "address": "",
                            "gst_e_invoice": gst_e_invoice,
                            "user_id": 15677,
                            "company_id": 15677,
                            "other_type": other_type if other_type else "",
                        })
                        print(payload)
                        response = requests.post(url, headers=headers, data=payload, verify=False)
                        print(response.text)
                        invoice_number = response.json().get("data", {}).get("invoice_number")

                        # Check if invoice number was generated
                        if not invoice_number:
                            errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
                        else:
                            print(f"Invoice number generated: {invoice_number}")
                else:
                    errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })

def scrape():
    a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    stop=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[2]/table/tbody/tr/td/div[1]/div/span').text
    res = [int(i) for i in stop.split() if i.isdigit()]
    stop=res[-1]
    stop=stop/50
    stop=math.ceil(stop)
    print(stop)
    count=0
    df = pd.DataFrame()
    while count<stop:
        a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p,p1=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        try:
            time.sleep(1)
            count=count+1
            job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
            soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
            a=soup.find_all("span",class_="ng-star-inserted")
            if(len(a)==0):
                a=soup.find_all("td",class_="row-item")
            z=[]
            for i in a:
            #     print(i.text.replace("\n","").strip())
                z.append(i.text.replace("\n","").strip())
            i=0
            if(count==stop):
                while i<len(z):
                    a2.append(z[i])
                    b.append(z[i+1])
                    c.append(z[i+2])
                    d.append(z[i+3])
                    e.append(z[i+4])
                    f.append(z[i+5])
                    g.append(z[i+6])
                    h.append(z[i+7])
                    i2.append(z[i+8])
                    j.append(z[i+9])
                    k.append(z[i+10])
                    l.append(z[i+11])
                    m.append(z[i+12])
                    n.append(z[i+13])
                    o.append(z[i+14])
                    p.append(z[i+15])
                    p1.append(a[i+16])
                    if((len(z[16])==0) & (len(z[17])==0) & (len(z[18])==0)):
                        i=i+19
                    elif(len(z[16])==0 and len(z[17])==0):
                        i=i+18
                    else:
                        i=i+16
                    print(i)
                df1 = pd.DataFrame({
                           'Registration Type': a2,
                           'Entity Type': b,
                           'Name of the Entity': c,
                           'State': d,
                           'Address': e,
                           'Mobile Number': f,
                           'Plastic Material Type': g,
                           'Category of Plastic': h,
                           'Financial Year': i2,
                           'Date': j,
                           'Total Plastic Qty (Tons)': k,
                           'Recycled Plastic %': l,
                           'GST': m,
                           'GST Paid': n,
                           'EPR invoice No': o,
                           'GST E-Invoice No': p,
##                               'upload status': p1
                           })
                df = pd.concat([df, df1],ignore_index=True)

            else:
                while i<len(z):
                    a2.append(z[i])
                    b.append(z[i+1])
                    c.append(z[i+2])
                    d.append(z[i+3])
                    e.append(z[i+4])
                    f.append(z[i+5])
                    g.append(z[i+6])
                    h.append(z[i+7])
                    i2.append(z[i+8])
                    j.append(z[i+9])
                    k.append(z[i+10])
                    l.append(z[i+11])
                    m.append(z[i+12])
                    n.append(z[i+13])
                    o.append(z[i+14])
                    p.append(z[i+15])
                    p1.append(a[i+16])
                    if((len(z[16])==0) & (len(z[17])==0) & (len(z[18])==0)):
                        i=i+19
                    elif(len(z[16])==0 and len(z[17])==0):
                        i=i+18
                    else:
                        i=i+16
                    print(i)
                df1 = pd.DataFrame({
                           'Registration Type': a2,
                           'Entity Type': b,
                           'Name of the Entity': c,
                           'State': d,
                           'Address': e,
                           'Mobile Number': f,
                           'Plastic Material Type': g,
                           'Category of Plastic': h,
                           'Financial Year': i2,
                           'Date': j,
                           'Total Plastic Qty (Tons)': k,
                           'Recycled Plastic %': l,
                           'GST': m,
                           'GST Paid': n,
                           'EPR invoice No': o,
                           'GST E-Invoice No': p,
##                               'upload status': p1
                           })
                if(count==1):
                    comp= pd.DataFrame({'aa':['0']})
                else:
                    new = df.tail(50).reset_index()
                    new = new.drop(['index'], axis=1)
                    comp=new.compare(df1)
                if(comp.empty==False):
                    df = pd.concat([df, df1],ignore_index=True)
                    nextt = driver.find_elements(by=By.CLASS_NAME, value='action-button')[1]
                    custom_wait_clickable_and_click(nextt)
                    click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                    custom_wait_clickable_and_click(click)
                    time.sleep(1)
                else:
                    df.to_excel('Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
                    break
        except:
            break
    now = datetime.datetime.now()
    df.to_excel('Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
    print("Your file is generated by name - "+'Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        

button1 = tk.Button(text='open browser', command=hello, bg='brown',fg='white')
canvas1.create_window(75, 75, window=button1)
button4 = tk.Button(text='Continue', command=ahead3, bg='brown',fg='white')
canvas4.create_window(75, 75, window=button4)
button5 = tk.Button(text='Generate pdfs', command=pdf_upload, bg='brown',fg='white')
canvas5.create_window(75, 75, window=button5)
button6 = tk.Button(text='Upload pdfs', command=pdf_upload2, bg='brown',fg='white')
canvas6.create_window(75, 75, window=button6)
button2 = tk.Button(text='show errors', command=error, bg='brown',fg='white')
canvas2.create_window(75, 75, window=button2)
button3 = tk.Button(text='Scrape details', command=scrape, bg='brown',fg='white')
canvas3.create_window(75, 75, window=button3)

root.mainloop()


