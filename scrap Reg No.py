import datetime
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
 
a2, b, c, d, ee, f, g = [], [], [], [], [], [], []
 
def custom_wait_clickable_and_click(elem, attempts=20):
    count = 0
    while count < attempts:
        try:
            elem.click()
            break
        except:
            time.sleep(1)
            count += 1
 
def scrape_dashboard_data(driver):
    while True:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
           
            rows = soup.select('tbody#ScrollableSimpleTableBody tr')
            for row in rows:
                date = row.select_one('td:nth-of-type(1) span').text.strip()
                l_name = row.select_one('td:nth-of-type(2) span').text.strip()
                t_name = row.select_one('td:nth-of-type(3) span').text.strip()
                app_no = row.select_one('td:nth-of-type(4) span').text.strip()
                reg_num = row.select_one('td:nth-of-type(5) span').text.strip()
                type_p = row.select_one('td:nth-of-type(6) span').text.strip()
                a_status = row.select_one('td:nth-of-type(7) span').text.strip()
 
                a2.append(date)
                b.append(l_name)
                c.append(t_name)
                d.append(app_no)
                ee.append(reg_num)
                f.append(type_p)
                g.append(a_status)
            try:
                driver.find_element(By.XPATH, '//button[@ngbtooltip="Next"]').click()
                time.sleep(2)
            except:
                break
        except Exception as e:
            print("No more data to scrape or an error occurred:", e)
            break
 
def dashboard_data():
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get('https://eprplastic.cpcb.gov.in/#/plastic/home/main_dashboard')
    time.sleep(5)
 
    date_input = driver.find_element(By.XPATH, '//div[contains(text(),"Show")]//input[@aria-autocomplete="list"]')
    date_input.clear()
    date_input.send_keys("100")
    click = driver.find_element(by=By.XPATH, value='//div[@role="option"]/span[text()="100"]')
    custom_wait_clickable_and_click(click)
   
    scrape_dashboard_data(driver)
    # driver.quit()
 
dashboard_data()
 
now = datetime.datetime.now()
df = pd.DataFrame({
    'Date of Application': a2,
    'Legal Name': b,
    'Trade Name': c,
    'App. No.': d,
    'Registration Number': ee,
    'Type of PIBOr': f,
    'Application Status': g,
})
df.to_excel('Scraped_dashboard_' + str(now.strftime("%d%m%Y_%H%M%S")) + '.xlsx', index=False)
