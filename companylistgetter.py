import requests
from bs4 import BeautifulSoup
import re
import csv

all_data = []

for page_no in range(1, 6):
    url = f"https://edge.pse.com.ph/companyDirectory/search.ax?page={page_no}"
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    for a_tag in soup.find_all('a', onclick=True):
        onclick = a_tag['onclick']
        match = re.match(r"cmDetail\('(\d+)','(\d+)'\);return false;", onclick)
        if match:
            company_id = match.group(1)
            security_id = match.group(2)
            company_name = a_tag.text.strip()
            all_data.append((company_id, security_id, company_name))

with open('updated_finalstocks.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['companyId', 'securityId', 'companyName'])
    for row in all_data:
        writer.writerow(row)

print("Data extraction complete! Saved to 'updated_finalstocks.csv'")
