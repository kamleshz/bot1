
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
import easygui
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 200, height = 150)
canvas1.pack()
canvas4 = tk.Canvas(root, width = 200, height = 150)
canvas4.pack()
canvas2 = tk.Canvas(root, width = 200, height = 150)
canvas2.pack()


def hello ():
    global errors
    global invoicee
    global driver
    today = date.today()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')
    driver.implicitly_wait(40)
    continu = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-plastic/div/app-admin-login/div/div/div/div[2]/div[2]/div/div[2]/form/div[2]/button').click()
    errors = []
    invoicee = []
    c=-1

    start = time.time()
    if(login_select.lower() =="a"):
        producer(c)
    elif(login_select.lower() =="b"):
        brand_owner(c)
    elif(login_select.lower() =="c"):
        importer(c)
    else:
        print("PLEASE ENTER CORRECT CHOICE")
    end = time.time()
    print("The time of execution of program is :",
      (end-start), "s")
    if(len(errors)>0):
        now = datetime.datetime.now()
        df2 = pd.DataFrame({'Errors': errors,
                   'Invoice no': invoicee,
                   })
        df2.to_excel('errors'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print(df2)
    else:
        print("ALL DATA INPUT SUCCESS")
    


def ahead3():
    global errors
    global invoicee
    global driver
    driver = driver
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')
    driver.implicitly_wait(40)
    errors = []
    invoicee = []
    c=-1
    start = time.time()
    if(login_select.lower() =="a"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/producer-list')
        driver.refresh()
        producer(c)
    elif(login_select.lower() =="b"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/bo-list')
        driver.refresh()
        brand_owner(c)
    elif(login_select.lower() =="c"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/importer-list')
        driver.refresh()
        importer(c)
    else:
        print("PLEASE ENTER CORRECT CHOICE")
    end = time.time()
    print("The time of execution of program is :",
      (end-start), "s")
    if(len(errors)>0):
        now = datetime.datetime.now()
        df2 = pd.DataFrame({'Errors': errors,
                   'Invoice no': invoicee,
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
                   })
        df2.to_excel('errors'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print(df2)
    else:
        print("ALL DATA INPUT SUCCESS")


def custom_wait_clickable_and_click(elem, attempts=10):
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
            


def producer(c):
    global errors
    global invoicee
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
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False)
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    count=0
    if(select.lower()=='b'):
        for i in range(len(df)):
            driver.implicitly_wait(20)
            #Add button
            try:
                time.sleep(1)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div[2]/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(add)
                time.sleep(1)
    #             except:
    #                 errors.append('add button error')
    #                 pass
                #registration type
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                    cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('registeration error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass



                #Name of the Entity Unregistered
                try:
                    if(df['registration type'][i].lower()=='unregistered'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                    else:
                        pass
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
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
                    pass

                #state
                try:
                    if(df['registration type'][i].lower()=='unregistered'):
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
                    pass

                #financial year
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    time.sleep(0.5)
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #GST
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #bank account no
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
                except:
                    errors.append('bank account no error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #ifsc code
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                except:
                    errors.append('ifsc code error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #gst paid
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
                except:
                    errors.append('gst paid error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Quantity (Tons)
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('Total Quantity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass


                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[3]/div/input').send_keys(df['invoice number'][i])
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
                            pass    
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
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
                    pass
                
                
                #Name of the Entity registered
                try:
                    if(df['registration type'][i].lower()=='registered'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['name of entity'][i])
                        cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                    else:
                        pass
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass
                

                #Submit
                try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
    #             except:
    #                 errors.append('Submit error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #Confirm
    #             try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(1)
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div[2]/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                    custom_wait_clickable_and_click(cl)
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(cl)

                except:
                    try:
                        errors.append('Confirm error')
                        invoicee.append(str(df['invoice number'][i]))
                        cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                        custom_wait_clickable_and_click(cl)
                        cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('Confirm error')
                        invoicee.append(str(df['invoice number'][i]))
                        try:
                            pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                            pop.click()
                        except:
                            pass
                        close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                        custom_wait_clickable_and_click(close)
                        pass

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
                errors.append('add button error')
                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass




    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select=='a'):
        df['date of procurement']=df['date of procurement'].astype(str)
    #         df['date of procurement'] = df['date of procurement'].apply(lambda x: x.replace("-", "/"))
        #plastic raw material/packaging procured
        for i in range(len(df)):
            driver.implicitly_wait(15)

            #Add button
            try:
                time.sleep(1)
                driver.implicitly_wait(15)
                r_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(r_type)
#                 time.sleep(0.5)
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
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #state
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    time.sleep(0.5)
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(2)
                except:
                    errors.append('state error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #address
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #mobile number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
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
                            pass    
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #financial year
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #DATE
                try:
                    a = str(df['date of procurement'][i])[:8]
                    d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                    datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                    datetime1 = datetime0.date()
                    datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Plastic Quantity
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #GST
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #gst paid
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
                except:
                    errors.append('gst paid error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #invoice number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
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

                #plastic material type
                try:
                    time.sleep(1)
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
                    pass

                #Submit
                try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    add = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
                    custom_wait_clickable_and_click(add)
                    time.sleep(0.5)
                    pop = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                    pop.click()
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)

                except:
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    try:
                        pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                        pop.click()
                    except:
                        pass
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    pass
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
                errors.append('add button error')
                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass



def brand_owner(c):
    global errors
    global invoicee
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False)
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['date of procurement']=df['date of procurement'].astype(str)
    #     df['date of procurement'] = df['date of procurement'].apply(lambda x: x.replace("-", "/"))
    driver.implicitly_wait(15)
    continu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-bo-list/div[1]/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
    custom_wait_clickable_and_click(continu)
    time.sleep(0.5)
    action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    custom_wait_clickable_and_click(action)
    time.sleep(0.5)
    nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    custom_wait_clickable_and_click(nxt)
    for i in range(len(df)):
        driver.implicitly_wait(15)
        #Add button
        try:
            time.sleep(1)
            driver.implicitly_wait(15)
            r_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
            custom_wait_clickable_and_click(r_type)
            time.sleep(0.5)
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
                pass

            #state
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
#                 time.sleep(2)
            except:
                errors.append('state error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #address
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
            except:
                errors.append('Name of the Entity error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #mobile number
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
            except:
                errors.append('mobile number error')
                invoicee.append(str(df['invoice number'][i]))
                pass



            #financial year
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
#                 time.sleep(0.5)
            except:
                errors.append('financial year error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #DATE
            try:
                a = str(df['date of procurement'][i])[:8]
                d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                datetime1 = datetime0.date()
                datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #Total Plastic Quantity
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #GST
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #gst paid
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
            except:
                errors.append('gst paid error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #invoice number
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
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
                cl=WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                custom_wait_clickable_and_click(cl)
                time.sleep(0.5)
                add = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="simple-table-with-pagination"]/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(add)
                time.sleep(0.5)
                pop = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                pop.click()
                close = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)

            except:
                errors.append('Submit error')
                invoicee.append(str(df['invoice number'][i]))
                try:
                    pop = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                    pop.click()
                except:
                    pass
                close = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
                pass
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
            errors.append('add button error')
            invoicee.append(str(df['invoice number'][i]))
            i=i-1
            pass
            


        

def importer(c):
    global errors
    global invoicee
    action = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-importer-list/div[1]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr/td[8]/span/span/em')))
    custom_wait_clickable_and_click(action)
    time.sleep(1)
    close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
    custom_wait_clickable_and_click(close)
    time.sleep(1)
    nxt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
    custom_wait_clickable_and_click(nxt)
    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False)
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    count=0
    if(select.lower()=='b'):
        for i in range(len(df)):
            driver.implicitly_wait(15)
            #Add button
            try:
                time.sleep(1)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(add)
#                 time.sleep(1)
    #                 except:
    #                     errors.append('add button error')
    #                     break
            #registration type
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('registeration error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass



                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #address
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #state
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(2)
                except:
                    errors.append('state error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #mobile number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #financial year
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    time.sleep(0.5)
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #GST
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #bank account no
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(str(df['bank account no'][i]))
                except:
                    errors.append('bank account no error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #ifsc code
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                except:
                    errors.append('ifsc code error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #gst paid
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(str(df['gst paid'][i]))
                except:
                    errors.append('gst paid error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Quantity (Tons)
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('Total Quantity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass



                #invoice number
                #import random
                #a = (random.randint(0,9999))
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(df['invoice number'][i])
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
                    if(df['category of plastic'][i].lower()=='cat iv'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1)
                    else:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1)
                #% of recycled plastic packaging
                        try:
                            driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
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
                    pass


                #plastic material type
                try:
                    if(df['plastic material type'][i].lower()=='others'):
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        #other plastic material type
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
                    else:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal8c8d"]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                except:
                    errors.append('plastic material type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Submit
                try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                    custom_wait_clickable_and_click(cl)
    #                 except:
    #                     errors.append('Submit error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass
    #                 #Confirm
    #                 try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    add = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div/div[4]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                    custom_wait_clickable_and_click(add)
                    time.sleep(0.5)
                    pop = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                    pop.click()
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)

                except:
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    try:
                        pop = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                        pop.click()
                    except:
                        pass
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[6]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    pass
            except:
                driver.refresh()
                driver.refresh()
                driver.implicitly_wait(10)
                time.sleep(1)
                close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[3]/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
                time.sleep(0.5)
                nxt = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[3]/div/div/div[2]/div[4]/form/div[4]/button[2]')))
                custom_wait_clickable_and_click(nxt)
                errors.append('add button error')
                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass


    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select=='a'):
        df['date of procurement']=df['date of procurement'].astype(str)
    #             df['date of procurement'] = df['date of procurement'].apply(lambda x: x.replace("-", "/"))
        #plastic raw material/packaging procured
        for i in range(len(df)):
            driver.implicitly_wait(15)
            #Add button
            try:
                time.sleep(1)
                driver.implicitly_wait(15)
                r_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                custom_wait_clickable_and_click(r_type)
#                 time.sleep(0.5)
                r_click = driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
#                 time.sleep(0.5)
                r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(r_select)

    #                 except:
    #                     errors.append('add button error')
    #                     break

                #entity type
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #country
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/div/div/div[2]/input').send_keys(df['country'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(1)
                except:
                    errors.append('country error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #address
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #mobile number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #category of plastic
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #financial year
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[3]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #DATE
                try:
                    a = str(df['date of procurement'][i])[:8]
                    d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                    datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                    datetime1 = datetime0.date()
                    datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Plastic Quantity
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #invoice number
                try:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal8a8b"]/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(df['invoice number'][i])
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

                #plastic material type
                try:
                    time.sleep(1)
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
                    pass

                #Submit
                try:
                    cl=WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    add = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[1]/div/div[2]/div[1]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/thead[1]/tr/th/div/div[2]/a[1]')))
                    custom_wait_clickable_and_click(add)
                    time.sleep(0.5)
                    pop = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                    pop.click()
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                except:
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    try:
                        pop = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/button')))
                        pop.click()
                    except:
                        pass
                    close = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-brand-owner-application/div[5]/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    pass
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
                errors.append('add button error')
                invoicee.append(str(df['invoice number'][i]))
                i=i-1
                pass

     


button1 = tk.Button(text='open browser', command=hello, bg='brown',fg='white')
canvas1.create_window(75, 75, window=button1)
button4 = tk.Button(text='Continue', command=ahead3, bg='brown',fg='white')
canvas4.create_window(75, 75, window=button4)
button2 = tk.Button(text='show errors', command=error, bg='brown',fg='white')
canvas2.create_window(75, 75, window=button2)

root.mainloop()


