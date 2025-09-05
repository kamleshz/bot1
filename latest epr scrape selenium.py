
from datetime import datetime, date
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import easygui
import os
from selenium.webdriver.common.action_chains import ActionChains
from lxml import html
from selenium.common.exceptions import WebDriverException


global driver
global email_id
global entity_name
global entity_type
global portal
global comman

def convert_cat(text):
    roman = ['I', 'II', 'III', 'IV', 'V']
    text = re.sub(r'\b([1-5])\b', lambda m: roman[int(m.group(1))-1], text)
    text = text.replace('-', ' ').replace('CAT', 'Cat').replace('cat', 'Cat').strip()
    return text

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

                rows = driver.find_elements(By.XPATH, '//tbody[@id="ScrollableSimpleTableBody"]/tr[position()>1]')
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

    # ============================
    # 📦 Fetch Sales Data
    # ============================
    try:
        print("📅 Fetching SALES Data")
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
        time.sleep(5)
        start_year = 2020
        current_year = datetime.now().year
        current_month = datetime.now().month

        end_year = current_year if current_month >= 4 else current_year - 1

        df_sales = pd.DataFrame()

        for year in range(start_year, end_year + 1):
            driver.refresh()
            time.sleep(2)
            from_date = f"01/04/{year}"
            to_date = f"31/03/{year+1}"

            try:
                time.sleep(3)
                date_input = driver.find_element(By.XPATH, "//input[@id='date_from']")
                date_input.clear()
                date_input.send_keys(from_date)

                date_end_input = driver.find_element(By.XPATH, "//input[@id='date_to']")
                date_end_input.clear()
                date_end_input.send_keys(to_date)

                click = driver.find_element(By.XPATH, '//button[contains(text(),"Fetch")]')
                custom_wait_clickable_and_click(click)

                df = pd.DataFrame()
                count = 0
                stop = driver.find_element(By.XPATH, '//table/tbody/tr/td/div[1]/div/span').text
                stop = [int(i) for i in stop.split() if i.isdigit()][-1]
                stop = math.ceil(stop / 50)

                while count < stop:
                    time.sleep(1)
                    count += 1
                    job = driver.find_element(By.ID, 'ScrollableSimpleTableBody')
                    soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
                    data = soup.find_all("span", class_="ng-star-inserted") or soup.find_all("td", class_="row-item")
                    z = [i.text.replace("\n", "").strip() for i in data]

                    a2, b, c, d, e1, f, g, h, h1, i2, j, k, l,l1, m, n, o, p, q, r, s = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                    i = 0
                    while i < len(z):
                        a2.append(z[i])
                        b.append(z[i+1])
                        c.append(z[i+2])
                        d.append(z[i+3])
                        e1.append(z[i+4])
                        f.append(z[i+5])
                        g.append(z[i+6])
                        h.append(z[i+7])
                        h1.append("Cat I" if "Containers" in z[i+7] else z[i+7])
                        i2.append(z[i+8])
                        j.append(z[i+9])
                        k.append(z[i+10])
                        l.append(z[i+11])
                        try:
                            recycle_consumption = float(z[i+10]) * (float(z[i+11]) / 100)
                        except (ValueError, TypeError):
                            recycle_consumption = "N/A"
                        l1.append(recycle_consumption)
                        m.append(z[i+12])
                        n.append(z[i+13])
                        o.append(z[i+14])
                        p.append(z[i+15])
                        q.append(entity_type)
                        r.append(entity_name)
                        s.append(email_id)

                        if len(z) > i+18 and z[i+16] == "" and z[i+17] == "" and z[i+18] == "":
                            i += 19
                        elif len(z) > i+17 and z[i+16] == "" and z[i+17] == "":
                            i += 18
                        else:
                            i += 16

                    df1 = pd.DataFrame({
                        'Registration Type': a2,
                        'Entity Type': b,
                        'Name of the Entity': c,
                        'State': d,
                        'Address': e1,
                        'Mobile Number': f,
                        'Plastic Material Type': g,
                        'Category of Plastic': h,
                        'Category': h1,
                        'Financial Year': i2,
                        'Date': j,
                        'Total Plastic Qty (Tons)': k,
                        'Recycled Plastic %': l,
                        'Recycle Consumption': l1,
                        'GST': m,
                        'GST Paid': n,
                        'EPR invoice No': o,
                        'GST E-Invoice No': p,
                        'Type_of_entity': q,
                        'entity_name': r,
                        'email_id': s
                    })

                    if df1.empty:
                        continue
                    if count == 1:
                        df = df1
                    else:
                        new = df.tail(50).reset_index(drop=True)
                        df1 = df1.reset_index(drop=True)

                        if list(new.columns) == list(df1.columns):
                            try:
                                comp = new.compare(df1)
                                if not comp.empty:
                                    df = pd.concat([df, df1], ignore_index=True)
                            except Exception as e:
                                df = pd.concat([df, df1], ignore_index=True)
                        else:
                            df = pd.concat([df, df1], ignore_index=True)

                    next_button = driver.find_elements(By.CLASS_NAME, 'action-button')[1]
                    custom_wait_clickable_and_click(next_button)
                    click = driver.find_element(By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                    custom_wait_clickable_and_click(click)

                df_sales = pd.concat([df_sales, df], ignore_index=True)
        
            except Exception as e:
                continue
        print("✅ SALES Data fetched successfully")

    except Exception as e:
        print(f"❌ Failed Sales Data")
        df_sales = pd.DataFrame(columns=[
        'Registration Type', 'Entity Type', 'Name of the Entity', 'State', 'Address',
        'Mobile Number', 'Plastic Material Type', 'Category of Plastic', 'Category', 'Financial Year',
        'Date', 'Total Plastic Qty (Tons)', 'Recycled Plastic %', 'Recycle Consumption', 'GST', 'GST Paid',
        'EPR invoice No', 'GST E-Invoice No','Type_of_entity','entity_name','email_id'
    ])
        pass

    # ============================
    # 📦 Fetch Procurement Data
    # ============================

    try:
        print("📅 Fetching PROCUREMENT Data")
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
        time.sleep(5)
        date_input = driver.find_element(By.XPATH, "//input[@id='date_from']")
        date_input.clear()
        date_input.send_keys("01/04/2020")
        today_date = datetime.now().strftime("%d/%m/%Y")
        date_end_input = driver.find_element(By.XPATH, "//input[@id='date_to']")
        date_end_input.send_keys(today_date)
        click = driver.find_element(by=By.XPATH, value='//button[contains(text(),"Fetch")]').click()
        custom_wait_clickable_and_click(click)

        df = pd.DataFrame()
        count = 0
        stop = driver.find_element(by=By.XPATH, value='//table/tbody/tr/td/div[1]/div/span').text
        stop = [int(i) for i in stop.split() if i.isdigit()][-1]
        stop = math.ceil(stop / 50)

        while count < stop:
            try:
                time.sleep(3)
                count += 1
                job = driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
                soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
                data = soup.find_all("span", class_="ng-star-inserted") or soup.find_all("td", class_="row-item")
                z = [i.text.replace("\n", "").strip() for i in data]

                a2, b, c, d, e1, f, g, h, h1, i2, j, k, l, l1, m, n, o, p, q, r, s = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
                i = 0
                while i < len(z):
                    a2.append(z[i])
                    b.append(z[i+1])
                    c.append(z[i+2])
                    d.append(z[i+3])
                    e1.append(z[i+4])
                    f.append(z[i+5])
                    g.append(z[i+6])
                    h.append(z[i+7])
                    h1.append("Cat I" if "Containers" in z[i+7] else z[i+7]),
                    i2.append(z[i+8])
                    j.append(z[i+9])
                    k.append(z[i+10])
                    l.append(z[i+11])
                    try:
                        recycle_consumption = float(z[i+10]) * (float(z[i+11]) / 100)
                    except (ValueError, TypeError):
                        recycle_consumption = "N/A"
                    l1.append(recycle_consumption)
                    m.append(z[i+12])
                    n.append(z[i+13])
                    o.append(z[i+14])
                    p.append(z[i+15])
                    q.append(entity_type)
                    r.append(entity_name)
                    s.append(email_id)

                    if len(z) > i+18 and z[i+16] == "" and z[i+17] == "" and z[i+18] == "":
                        i += 19
                    elif len(z) > i+17 and z[i+16] == "" and z[i+17] == "":
                        i += 18
                    else:
                        i += 16

                df1 = pd.DataFrame({
                    'Registration Type': a2,
                    'Entity Type': b,
                    'Name of the Entity': c,
                    'State': d,
                    'Address': e1,
                    'Mobile Number': f,
                    'Plastic Material Type': g,
                    'Category of Plastic': h,
                    'Category': h1,
                    'Financial Year': i2,
                    'Date': j,
                    'Total Plastic Qty (Tons)': k,
                    'Recycled Plastic %': l,
                    'Recycle Consumption': l1,
                    'GST': m,
                    'GST Paid': n,
                    'EPR invoice No': o,
                    'GST E-Invoice No': p,
                    'Type_of_entity': q,
                    'entity_name': r,
                    'email_id': s
                })

                if count == 1:
                    df = df1
                else:
                    new = df.tail(50).reset_index(drop=True)
                    df1 = df1.reset_index(drop=True)

                    if list(new.columns) == list(df1.columns):
                        try:
                            comp = new.compare(df1)
                            if not comp.empty:
                                df = pd.concat([df, df1], ignore_index=True)
                        except Exception as e:
                            df = pd.concat([df, df1], ignore_index=True)
                    else:
                        df = pd.concat([df, df1], ignore_index=True)

                next_button = driver.find_elements(by=By.CLASS_NAME, value='action-button')[1]
                custom_wait_clickable_and_click(next_button)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
            except:
                break

        print("✅ PROCUREMENT Data fetched successfully")
        
        df_procurement = df

    except Exception as e:
        print(f"❌ Failed Procurement Data")
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
        print("📅 Fetching Credit Wallet Data")
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
        time.sleep(3)
        driver.refresh()
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
        print("✅ Credit Wallet Data fetched successfully")
        
    except Exception as e:
        df_wallet_credit = pd.DataFrame(columns=[
                    'SL_No','Date','Credited_From','Certificate_ID','Value',
                    'Certificate_Owner','Category','Processing_Type','Transaction_ID',
                    'Available_Potential_Prior_Generation','Available_Potential_After_Generation',
                    'Used_Potential_Prior_Generation','Used_Potential_After_Generation',
                    'Cumulative_Potential','Generated_At','Validity','Type_of_entity','entity_name','email_id'
        ])

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
                    post_qty = 0
                try:
                    post_recycled = texts[4]
                except:
                    post_recycled = 0
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
        filename = os.path.join('ALL_EPR_DASHBOARD' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')

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

    time.sleep(50000)

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

    scrape()
except Exception as e:
    print("❌ Error ", e)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="user_profile"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="dropdown-menu show"]/a[contains(text(),"Log")]'))).click()
    time.sleep(10)