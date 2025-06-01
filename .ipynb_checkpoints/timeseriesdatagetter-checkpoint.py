import requests
import json
import csv
import os
from datetime import datetime
import time

url = 'https://edge.pse.com.ph/common/DisclosureCht.ax'

# Headers - must match DevTools
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://edge.pse.com.ph',
    'Referer': 'https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id=114', 
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Cookie': '<your actual session cookie here>'   ##adjust based on your actual session cookie
}

os.makedirs('timeseriesdata', exist_ok=True)

with open('updated_finalstocks.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        company_id = row['companyId']
        security_id = row['securityId']
        company_name = row['companyName'].replace('/', '-')
        company_file_path = f'historicaldata/{company_name}_historical.csv'

        print(f"\nFetching data for: {company_name} | companyId: {company_id}")

        payload = {
            'cmpy_id': company_id,
            'security_id': security_id,
            'startDate': '01-01-2000',
            'endDate': datetime.today().strftime('%m-%d-%Y')
        }

        # POST request
        r = requests.post(url, json=payload, headers=headers)
        print("Status code:", r.status_code)

        if r.status_code == 200 and r.text.strip():
            try:
                hist_data = json.loads(r.text)
                if 'chartData' in hist_data:
                    hist_values = hist_data['chartData']
                    if hist_values:
                        print("Data received!")
                        with open(company_file_path, 'w', newline='') as company_file:
                            writer = csv.writer(company_file)
                            writer.writerow(['Date', 'Value', 'Open', 'Close', 'High', 'Low'])
                            for item in hist_values:
                                date_object = datetime.strptime(item['CHART_DATE'], '%b %d, %Y 00:00:00')
                                shortdate = date_object.strftime('%d/%m/%y')
                                writer.writerow([
                                    shortdate,
                                    item['VALUE'],
                                    item['OPEN'],
                                    item['CLOSE'],
                                    item['HIGH'],
                                    item['LOW']
                                ])
                        print(f" Data saved for {company_name}!")
                    else:
                        print("No chart data found.")
                else:
                    print(f" 'chartData' not in JSON: {hist_data}")
            except json.JSONDecodeError:
                print(f" Failed to parse JSON for {company_name}")
        else:
            print(f" No data or error from server for {company_name}.")

        time.sleep(5)  # Sleep to avoid rate limits; adjust as needed

print(" All data downloaded successfully!")
