
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
import tkinter.filedialog as fd
import getpass
import time
import pandas as pd
import tkinter as tk
from bs4 import BeautifulSoup
import math
import easygui
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 180, height = 80)
canvas1.pack()
canvas4 = tk.Canvas(root, width = 180, height = 80)
canvas4.pack()
canvas2 = tk.Canvas(root, width = 180, height = 80)
canvas2.pack()
canvas3 = tk.Canvas(root, width = 180, height = 150)
canvas3.pack()


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
    #mail = 'goelabhishk@gmail.com'
    #passs = 'Abhi@1234'
    email = driver.find_element(by=By.XPATH, value='//*[@id="username"]')
    email.send_keys(mail)
    password = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
    password.send_keys(passs)
    login = driver.find_element(by=By.XPATH, value='//*[@id="signIn"]')
    login.click()
    time.sleep(4)
    
    otpp = easygui.enterbox("enter otp")
    otp = driver.find_element(by=By.XPATH, value='//*[@id="loginUserID"]').send_keys(otpp)
    driver.implicitly_wait(15)
    continu = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-plastic/div/app-admin-login/div/div/div/div[2]/div[2]/div/div[2]/form/div[2]/button').click()
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
            


def producer():
    action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-producer-list/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
    custom_wait_clickable_and_click(action)
    time.sleep(1)
    close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    custom_wait_clickable_and_click(close)
    time.sleep(1)
    nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    custom_wait_clickable_and_click(nxt)
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
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=14
            driver.implicitly_wait(20)
            i=i+1
            #Add button
            try:
                time.sleep(0.5)
                if(len(add1)>11):
                    custom_wait_clickable_and_click(add1[5])
                else:
                    custom_wait_clickable_and_click(add1[0])
                time.sleep(1)
                #registration type
    ##                try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                cl = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
    #                     time.sleep(0.5)
    ##                except:
    ##                    errors.append('registeration error')
    ##                    invoicee.append(str(df['invoice number'][i]))
    ##                    roww.append(i+2)
    ##                    pass

                if(df['registration type'][i].lower()=='registered'):
                    #Type
                    cl = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
                    custom_wait_clickable_and_click(cl)


                    #financial year
                    try:
                        fy=0
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #bank account no 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons)
                    try:
                        qty = round(float(df['quantity (tpa)'][i]), 3)
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
                    except:             
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
                    except:                                     
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

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

                    #category of plastic
                    try:
                        if(df['category of plastic'][i].lower()=='cat iv'):
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                    #% of recycled plastic packaging
                            try:
                                driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
                            except:
                                errors.append('% of recycled plastic packaging error')
                                invoicee.append(str(df['invoice number'][i]))
                                pass    
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass


                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Name of the Entity registered
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    time.sleep(5)


    #                     #address nn
    #                     try:
    #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
    #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys(df['address'][i])

    #                     except:
    #                         errors.append('Name of the Entity error')
    #                         invoicee.append(str(df['invoice number'][i]))
    #                         pass

    #                     #state nn
    #                     try:
    #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/span[1]')))
    #                         custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
    #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
    #                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    #                     #   time.sleep(2)
    #                     except:
    #                         errors.append('state error')
    #                         invoicee.append(str(df['invoice number'][i]))
    #                         pass

    #                     #GST nn
    #                     try:
    #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
    #                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
    #                     except:
    #                         errors.append('GST error')
    #                         invoicee.append(str(df['invoice number'][i]))
    #                         pass
    #                     break

    ########################################################################################################################
                else:

                    #Name of the Entity Unregistered
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #address
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #state
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            time.sleep(0.5)
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                            cl=WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(2)
                        else:
                            pass
                    except:
                        errors.append('state error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #mobile number
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                        else:
                            pass
                    except:
                        errors.append('mobile number error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #financial year
                    try:
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #GST
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                    except:
                        errors.append('GST error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #bank account no
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #ifsc code
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #Total Quantity (Tons)
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #Invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

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
    #                         roww.append(i+2)
    #                         pass

                    #category of plastic
                    try:
                        if(df['category of plastic'][i].lower()=='cat iv'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                        else:
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                    #% of recycled plastic packaging
                            try:
                                driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
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

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass


                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass


                #Submit
                try:
                    if(fy<14):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                        custom_wait_clickable_and_click(cl)
                        time.sleep(0.5)
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                        custom_wait_clickable_and_click(cl)
                        time.sleep(1)
                        try:
                            try:
                                pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                                pop.click()
                            except:
                                pass
                            close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span'))).click()
    #                             custom_wait_clickable_and_click(close)  
    #                             errors.append('Submit error')
    #                             invoicee.append(str(df['invoice number'][i]))
    #                             roww.append(i+2)
                        except:
                            pass
                    else:
                        raise error
                except:
    ##                    try:
                    errors.append('Confirm error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    try:
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                    except:
                        driver.refresh()
                        driver.refresh()
                        driver.implicitly_wait(15)
                        time.sleep(1)
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
        #                 time.sleep(0.5)
                        nxt = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
                        custom_wait_clickable_and_click(nxt)       

            except:
                driver.refresh()
                driver.refresh()
                driver.implicitly_wait(15)
                time.sleep(1)
                close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
    #                 time.sleep(0.5)
                nxt = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
                custom_wait_clickable_and_click(nxt)
                time.sleep(2)
    ##                errors.append('add button error')
    ##                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass




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
                add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, add1[0])))
                custom_wait_clickable_and_click(add)
                time.sleep(1)
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
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
            



def brand_owner():
    global errors
    global invoicee
    global roww
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['date of invoice']=df['date of invoice'].astype(str)
    #     df['date of invoice'] = df['date of invoice'].apply(lambda x: x.replace("-", "/"))
    driver.implicitly_wait(15)
    continu = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-bo-list/div[1]/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
    custom_wait_clickable_and_click(continu)
    time.sleep(0.5)
    action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    custom_wait_clickable_and_click(action)
    time.sleep(0.5)
    nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    custom_wait_clickable_and_click(nxt)
    i=-1
    while i < len(df)-1:
        print(i+2)
        fy=1
        driver.implicitly_wait(15)
        i=i+1
        #Add button
        try:
            time.sleep(1)
            driver.implicitly_wait(15)
            r_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
            custom_wait_clickable_and_click(r_type)
            time.sleep(1)
            r_click = driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
            r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
            custom_wait_clickable_and_click(r_select)

    #         except:
    #             errors.append('add button error')
    #             break



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
                cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
#                 time.sleep(2)
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



            #financial year
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
                fy=len(driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[1]').text)
#                 time.sleep(0.5)
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

            #category of plastic
            try:
                if(df['category of plastic'][i].lower()=='cat iv'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
                else:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                    cl=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
    #         #% of recycled plastic packaging
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(int(df['recycled plastic %'][i]))
    #                 except:
    #                     errors.append('% of recycled plastic packaging error')
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span').click()                    
    #                     pass    
            except:
                errors.append('category of plastic error')
                invoicee.append(str(df['invoice number'][i]))
                roww.append(i+2)
                pass

            #entity type
            try:
                if(df['category of plastic'][i].lower()=='cat i'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                    #cat-1 container capacity
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
                else:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)

            except:
                errors.append('entity type error')
                invoicee.append(str(df['invoice number'][i]))
                roww.append(i+2)
                pass

            #plastic material type
            try:
                time.sleep(1)
                if(df['plastic material type'][i].lower()=='others'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    #other plastic material type
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
    #                 try:
    #                     #financial year and date
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
    #                     driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]').click()
    #                     time.sleep(0.5)
    #                     driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
    #                 except:
    #                     pass
                else:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
            except:
                errors.append('plastic material type error')
                invoicee.append(str(df['invoice number'][i]))
                roww.append(i+2)
                pass

            try:
                if(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()=='cat i'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(datetime2)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['recycled plastic %'][i]))
                elif(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()!='cat i'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
                elif(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others'):
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
                else:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
            except:
                pass

            #Submit
            try:
                if(fy==0):
                    cl=WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    try:
                        try:
                            pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                            pop.click()
                        except:
                            pass
                        close = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
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
##                try:
##                    pop = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
##                    pop.click()
##                except:
##                    pass
                close = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
        except:
            driver.refresh()
            driver.refresh()
            driver.implicitly_wait(15)
            time.sleep(1)
            close = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
            custom_wait_clickable_and_click(close)
            time.sleep(0.5)
            nxt = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
            custom_wait_clickable_and_click(nxt)
##            errors.append('add button error')
##            invoicee.append(str(df['invoice number'][i]))
            i=i-1
            pass
            


        

def importer():
    driver.implicitly_wait(1)
    global errors
    global invoicee
    global roww

#     action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-importer-list/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
#     custom_wait_clickable_and_click(action)
#     time.sleep(1)
#     close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
#     custom_wait_clickable_and_click(close)
#     time.sleep(1)
#     nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
#     custom_wait_clickable_and_click(nxt)
    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose pdf files')
    root.destroy()
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
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=14
            
            i=i+1
            #Add button
            try:
                time.sleep(1)
                add = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
            #registration type
##                try:
                time.sleep(1)
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)


                if(df['registration type'][i].lower()=='registered'):
                    #Type
                    cl = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
                    custom_wait_clickable_and_click(cl)


                    #financial year
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #bank account no 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons)
                    try:
                        qty = round(float(df['quantity (tpa)'][i]), 3)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
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
                        pass

                    #category of plastic
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[3]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[3]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                

                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                
                    #Name of the Entity registered
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    time.sleep(5)
                    
                    
#                     #address nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys(df['address'][i])

#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #state nn
#                     try:
#                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/span[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
#                         cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                     #   time.sleep(2)
#                     except:
#                         errors.append('state error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #GST nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
#                     except:
#                         errors.append('GST error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
#                     break
                    
########################################################################################################################
                else:
                
                    #Name of the Entity unregistred
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                        #driver.find_element(by=By.XPATH, value='').click()
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #address
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #state
                    try:
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                       time.sleep(2)
                    except:
                        errors.append('state error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #mobile number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                    except:
                        errors.append('mobile number error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #financial year
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #GST
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                    except:
                        errors.append('GST error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #bank account no
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(str(df['bank account no'][i]))
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #ifsc code
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(str(df['gst paid'][i]))
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #Total Quantity (Tons)
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass



                    #invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
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
                    except:
                        errors.append('Invoice upload error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #category of plastic
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1)
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass


                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            #other plastic material type
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        roww.append(i+2)
                        pass
#                 break
                #Submit
                try:
                    if(fy<14):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                        custom_wait_clickable_and_click(cl)
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                        custom_wait_clickable_and_click(cl)
                        time.sleep(0.5)
                        try:
                            try:
                                pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                                pop.click()
                            except:
                                pass
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
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
                    try:
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                        pass
                    except:
                        driver.refresh()
                        driver.refresh()
                        driver.implicitly_wait(10)
                        time.sleep(1)
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                        time.sleep(0.5)
            except:
                driver.refresh()
                driver.refresh()
                driver.implicitly_wait(10)
                time.sleep(1)

    ##                errors.append('add button error')
    ##                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass


    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select.lower()=='a'):
        df['date of invoice']=df['date of invoice'].astype(str)
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
        i=-1
        while i < len(df)-1:
            print(i+2)
            fy=14
            
            i=i+1
            #Add button
            try:
                time.sleep(1)
                driver.implicitly_wait(15)
                r_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(r_type)
#                 time.sleep(0.5)
                r_click = driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
#                 time.sleep(0.5)
                r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(r_select)

    #                 except:
    #                     errors.append('add button error')
    #                     break

                #entity type
                try:
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #country
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/div/div/div[2]/input').send_keys(df['country'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                except:
                    errors.append('country error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #address
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #mobile number
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #category of plastic
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #financial year
                try:
                    fy=14
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
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
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Total Plastic Quantity
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #invoice number
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(df['invoice number'][i])
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

                except:
                    errors.append('Invoice upload error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #plastic material type
                try:
                    if(df['plastic material type'][i].lower()=='others'):
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                        #other plastic material type
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
                    else:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                except:
                    errors.append('plastic material type error')
                    invoicee.append(str(df['invoice number'][i]))
                    roww.append(i+2)
                    pass

                #Submit
                try:
                    if(fy<14):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                        custom_wait_clickable_and_click(cl)
                        time.sleep(0.5)
                        try:
                            try:
                                pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                                pop.click()
                            except:
                                pass
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
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
                    try:
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                        pass
                    except:
                        driver.refresh()
                        driver.refresh()
                        driver.implicitly_wait(10)
                        time.sleep(1)
                        close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                        time.sleep(0.5)
            except:
                driver.refresh()
                driver.refresh()
                driver.implicitly_wait(10)
                time.sleep(1)

    ##                errors.append('add button error')
    ##                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass


####################################################################################################################################################################################

def scrape():
    a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    stop=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[2]/table/tbody/tr/td/div[1]/div/span').text
    res = [int(i) for i in stop.split() if i.isdigit()]
    stop=res[-1]
    stop=stop/50
    stop=math.ceil(stop)
    print(stop)
    count=0
    while count<stop:
        try:
            
            count=count+1
            job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
            soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
            a=soup.find_all("span",class_="ng-star-inserted")
            z=[]
            for i in a:
            #     print(i.text.replace("\n","").strip())
                z.append(i.text.replace("\n","").strip())
            i=0
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
                if((len(z[16])==0) & (len(z[17])==0) & (len(z[18])==0)):
                    i=i+19
                elif(len(z[16])==0 and len(z[17])==0):
                    i=i+18
                else:
                    i=i+17
                print(i)
            df = pd.DataFrame({
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
                       })
            time.sleep(1)
            nextt = driver.find_elements(by=By.CLASS_NAME, value='action-button')[1]
            custom_wait_clickable_and_click(nextt)
            click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
            custom_wait_clickable_and_click(click)
            time.sleep(2)
        except:
            break
    df.to_excel('Scrapped_Data.xlsx')



button1 = tk.Button(text='open browser', command=hello, bg='brown',fg='white')
canvas1.create_window(75, 75, window=button1)
button4 = tk.Button(text='Continue', command=ahead3, bg='brown',fg='white')
canvas4.create_window(75, 75, window=button4)
button2 = tk.Button(text='show errors', command=error, bg='brown',fg='white')
canvas2.create_window(75, 75, window=button2)
button3 = tk.Button(text='Scrape details', command=scrape, bg='brown',fg='white')
canvas3.create_window(75, 75, window=button3)

root.mainloop()


