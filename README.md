# Updated All PSE Stocks Timeseries Data Extraction

Author: [Christian Regie Jabagat](https://github.com/ChristianEiger)  
Repository: [Updated-all-PSE-stocks-timeseries-data-extraction](https://github.com/ChristianEiger/Updated-all-PSE-stocks-timeseries-data-extraction)

---

## Overview

This repository contains a Python-based data extraction script for the **Philippine Stock Exchange (PSE)**. It extracts:

 **Company Directory information** (Company Name, Stock Symbol, Sector, CompanyId, SecurityId)  
 **Timeseries historical stock data** via PSE’s hidden APIs  

The extracted data is saved as **CSV files** for easy use in data analytics or financial modeling.

---

## Features

- Extracts **all available PSE-listed company information**.
- Extracts **timeseries stock data** for each company.
- Uses **Selenium** to navigate the PSE’s online directory and fetch hidden form values (CompanyId and SecurityId).
- Outputs data as CSV for seamless analysis.
- Designed to be **headless and automated**.

---

## Usage

1. **Clone the repository:**
2. **Install dependencies:**
3. **Run company profile extraction script:companylistgetter.py**
4. **Run company data extraction script based on company profile in step 3:timeseriesgetter.py**

---

##  Notes & Troubleshooting

- Make sure **Google Chrome** and **chromedriver** are installed and accessible.
- For **macOS**, you may need to grant accessibility permissions to the terminal.
- The script uses **headless Selenium** for seamless, automated scraping.

---

##  Contributions & Contact

Feel free to **open a pull request or issue** if you’d like to contribute or report a problem.

For questions or collaborations, please reach out via [christianjabagat@gmail.com].

---

Happy scraping!


