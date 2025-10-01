from datetime import datetime, timedelta, date
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
from selenium.common.exceptions import WebDriverException
import tkinter as tk
import tkinter.filedialog as fd
import time
import pandas as pd
import tkinter as tk
import easygui
import requests
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from selenium.webdriver.common.action_chains import ActionChains

def Home():
    global errors
    global invoicee
    global roww
    global driver
    global email_id
    global entity_name
    global entity_type
    global portal
    global comman
    today = date.today()
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
    WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.XPATH, '//span[@class="account-name"]'))
)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//img[@class="ilens-home-img cursor-pointer"]/parent::a'))).click()
        email_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//tbody[@id="ScrollableSimpleTableBody"]//span[contains(text(),"@")]'))).text
        portal = "PW"
        comman = f"{email_id}_PW"
        time.sleep(3)
        driver.get("https://eprplastic.cpcb.gov.in/#/epr/pibo-dashboard-view")

        entity_type = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//p[text()="User Type"]/following::span[1]'))).text
        entity_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//p[text()="Company Name"]/following::span[1]'))).text
    except Exception as e:
        print("❌ Error ", e)
        pass

    errors = []
    invoicee = []
    roww=[]
    c=-1

    print(driver.get_cookies())



def error():
    global df
    now = datetime.now()
    df.to_excel('errors_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')


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
    
           
def state():
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()
    df = pd.read_excel(file, keep_default_na=False, converters={'Year': str})

    cols_to_convert = [
        'Pre Cat I', 'Pre Cat II', 'Pre Cat III', 'Pre Cat IV',
        'PreRecy Cat I', 'PreRecy Cat II', 'PreRecy Cat III', 'PreRecy Cat IV',
        'Post Cat I', 'Post Cat II', 'Post Cat III', 'Post Cat IV',
        'PostRecy Cat I', 'PostRecy Cat II', 'PostRecy Cat III', 'PostRecy Cat IV',
        'Expo Cat I', 'Expo Cat II', 'Expo Cat III', 'Expo Cat IV',
        'ExpoRecy Cat I', 'ExpoRecy Cat II', 'ExpoRecy Cat III', 'ExpoRecy Cat IV'
    ]

    # Convert each column to float64
    df[cols_to_convert] = df[cols_to_convert].astype('float64')


    driver.get('https://eprplastic.cpcb.gov.in/#/epr/filing/state-wise-plastic-waste')
    time.sleep(1)


    for i, row in df.iterrows():
        driver.refresh()
        # driver.get('https://eprplastic.cpcb.gov.in/#/epr/filing/state-wise-plastic-waste')
        time.sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@name="select_fin_year"]//input').send_keys(df['Year'][i])
        time.sleep(2)
        cl = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]'))).click()

        # pwp_button_locator = (By.XPATH, '//button[text()="Add Data "]').click()
        cl = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Add Data "]'))).click()
        # custom_wait_clickable_and_click(driver, pwp_button_locator)

        driver.find_element(by=By.XPATH, value='//*[@name="state_select"]//input').send_keys(df['State'][i])
        cl = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]'))).click()

        ## Cat I (Rigid)

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[1]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[1]/input').send_keys(df['Pre Cat I'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[2]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[2]/input').send_keys(df['PreRecy Cat I'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[3]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[3]/input').send_keys(df['Post Cat I'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[4]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[4]/input').send_keys(df['PostRecy Cat I'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[5]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[5]/input').send_keys(df['Expo Cat I'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[6]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Rigid Plastic (Cat-I)"]/following-sibling::td[6]/input').send_keys(df['ExpoRecy Cat I'][i])

            ## Cat II (Rigid)

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[1]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[1]/input').send_keys(df['Pre Cat II'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[2]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[2]/input').send_keys(df['PreRecy Cat II'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[3]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[3]/input').send_keys(df['Post Cat II'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[4]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[4]/input').send_keys(df['PostRecy Cat II'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[5]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[5]/input').send_keys(df['Expo Cat II'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[6]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Flexible Plastic (Cat-II)"]/following-sibling::td[6]/input').send_keys(df['ExpoRecy Cat II'][i])


            ## Cat III (Rigid)

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[1]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[1]/input').send_keys(df['Pre Cat III'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[2]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[2]/input').send_keys(df['PreRecy Cat III'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[3]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[3]/input').send_keys(df['Post Cat III'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[4]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[4]/input').send_keys(df['PostRecy Cat III'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[5]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[5]/input').send_keys(df['Expo Cat III'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[6]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="MLP (Cat-III)"]/following-sibling::td[6]/input').send_keys(df['ExpoRecy Cat III'][i])

            ## Cat IV (Rigid)

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[1]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[1]/input').send_keys(df['Pre Cat IV'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[2]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[2]/input').send_keys(df['PreRecy Cat IV'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[3]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[3]/input').send_keys(df['Post Cat IV'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[4]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[4]/input').send_keys(df['PostRecy Cat IV'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[5]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[5]/input').send_keys(df['Expo Cat IV'][i])

        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[6]/input').clear()
        driver.find_element(by=By.XPATH, value='//td[text()="Compostable Plastic (Cat-IV)"]/following-sibling::td[6]/input').send_keys(df['ExpoRecy Cat IV'][i])

        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"][text()="Submit"]'))).click()
        time.sleep(2)
        # break


def all_scrape():

    def convert_cat(text):
        roman = ['I', 'II', 'III', 'IV', 'V']
        text = re.sub(r'\b([1-5])\b', lambda m: roman[int(m.group(1))-1], text)
        text = text.replace('-', ' ').replace('CAT', 'Cat').replace('cat', 'Cat').strip()
        return text

    def scrape_data_target():
        try:
            print("📅 Fetching TARGET Data")

            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-dashboard-view')
            time.sleep(5)
            a2, b2, c2, d2, e2, h2, i2, j2, k2 = [], [], [], [], [], [], [], [], []
            x = 1

            while True:
                try:
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//span[@title="Clear all"]/following::span[1]'))).click()
                    section_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
                    if x > len(section_links):
                        break
                    financial_year = section_links[x-1].text.strip()
                    section_links[x-1].click()
                    time.sleep(2)

                    rows = driver.find_elements(By.XPATH, '//tbody[@id="ScrollableSimpleTableBody"]/tr')
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        a2.append(convert_cat(cells[0].text))
                        b2.append(cells[1].text)
                        c2.append(cells[2].text)
                        d2.append(cells[3].text)
                        e2.append(cells[4].text)
                        h2.append(financial_year)
                        i2.append(entity_type)
                        j2.append(entity_name)
                        k2.append(email_id)
                    x += 1

                except Exception as e:
                    print(f"❌ Failed Target Data:{e}")
                    return
                
            print("✅ Target Data fetched successfully")
            return pd.DataFrame({
                'Category': a2,
                'Min_Recycling_Target': b2,
                'Max_EOL_Target': c2,
                'Min_Of_Recycling_Material': d2,
                'Min_Reuse_Target': e2,
                'Financial_Year': h2,
                'Type_of_entity': i2,
                'entity_name': j2,
                'email_id': k2
            })
        
        except:
            return pd.DataFrame(columns=[
                'Category','Min_Recycling_Target','Max_EOL_Target','Min_Of_Recycling_Material',
                'Min_Reuse_Target','Financial_Year','Type_of_entity','entity_name','email_id'
            ])

    def scrape_data_annual_report():
        try:
            print("📅 Fetching ANNUAL Data")

            driver.get('https://eprplastic.cpcb.gov.in/#/epr/annual-report-filing')
            time.sleep(5)
            driver.refresh()
            time.sleep(2)
            driver.implicitly_wait(15)

            a3, b3, c3, d3, e3, f3, g3, h3, i3 = [], [], [], [], [], [], [], [], []
            rows = driver.find_elements(By.XPATH, '//div[contains(text(),"Annual Report (")]/following::div[1]//tbody[@id="ScrollableSimpleTableBody"]/tr[position()>0]')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                a3.append(cells[1].text)
                b3.append(cells[2].text)
                c3.append(cells[3].text)
                d3.append(cells[4].text)
                e3.append(cells[5].text)
                f3.append(cells[6].text)
                g3.append(entity_type)
                h3.append(entity_name)
                i3.append(email_id)
            annual_df = pd.DataFrame({
                'Category': a3,
                'Procurement_Tons': b3,
                'Sales_Tons': c3,
                'Export_Tons': d3,
                'Reuse_Tons': e3,
                'UREP_Tons': f3,
                'Type_of_entity': g3,
                'entity_name': h3,
                'email_id':i3
            })
            print("✅ ANNUAL Data fetched successfully")

        except Exception as e:
            print(f"❌ Failed ANNUAL Data")
            annual_df = pd.DataFrame(columns=[
                'Category','Procurement_Tons','Sales_Tons','Export_Tons','Reuse_Tons',
                'UREP_Tons','Type_of_entity','entity_name','email_id'
            ])
            pass

        try:
            print("📅 Fetching compliance Data")

            a4, a41, b4, c4, d4, e4, g4, h4, i4 = [], [], [], [], [], [], [], [], []
            try:
                rows = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH,'//div[contains(text(),"Fulfilment of EPR Targets")]/following::div[1]//table[@id="simple-table-with-pagination"]/tbody/tr[position()>0]')))
            except:
                rows = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH,'//div[contains(text(),"Fulfilment of EPR Targets")]/following::div[1]//tbody/tr[position()>0]')))

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                a4.append(convert_cat(cells[1].text.split("-")[0].strip()))
                a41.append(cells[1].text.split("-")[-1].strip())
                b4.append(cells[2].text)
                c4.append(cells[3].text)
                d4.append(cells[4].text)
                e4.append(cells[5].text)
                g4.append(entity_type)
                h4.append(entity_name)
                i4.append(email_id)

            compliance_df = pd.DataFrame({
                'Category': a4,
                'Rec_Eol': a41,
                'Target': b4,
                'Achieved': c4,
                'Available_Potential': d4,
                'Remarks': e4,
                'Type_of_entity': g4,
                'entity_name': h4,
                'email_id': i4
            })
            print("✅ compliance Data fetched successfully")

        except Exception as e:
            print(f"❌ Failed compliance Data")
            compliance_df = pd.DataFrame(columns=[
                'Category','Rec_Eol','Target','Achieved','Available_Potential',
                'Remarks','Type_of_entity','entity_name','email_id'
            ])
            pass

        try:
            print("📅 Fetching Next year Target Data")

            a5, b5, c5, g5, h5, i5 = [], [], [], [], [], []
            rows = driver.find_elements(By.XPATH, '//div[contains(text(),"Next year Targets (")]/following::div[1]//tbody[@id="ScrollableSimpleTableBody"]/tr[position()>0]')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                a5.append(convert_cat(cells[1].text.split("-")[0].strip()))
                b5.append(cells[1].text.split("-")[-1].replace("Plastic", "").strip())
                c5.append(cells[2].text)
                g5.append(entity_type)
                h5.append(entity_name)
                i5.append(email_id)
            next_target_df = pd.DataFrame({
                'Category': a5,
                'Rec_Eol': b5,
                'Target': c5,
                'Type_of_entity': g5,
                'entity_name': h5,
                'email_id': i5
            })
            print("✅ Next year Target Data fetched successfully")
            
        except Exception as e:
            print(f"❌ Failed Next year Target Data")
            next_target_df = pd.DataFrame(columns=[
                'Category','Rec_Eol','Target','Type_of_entity','entity_name','email_id'
            ])
            pass
        return annual_df, compliance_df, next_target_df

    def scrape():
        try:
            try:
                cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
                login_token = None
                for cookie in cookies_data["cookies"]:
                    if cookie["name"] == "login-token":
                        login_token = cookie["value"]
                        break
            except Exception as e:
                print("❌ Failed to retrieve cookies:", e)
                return
            
            date_list = []
            start_date = datetime(2020, 4, 1)
            end_date = datetime.today()
            while start_date < end_date:
                next_year = start_date.replace(year=start_date.year + 1) - timedelta(days=1)
                date_list.append({
                    "date_from": start_date.strftime('%Y-%m-%d'),
                    "date_to": next_year.strftime('%Y-%m-%d')
                })
                start_date = next_year + timedelta(days=1)

            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'login-token={login_token}',
                'Origin': 'https://eprplastic.cpcb.gov.in',
                'Permissions-Policy': 'self',
                'User-Agent': 'Mozilla/5.0'
            }

            # ============================
            # 📦 Fetch Sales Data
            # ============================

            sales_rows = []
            url_sales = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_materials_sold"

            for date_range in date_list:
                print(f"📅 Fetching SALES data from {date_range['date_from']} to {date_range['date_to']}")
                payload = json.dumps({
                    "page": 1,
                    "records": 100000,
                    "filters": {},
                    "page_count": 50,
                    "page_no": 1,
                    "no_of_records": 100000,
                    "search_text": "",
                    "from_date": date_range["date_from"],
                    "to_date": date_range["date_to"],
                    "sortData": ""
                })

                try:
                    response = requests.post(url_sales, headers=headers, data=payload, verify=False)
                except Exception as e:
                    print("❌ API request error, retrying after delay:", e)
                    time.sleep(20)
                    response = requests.post(url_sales, headers=headers, data=payload, verify=False)

                try:
                    rows = response.json().get("data", {}).get("tableData", {}).get("bodyContent", [])
                    if not rows:
                        print("⚠️ No data returned for this SALES range.")
                    sales_rows.extend(rows)
                except Exception as e:
                    print("❌ Error parsing SALES API response:", e)
                    continue
            
            if sales_rows:
                df_sales = pd.DataFrame([{
                    'Registration Type': row.get("registration_type", "N/A"),
                    'Entity Type': row.get("entity_type", "N/A"),
                    'Name of the Entity': row.get("entity_name", "N/A"),
                    'State': row.get("entity_state", "N/A"),
                    'Address': re.sub(r'[^\x20-\x7E]', ' ', row.get("entity_address", "N/A")).strip(),
                    'Mobile Number': row.get("entity_mobile", "N/A"),
                    'Plastic Material Type': row.get("plastic_type", "N/A"),
                    'Category of Plastic': row.get("plastic_category", "N/A"),
                    'Category': "Cat I" if "Containers" in row.get("plastic_category", "N/A") else row.get("plastic_category", "N/A"),
                    'Financial Year': row.get("year", "N/A"),
                    'Date': row.get("last_updated_at", "N/A"),
                    'Total Plastic Qty (Tons)': row.get("quantity", "N/A"),
                    'Recycled Plastic %': row.get("recycled", "N/A"),
                    'Recycle Consumption': (
                        float(row.get("quantity", 0)) * float(row.get("recycled", 0)) / 100
                        if row.get("quantity") not in [None, "N/A", ""] and row.get("recycled") not in [None, "N/A", ""] 
                        else 0
                    ),
                    'GST': row.get("gst", "N/A"),
                    'GST Paid': row.get("gst_paid", "N/A"),
                    'EPR invoice No': row.get("invoice_no", "N/A"),
                    'GST E-Invoice No': row.get("gst_e_invoice", "N/A"),
                    'Upload Status': row.get("status", "N/A"),
                    'Type_of_entity': entity_type,
                    'entity_name': entity_name,
                    'email_id': email_id
                } for row in sales_rows])
            else:
                df_sales = pd.DataFrame(columns=[
                    'Registration Type', 'Entity Type', 'Name of the Entity', 'State', 'Address',
                    'Mobile Number', 'Plastic Material Type', 'Category of Plastic', 'Category', 'Financial Year',
                    'Date', 'Total Plastic Qty (Tons)', 'Recycled Plastic %', 'Recycle Consumption', 'GST', 'GST Paid',
                    'EPR invoice No', 'GST E-Invoice No', 'Upload Status','Type_of_entity','entity_name','email_id'
                ])
                print("No sales data found.")
        except:
            print(f"❌ Failed Sales data")
            df_sales = pd.DataFrame(columns=[
                    'Registration Type', 'Entity Type', 'Name of the Entity', 'State', 'Address',
                    'Mobile Number', 'Plastic Material Type', 'Category of Plastic', 'Category', 'Financial Year',
                    'Date', 'Total Plastic Qty (Tons)', 'Recycled Plastic %', 'Recycle Consumption', 'GST', 'GST Paid',
                    'EPR invoice No', 'GST E-Invoice No', 'Upload Status','Type_of_entity','entity_name','email_id'
                ])
            pass

        # ============================
        # 📦 Fetch Procurement Data
        # ============================

        try:
            procurement_rows = []
            url_proc = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_material_procurement_details"

            for date_range in date_list:
                print(f"📅 Fetching PROCUREMENT data from {date_range['date_from']} to {date_range['date_to']}")
                payload = json.dumps({
                    "page": 1,
                    "records": 100000,
                    "filters": {},
                    "page_count": 50,
                    "page_no": 1,
                    "no_of_records": 100000,
                    "search_text": "",
                    "from_date": date_range["date_from"],
                    "to_date": date_range["date_to"],
                    "sortData": ""
                })

                try:
                    response = requests.post(url_proc, headers=headers, data=payload, verify=False)
                except Exception as e:
                    print("❌ API request error, retrying after delay:", e)
                    time.sleep(20)
                    response = requests.post(url_proc, headers=headers, data=payload, verify=False)

                try:
                    rows = response.json().get("data", {}).get("tableData", {}).get("bodyContent", [])
                    if not rows:
                        print("⚠️ No data returned for this PROCUREMENT range.")
                    procurement_rows.extend(rows)
                except Exception as e:
                    print("❌ Error parsing PROCUREMENT API response:", e)
                    continue

            if procurement_rows:
                df_procurement = pd.DataFrame([{
                    'Registration Type': row.get("registration_type", "N/A"),
                    'Entity Type': row.get("entity_type", "N/A"),
                    'Name of the Entity': row.get("entity_name", "N/A"),
                    'State': row.get("entity_state", "N/A"),
                    'Address': re.sub(r'[^\x20-\x7E]', ' ', row.get("entity_address", "N/A")).strip(),
                    'Mobile Number': row.get("entity_mobile", "N/A"),
                    'Plastic Material Type': row.get("plastic_type", "N/A"),
                    'Category of Plastic': row.get("plastic_category", "N/A"),
                    'Category': "Cat I" if "Containers" in row.get("plastic_category", "N/A") else row.get("plastic_category", "N/A"),
                    'Financial Year': row.get("year", "N/A"),
                    'Date': row.get("last_updated_at", "N/A"),
                    'Total Plastic Qty (Tons)': row.get("quantity", "N/A"),
                    'Recycled Plastic %': row.get("recycled", "N/A"),
                    'Recycle Consumption': (
                        float(row.get("quantity", 0)) * (float(row.get("recycled", 0)) / 100)
                        if row.get("quantity") not in [None, "N/A", ""] and row.get("recycled") not in [None, "N/A", ""] 
                        else 0
                    ),
                    'GST': row.get("gst", "N/A"),
                    'GST Paid': row.get("gst_paid", "N/A"),
                    'EPR invoice No': row.get("invoice_no", "N/A"),
                    'GST E-Invoice No': row.get("gst_e_invoice", "N/A"),
                    'Type_of_entity': entity_type,
                    'entity_name': entity_name,
                    'email_id': email_id
                } for row in procurement_rows])
            else:
                df_procurement = pd.DataFrame(columns=[
                    'Registration Type', 'Entity Type', 'Name of the Entity', 'State', 'Address',
                    'Mobile Number', 'Plastic Material Type', 'Category of Plastic', 'Category', 'Financial Year',
                    'Date', 'Total Plastic Qty (Tons)', 'Recycled Plastic %','Recycle Consumption', 'GST', 'GST Paid',
                    'EPR invoice No', 'GST E-Invoice No','Type_of_entity','entity_name','email_id'
                ])
                print("No procurement data found.")
        except:
            print(f"❌ Failed Procurement data")
            df_procurement = pd.DataFrame(columns=[
                    'Registration Type', 'Entity Type', 'Name of the Entity', 'State', 'Address',
                    'Mobile Number', 'Plastic Material Type', 'Category of Plastic', 'Category', 'Financial Year',
                    'Date', 'Total Plastic Qty (Tons)', 'Recycled Plastic %','Recycle Consumption', 'GST', 'GST Paid',
                    'EPR invoice No', 'GST E-Invoice No','Type_of_entity','entity_name','email_id'
                ])
            pass

        # ============================
        # 📦 wallet Data
        # ============================

        try:
            a2, b, c, d, e1, f, g, h, i2, j, k, l, m, n, o, p, q, r, s = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

            url = "https://eprplastic.cpcb.gov.in/epr/m3/api/v1.0/pwp/list_credit_transactions"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'login-token={login_token}',
                'User-Agent': 'Mozilla/5.0'
            }

            payload = json.dumps({})
            try:
                response = requests.post(url, headers=headers, data=payload, files=None, verify=False)
                if response.json().get("status") != "success":
                    time.sleep(20)
                    response = requests.post(url, headers=headers, data=payload, files=None, verify=False)
            except Exception as e:
                print("❌ API request error, retrying after delay:", e)
                time.sleep(20)
                response = requests.post(url, headers=headers, data=payload, files=None, verify=False)
            try:
                details = response.json()["data"]["tableData"]["bodyContent"]

                for index, d_data in enumerate(details):
                    index += 1
                    com_id = d_data["id"]
                    date = d_data.get("date", "")
                    credit = d_data.get("transferTo", "")
                    try:
                        url = "https://eprplastic.cpcb.gov.in/epr/m3/api/v1.0/pwp/list_transfered_certificates"
                        payload = json.dumps({"id": com_id})

                        retries = 0
                        max_retries = 5
                        delay = 20

                        while retries < max_retries:
                            try:
                                response = requests.post(url, headers=headers, data=payload, files=None, verify=False)
                                response_json = response.json()

                                if response_json.get("status") == "success":
                                    rows = response_json["data"]["tableData"]["bodyContent"]
                                    break
                                else:
                                    print(f"⚠️ Status not successful: {response_json.get('status')}, retrying after {delay} seconds...")
                            except Exception as e:
                                print("❌ API request error, retrying after delay:", e)

                            retries += 1
                            time.sleep(delay)
                        else:
                            print("❌ Maximum retries exceeded for the second request.")
                            continue

                        rows = response.json()["data"]["tableData"]["bodyContent"]

                        for row in rows:
                            a2.append(index)
                            b.append(date)
                            c.append(credit)
                            d.append(row.get("cert_id", "N/A"))
                            e1.append(row.get("value", "N/A"))
                            f.append(row.get("owner", "N/A"))
                            g.append(row.get("category", "N/A").replace("-", " "))
                            h.append(row.get("processing_type", "N/A"))
                            i2.append(row.get("transaction_id", "N/A"))
                            j.append(row.get("before_potential", "N/A"))
                            k.append(row.get("after_potential", "N/A"))
                            l.append(row.get("before_used_potential", "N/A"))
                            m.append(row.get("after_used_potential", "N/A"))
                            n.append(row.get("cumulative_potential", "N/A"))
                            o.append(row.get("generation_time", "N/A"))
                            p.append(row.get("validity", "N/A"))
                            q.append(entity_type)
                            r.append(entity_name)
                            s.append(email_id)
                    except:
                        pass

            except Exception as e:
                print("❌ Error parsing wallet API response:", e)
                    
            if a2:
                df_wallet_credit = pd.DataFrame({
                    'SL_No': a2,
                    'Date': b,
                    'Credited_From': c,
                    'Certificate_ID': d,
                    'Value': e1,
                    'Certificate_Owner': f,
                    'Category': g,
                    'Processing_Type': h,
                    'Transaction_ID': i2,
                    'Available_Potential_Prior_Generation': j,
                    'Available_Potential_After_Generation': k,
                    'Used_Potential_Prior_Generation': l,
                    'Used_Potential_After_Generation': m,
                    'Cumulative_Potential': n,
                    'Generated_At': o,
                    'Validity': p,
                    'Type_of_entity': q,
                    'entity_name': r,
                    'email_id': s
                })
                print("✅ Credit Wallet Data fetched successfully")

            else:
                df_wallet_credit = pd.DataFrame(columns=[
                    'SL.No', 'Date', 'Credited From', 'Certificate ID', 'Value',
                    'Certificate Owner', 'Category', 'Processing Type', 'Transaction ID',
                    'Available Potential Prior Generation', 'Available Potential After Generation',
                    'Used Potential Prior Generation', 'Used Potential After Generation',
                    'Cumulative Potential', 'Generated At', 'Validity','Type_of_entity','entity_name','email_id'
                ])
                print("No credit wallet data found.")
        except:
            print(f"❌ Failed Credit wallet data")
            df_wallet_credit = pd.DataFrame(columns=[
                        'SL_No','Date','Credited_From','Certificate_ID','Value',
                        'Certificate_Owner','Category','Processing_Type','Transaction_ID',
                        'Available_Potential_Prior_Generation','Available_Potential_After_Generation',
                        'Used_Potential_Prior_Generation','Used_Potential_After_Generation',
                        'Cumulative_Potential','Generated_At','Validity','Type_of_entity','entity_name','email_id'
            ])
            pass

        try:
            print("📅 Fetching Debit Wallet Data")
            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
            time.sleep(3)
            driver.refresh()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//a[text()="Debit Transactions"]'))).click()

            a2,b,c,c2,c3,d,e1,f,g,h,i2,j,k,l,m,n,o,p,q=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
            x=1
            while True:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='simple-table-with-pagination']/tbody/tr[1]/td[8]/span/span/em")))
                try:
                    xpath = f"//table[@id='simple-table-with-pagination']/tbody/tr[{x}]/td[8]/span/span/em"
                    target_element = driver.find_element(By.XPATH, xpath)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
                    sno=driver.find_element(by=By.XPATH, value='//table[@id="simple-table-with-pagination"]/tbody/tr['+str(x)+']/td[1]').text
                    date=driver.find_element(by=By.XPATH, value='//table[@id="simple-table-with-pagination"]/tbody/tr['+str(x)+']/td[2]/span').text
                    credit=driver.find_element(by=By.XPATH, value='//table[@id="simple-table-with-pagination"]/tbody/tr['+str(x)+']/td[5]/span').text
                    for _ in range(5):
                        try:
                            driver.find_element(By.XPATH, '//table[@id="simple-table-with-pagination"]/tbody/tr['+str(x)+']/td[8]/span/span/em').click()
                            break
                        except WebDriverException:
                            time.sleep(1)
                    time.sleep(3)
                    tree = html.fromstring(driver.page_source)
                    job = tree.xpath('//h5[text()="Transfered Certificates"]/parent::div/parent::div//table[@id="simple-table-with-pagination"]/tbody/tr//td/span[@title]')
                    z=[]
                    for ii in job:
                        details = ii.xpath('./@title')[0].strip()
                        if details:
                            z.append(details)
                    i=0
                    while i < len(z):
                        a2.append(sno)
                        b.append(date)
                        c.append(credit)
                        c2.append(entity_type)
                        c3.append(entity_name)
                        d.append(z[i])
                        e1.append(z[i+1])
                        f.append(z[i+2])
                        g.append(z[i+3].replace("-", " "))
                        h.append(z[i+4])
                        i2.append(z[i+5])
                        j.append(z[i+6])
                        k.append(z[i+7])
                        l.append(z[i+8])
                        m.append(z[i+9])
                        n.append(z[i+10])
                        o.append(z[i+11])
                        p.append(z[i+12])
                        q.append(email_id)
                        i += 13
                    
                    df_wallet_debit = pd.DataFrame({
                        'SL_No': a2,
                        'Date': b,
                        'Transfer To (PIBO)': c,
                        'Certificate_ID': d,
                        'Value': e1,
                        'Certificate_Owner': f,
                        'Category': g,
                        'Processing_Type': h,
                        'Transaction_ID': i2,
                        'Available_Potential_Prior_Generation': j,
                        'Available_Potential_After_Generation': k,
                        'Used_Potential_Prior_Generation': l,
                        'Used_Potential_After_Generation': m,
                        'Cumulative_Potential': n,
                        'Generated_At': o,
                        'Validity': p,
                        'Type_of_entity':c2,
                        'entity_name':c3,
                        'email_id': q
                    })
                    
                    time.sleep(1)
                    for _ in range(5):
                        try:
                            driver.find_element(By.XPATH, '//button[@id="closeSubmitModal"]/span').click()
                            break
                        except WebDriverException:
                            time.sleep(1)
                    time.sleep(1)
                    x += 1
                except:
                    break
            print("✅ Debit Wallet Data fetched successfully")

        except Exception as e:
            print(f"❌ Failed Debit wallet data")
            df_wallet_debit = pd.DataFrame(columns=[
                        'SL_No','Date','Transfer To (PIBO)','Certificate_ID','Value',
                        'Certificate_Owner','Category','Processing_Type','Transaction_ID',
                        'Available_Potential_Prior_Generation','Available_Potential_After_Generation',
                        'Used_Potential_Prior_Generation','Used_Potential_After_Generation',
                        'Cumulative_Potential','Generated_At','Validity','Type_of_entity','entity_name','email_id'
            ])

        try:
            print("📅 Fetching 2 Credit Transactions Data")
            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
            time.sleep(3)
            driver.refresh()
            driver.implicitly_wait(15)

            a2, a3, b3, c3, c2, d3, e3, f3, g3, h3, i3 = [], [], [], [], [], [], [], [], [], [], []
            rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody[@id="ScrollableSimpleTableBody"]/tr')))
            time.sleep(3)
            tree = html.fromstring(driver.page_source)
            rows = tree.xpath('//tbody[@id="ScrollableSimpleTableBody"]/tr')
            for row in rows:
                cells = row.xpath('./td')
                a2.append(cells[0].text_content())
                a3.append(cells[1].text_content())
                b3.append(cells[2].text_content())
                c3.append(convert_cat(cells[3].text_content().strip().split()[0].strip()))
                c2.append(' '.join(cells[3].text_content().strip().split()[1:]))
                d3.append(cells[4].text_content())
                e3.append(cells[5].text_content())
                f3.append(cells[6].text_content())
                g3.append(entity_type)
                h3.append(entity_name)
                i3.append(email_id)

            credit_2_df = pd.DataFrame({
                'Sr.No': a2,
                'Date': a3,
                'Transaction ID': b3,
                'Category': c3,
                'Processing Type': c2,
                'Credited From': d3,
                'Status': e3,
                'Amount': f3,
                'Type_of_entity': g3,
                'entity_name': h3,
                'email_id':i3
            })
            print("✅ 2 Credit Transactions Data fetched successfully")

        except:
            print(f"❌ Faild 2 Credit Transactions Target Data")
            credit_2_df = pd.DataFrame(columns=[
                'Sr.No','Date','Transaction ID','Category','Processing Type','Credited From',
                'Status','Amount','Type_of_entity','entity_name','email_id'
            ])
            pass

        try:
            print("📅 Fetching 2 Debit Transactions Data")
            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
            time.sleep(3)
            driver.refresh()
            driver.implicitly_wait(15)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//a[text()="Debit Transactions"]'))).click()

            a2, a3, b3, c3, c2, d3, e3, f3, g3, h3, i3 = [], [], [], [], [], [], [], [], [], [], []
            rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody[@id="ScrollableSimpleTableBody"]/tr')))
            time.sleep(3)
            tree = html.fromstring(driver.page_source)
            rows = tree.xpath('//tbody[@id="ScrollableSimpleTableBody"]/tr')
            for row in rows:
                cells = row.xpath('./td')
                a2.append(cells[0].text_content())
                a3.append(cells[1].text_content())
                b3.append(cells[2].text_content())
                c3.append(convert_cat(cells[3].text_content().strip().split()[0].strip()))
                c2.append(' '.join(cells[3].text_content().strip().split()[1:]))
                d3.append(cells[4].text_content())
                e3.append(cells[5].text_content())
                f3.append(cells[6].text_content())
                g3.append(entity_type)
                h3.append(entity_name)
                i3.append(email_id)

            debit_2_df = pd.DataFrame({
                'Sr.No': a2,
                'Date': a3,
                'Transaction ID': b3,
                'Category': c3,
                'Processing Type': c2,
                'Transfer To (PIBO)': d3,
                'Status': e3,
                'Amount': f3,
                'Type_of_entity': g3,
                'entity_name': h3,
                'email_id':i3
            })
            print("✅ 2 Debit Transactions Data fetched successfully")

        except:
            print(f"❌ Faild 2 Debit Transactions Target Data")
            debit_2_df = pd.DataFrame(columns=[
                'Sr.No','Date','Transaction ID','Category','Processing Type','Transfer To (PIBO)',
                'Status','Amount','Type_of_entity','entity_name','email_id'
            ])
            pass
        # ============================
        # 📦 Filing Transactions Data
        # ============================
        try:
            print("📅 Fetching Filing Transactions Data")
            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
            time.sleep(3)
            driver.refresh()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//a[text()="Filing Transactions"]'))).click()

            driver.implicitly_wait(15)

            a2, a3, b3, c3, c2, d3, e3, f3, g3, h3, i3 = [], [], [], [], [], [], [], [], [], [], []
            rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody[@id="ScrollableSimpleTableBody"]/tr')))
            time.sleep(3)
            tree = html.fromstring(driver.page_source)
            rows = tree.xpath('//tbody[@id="ScrollableSimpleTableBody"]/tr')
            for row in rows:
                cells = row.xpath('./td')
                a2.append(cells[0].text_content())
                a3.append(cells[1].text_content())
                b3.append(cells[2].text_content())
                c3.append(convert_cat(cells[3].text_content().strip().split()[0].strip()))
                c2.append(' '.join(cells[3].text_content().strip().split()[1:]))
                d3.append(cells[4].text_content())
                e3.append(cells[5].text_content())
                f3.append(cells[6].text_content())
                g3.append(entity_type)
                h3.append(entity_name)
                i3.append(email_id)

            filing_df = pd.DataFrame({
                'Sr.No': a2,
                'Date': a3,
                'Transaction ID': b3,
                'Category': c3,
                'Processing Type': c2,
                'Operation Type': d3,
                'Amount': e3,
                'Number of Certificates': f3,
                'Type_of_entity': g3,
                'entity_name': h3,
                'email_id':i3
            })
            print("✅ Filing Transactions Data fetched successfully")

        except:
            print(f"❌ Filing Transactions Target Data")
            filing_df = pd.DataFrame(columns=[
                'Sr.No','Date','Transaction ID','Category','Processing Type','Operation Type','Amount',
                'Number of Certificates','Type_of_entity','entity_name','email_id'
            ])
            pass

        # ============================
        # 📦 Consumption Regn Data
        # ============================

        try:
            print("📅 Fetching Consumption Regn Data")

            driver.get('https://eprplastic.cpcb.gov.in/#/epr/producer-list')
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//em[@class="fa fa-eye"]'))).click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@id="product-comments-tab"]'))).click()

            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(text(),"Pertaining to Waste")]/following::div[1]//tbody/tr[position()>2]')))
            time.sleep(3)
            tree = html.fromstring(driver.page_source)
            rows = tree.xpath('//div[contains(text(),"Pertaining to Waste")]/following::div[1]//tbody/tr[position()>0]')
            data = []

            sl_no = ""
            state = ""
            year = ""

            for row in rows:
                cells = row.xpath('./td')
                texts = [cell.text for cell in cells]

                if len(texts) == 2:
                    sl_no = texts[0].strip() or sl_no
                    state = texts[1].strip() or sl_no
                elif len(texts) == 1:
                    year = texts[0].strip() or year
                elif len(texts) == 5:
                    category = convert_cat(texts[0].split("(")[1].replace(")",""))
                    material = texts[0].split("(")[0].strip()
                    pre_qty = texts[1].strip()
                    pre_recycled = texts[2].strip()
                    try:
                        pre_recycle_consumption = float(texts[1]) * (float(texts[2]) / 100)
                    except (ValueError, TypeError):
                        pre_recycle_consumption = 0
                    post_qty = texts[3].strip()
                    post_recycled = texts[4].strip()
                    try:
                        post_recycle_consumption = float(texts[3]) * (float(texts[4]) / 100)
                    except (ValueError, TypeError):
                        post_recycle_consumption = 0
                    try:
                        total_consumption = float(pre_qty) + float(post_qty)
                    except:
                        total_consumption = 0
                    data.append([
                        sl_no,
                        state,
                        year,
                        category,
                        material,
                        pre_qty,
                        pre_recycled,
                        pre_recycle_consumption,
                        post_qty,
                        post_recycled,
                        post_recycle_consumption,
                        total_consumption,
                        entity_type,
                        entity_name,
                        email_id
                    ])

                elif "Total" in texts[0]:
                    category = texts[0].strip()
                    pre_qty = texts[1]
                    pre_recycled = texts[2]
                    try:
                        pre_recycle_consumption = float(texts[1]) * (float(texts[2]) / 100)
                    except (ValueError, TypeError):
                        pre_recycle_consumption = 0
                    try:
                        post_qty = texts[3].strip()
                    except:
                        post_qty = None
                    try:
                        post_recycled = texts[4]
                    except:
                        post_recycled = None
                    if post_qty and post_recycled:
                        try:
                            post_recycle_consumption = float(texts[3]) * (float(texts[4]) / 100)
                        except (ValueError, TypeError):
                            post_recycle_consumption = 0
                    else:
                        post_recycle_consumption = 0
                    try:
                        total_consumption = float(pre_qty) + float(post_qty)
                    except:
                        total_consumption = 0
                    data.append([
                        category,
                        "",
                        "",
                        "",
                        "",
                        pre_qty,
                        pre_recycled,
                        pre_recycle_consumption,
                        post_qty,
                        post_recycled,
                        post_recycle_consumption,
                        total_consumption,
                        entity_type,
                        entity_name,
                        email_id
                    ])
                else:
                    continue

            headers = [
                "Sl. No.","State Name","Year","Category of Plastic","Material type","Pre Consumer Waste Plastic Quantity (TPA)",
                "Pre Consumer Waste Recycled Plastic %","Pre Consumer Waste Recycle Consumption","Post Consumer Waste Plastic Quantity (TPA)",
                "Post Consumer Waste Recycled Plastic %","Post Consumer Waste Recycle Consumption",'Total Consumption','Type_of_entity','entity_name','email_id'
            ]

            pertaining_df = pd.DataFrame(data, columns=headers)
            print("✅ Consumption Regn Data fetched successfully")

        except:
            print(f"❌ Failed Consumption Regn Data")
            pertaining_df = pd.DataFrame(columns=[
                "Sl. No.","State Name","Year","Category of Plastic","Material type","Pre Consumer Waste Plastic Quantity (TPA)",
                "Pre Consumer Waste Recycled Plastic %","Pre Consumer Waste Recycle Consumption","Post Consumer Waste Plastic Quantity (TPA)",
                "Post Consumer Waste Recycled Plastic %","Post Consumer Waste Recycle Consumption",'Total Consumption','Type_of_entity','entity_name','email_id'
            ])
            pass

        # ============================
        # 📦 Consumption Ar Data
        # ============================

        try:
            print("📅 Fetching Consumption AR Data")

            driver.get('https://eprplastic.cpcb.gov.in/#/epr/filing/state-wise-plastic-waste')
            time.sleep(5)
            x = 1
            while True:
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@name="select_fin_year"]/div/span'))).click()
                    section_links = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
                    if x > len(section_links):
                        break
                    financial_year = section_links[x-1].text.strip()
                    section_links[x-1].click()
                    time.sleep(2)
                    rows = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="table table-bordered scrollable-table pw-generated"]/tbody/tr[position()>2]')))
                    time.sleep(3)
                    tree = html.fromstring(driver.page_source)
                    rows = tree.xpath('//table[@class="table table-bordered scrollable-table pw-generated"]/tbody/tr[position()>0]')
                    data = []
                
                    sl_no = ""
                    state = ""
                    year = ""
                
                    for row in rows:
                        cells = row.xpath('./td')
                        texts = [cell.text for cell in cells]
                
                        if len(texts) == 2:
                            sl_no = texts[0].strip() or sl_no
                            state = texts[1].strip() or sl_no
                        elif len(texts) == 1:
                            year = texts[0].strip() or year
                        elif len(texts) == 7:
                            category = convert_cat(texts[0].split("(")[1].replace(")",""))
                            material = texts[0].split("(")[0].strip()
                            pre_qty = texts[1].strip()
                            pre_recycled = texts[2].strip()
                            try:
                                pre_recycle_consumption = float(texts[1]) * (float(texts[2]) / 100)
                            except (ValueError, TypeError):
                                pre_recycle_consumption = 0
                            post_qty = texts[3].strip()
                            post_recycled = texts[4].strip()
                            try:
                                post_recycle_consumption = float(texts[3]) * (float(texts[4]) / 100)
                            except (ValueError, TypeError):
                                post_recycle_consumption = 0
                            export_qty = texts[5].strip()
                            export_recycled = texts[6].strip()
                            try:
                                export_recycle_consumption = float(texts[5]) * (float(texts[6]) / 100)
                            except (ValueError, TypeError):
                                export_recycle_consumption = 0
                            try:
                                total_consumption = float(pre_qty) + float(post_qty) + float(export_qty)
                            except:
                                total_consumption = 0
                            data.append([
                                sl_no,
                                state,
                                year,
                                category,
                                material,
                                pre_qty,
                                pre_recycled,
                                pre_recycle_consumption,
                                post_qty,
                                post_recycled,
                                post_recycle_consumption,
                                export_qty,
                                export_recycled,
                                export_recycle_consumption,
                                total_consumption,
                                entity_type,
                                entity_name,
                                email_id
                            ])
                        
                        elif len(texts) == 5:
                            category = convert_cat(texts[0].split("(")[1].replace(")",""))
                            material = texts[0].split("(")[0].strip()
                            pre_qty = texts[1].strip()
                            pre_recycled = None
                            pre_recycle_consumption = None

                            post_qty = texts[2].strip()
                            post_recycled = None
                            post_recycle_consumption = None
                            export_qty = texts[3].strip()
                            export_recycled = texts[4].strip()
                            try:
                                export_recycle_consumption = float(texts[3]) * (float(texts[4]) / 100)
                            except (ValueError, TypeError):
                                export_recycle_consumption = 0
                            total_consumption = float(pre_qty) + float(post_qty) + float(export_qty)
                            data.append([
                                sl_no,
                                state,
                                year,
                                category,
                                material,
                                pre_qty,
                                pre_recycled,
                                pre_recycle_consumption,
                                post_qty,
                                post_recycled,
                                post_recycle_consumption,
                                export_qty,
                                export_recycled,
                                export_recycle_consumption,
                                total_consumption,
                                entity_type,
                                entity_name,
                                email_id
                            ])
                        else:
                            continue
                    x+=1
                except Exception as e:
                    x += 1

            headers = [
                "Sl. No.","State Name","Year","Category of Plastic","Material type","Pre Consumer Waste Plastic Quantity (TPA)",
                "Pre Consumer Waste Recycled Plastic %","Pre Consumer Waste Recycle Consumption","Post Consumer Waste Plastic Quantity (TPA)",
                "Post Consumer Waste Recycled Plastic %","Post Consumer Waste Recycle Consumption","Export Quantity Plastic Quantity (TPA)",
                "Export Quantity Recycled Plastic %","Export Quantity Recycle Consumption",'Total Consumption','Type_of_entity','entity_name','email_id'
            ]
                    
            cat_df = pd.DataFrame(data, columns=headers)
            print("✅ Consumption AR fetched successfully")
        except:
            print(f"❌ Failed Consumption AR Data")
            cat_df = pd.DataFrame(columns=[
                "Sl. No.","State Name","Year","Category of Plastic","Material type","Pre Consumer Waste Plastic Quantity (TPA)",
                "Pre Consumer Waste Recycled Plastic %","Pre Consumer Waste Recycle Consumption","Post Consumer Waste Plastic Quantity (TPA)",
                "Post Consumer Waste Recycled Plastic %","Post Consumer Waste Recycle Consumption","Export Quantity Plastic Quantity (TPA)",
                "Export Quantity Recycled Plastic %","Export Quantity Recycle Consumption",'Total Consumption','Type_of_entity','entity_name','email_id'
            ])
            pass

        # ============================
        # 📦 Certificates Generations Data
        # ============================ 

        cer_gen_df = pd.DataFrame(columns=[
                "Sr.No","Generation ID","Category","Processing Type","Amount","Status","Created At",'Type_of_entity','entity_name','email_id'
            ])  
        
        target_df = scrape_data_target()
        annual_df, compliance_df, next_target_df = scrape_data_annual_report()

        try:
            now = datetime.now()
            # filename = os.path.join('ALL_EPR_DASHBOARD' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')
            filename = os.path.join('.', 'ALL_EPR_DASHBOARD_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')

            def add_columns_to_dataframe(df):
                if df is None:
                    return None
                if df.empty:
                    for col in ['portal', 'comman']:
                        if col not in df.columns:
                            df[col] = []
                else:
                    df['portal'] = portal
                    df['comman'] = comman
                return df

            # Process all DataFrames
            dfs = {
                "Sales Data": df_sales,
                "Procurement Data": df_procurement,
                "1 Credit Wallet Data": df_wallet_credit,
                "2 Credit Wallet Data": credit_2_df,
                "1 Debit Wallet Data": df_wallet_debit,
                "2 Debit Wallet Data": debit_2_df,
                "Certificates Generations Data": cer_gen_df,
                "Filing Transactions Data": filing_df,
                "Target_Data": target_df,
                "Annual_report_Data": annual_df,
                "Compliance_status_Data": compliance_df,
                "Next_year_target_Data": next_target_df,
                "Consumption Regn Data": pertaining_df,
                "Consumption AR Data": cat_df
            }

            # Add columns to all DataFrames
            for sheet_name, df in dfs.items():
                if df is not None:
                    dfs[sheet_name] = add_columns_to_dataframe(df)

            # Save to Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in dfs.items():
                    if df is not None:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"✅ Excel file saved with separate sheets: {filename}")

        except Exception as e:
            print("❌ Error creating excel", e)


    try:
        scrape()
    except Exception as e:
        print("❌ Error ", e)
        pass
        time.sleep(10)

