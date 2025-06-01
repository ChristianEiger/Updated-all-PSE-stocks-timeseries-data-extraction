from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://edge.pse.com.ph/companyDirectory/form.do")
time.sleep(2)


try:
    agree_btn = driver.find_element(By.ID, "iAgreeBtn")
    driver.execute_script("arguments[0].click();", agree_btn)
    print("Clicked I AGREE (if it was there).")
    time.sleep(1)
except:
    print("No I AGREE button found.")

all_data = []
page_num = 1


while True:
    print(f"\n🔄 Extracting data from page {page_num}...")

    tables = driver.find_elements(By.CSS_SELECTOR, "table.list")
    if len(tables) < 2:
        print("Could not find the main 'company list' table. Exiting loop.")
        break

    company_table = tables[1]


    rows = company_table.find_elements(By.TAG_NAME, "tr")[1:]
    if not rows:
        print("No data rows found in the directory. Exiting loop.")
        break


    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 3:
            continue

        company_name = cols[0].text.strip()
        symbol       = cols[1].text.strip()
        sector       = cols[2].text.strip()


        company_id   = ""
        security_id  = ""
        try:
            link_elem = cols[0].find_element(By.TAG_NAME, "a")
            onclick = link_elem.get_attribute("onclick") or ""

            matches = re.findall(r"'(.*?)'", onclick)
            if len(matches) >= 2:
                company_id, security_id = matches[0], matches[1]
        except Exception:

            pass

        all_data.append([
            company_name,
            symbol,
            sector,
            company_id,
            security_id
        ])
        print(f"Extracted: {company_name} | {symbol} | {sector} | {company_id} | {security_id}")


    try:

        next_page_xpath = f"//a[contains(text(), '{page_num+1}')]"
        next_link = driver.find_element(By.XPATH, next_page_xpath)
        driver.execute_script("arguments[0].click();", next_link)
        time.sleep(2) 
        page_num += 1
    except:
        print("Reached last page (no next-page link).")
        break


with open('pse_companies_full.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['CompanyName','Symbol','Sector','CompanyId','SecurityId'])
    writer.writerows(all_data)

print("\nData extraction complete! Saved to 'pse_companies_full.csv'")
driver.quit()