def Format4():
    # Define the column names exactly as given
    columns = [
        "Year", "State",
        "Pre Cat I", "Pre Cat II", "Pre Cat III", "Pre Cat IV",
        "PreRecy Cat I", "PreRecy Cat II", "PreRecy Cat III", "PreRecy Cat IV",
        "Post Cat I", "Post Cat II", "Post Cat III", "Post Cat IV",
        "PostRecy Cat I", "PostRecy Cat II", "PostRecy Cat III", "PostRecy Cat IV",
        "Expo Cat I", "Expo Cat II", "Expo Cat III", "Expo Cat IV",
        "ExpoRecy Cat I", "ExpoRecy Cat II", "ExpoRecy Cat III", "ExpoRecy Cat IV"
    ]
 
    # Create an empty DataFrame with those columns
    df = pd.DataFrame(columns=columns)
 
    # Save to Excel
    excel_filename = 'State_Wise_Upload_Format.xlsx'
    df.to_excel(excel_filename, index=False)
 
    # Show success message
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")
 
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
 
root = Tk()
root.title("State Wise Upload")
root.geometry("600x200")
root.configure(bg="#FFFFFF")
root.resizable(width=False, height=False)
 
menubar = Menu(root)
root.config(menu=menubar)
 
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=file_menu)
Excel_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Excel Format", menu=Excel_menu)
 
Excel_menu.add_command(label="Base Data_Format", command=Format4)


btn_frame = Frame(root, bg="#FFFFFF")
btn_frame.pack(pady=60)

btn_width = 15
btn_height = 2

# Button 1: Login
btn1 = Button(btn_frame, text='Login', command=Home, bg='#006400', fg='#FFFFFF',
              font=('Verdana', 12), width=btn_width, height=btn_height)
btn1.grid(row=0, column=0, padx=10)

# Button 2: Upload
btn2 = Button(btn_frame, text='Upload State Wise Data', command=state, bg='#006400', fg='#FFFFFF',
              font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=120)
btn2.grid(row=0, column=1, padx=10)

# Button 3: scrape
btn2 = Button(btn_frame, text='Scrape Data', command=all_scrape, bg='#006400', fg='#FFFFFF',
              font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=120)
btn2.grid(row=0, column=2, padx=10)

root.mainloop()


