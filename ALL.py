from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

url = "https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

driver = webdriver.Chrome('............')  # put your google chrome driver link here
driver.get(url)
time.sleep(1)
bhk_button = driver.find_element_by_xpath('/html/body/nav[1]/div/ul[1]/li[3]').click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/nav[1]/div/ul[1]/li[3]/ul/li/div/ul/li[3]/label/span").click();
time.sleep(1)
driver.find_element_by_xpath("/html/body/nav[1]/div/ul[1]/li[3]/ul/li/div/ul/li[4]/label/span").click();
time.sleep(1)

html_src = driver.page_source

driver.quit()

soup = BeautifulSoup(html_src, "lxml")

info = soup.find('div', {'class': 'searchlistitems'})
totalEntries = info.find('input')['value']

j = -1

colms = ['BHK', 'Location', 'Prices (in Rupees)', 'Rates(per Square feet)', 'Area', 'Facing', 'Status', 'Floor no.',
         'Furnish type', 'Freehold', 'No. of bathrooms', 'Posted by', 'Posted Time']
raw_data = [[] for x in range(len(colms))]
n = 0
for i in info.stripped_strings:
    if i == 'Featured':
        continue
    if j == 0:
        raw_data[0].append(i[0:1])
    elif j == 1:
        raw_data[1].append(i)
    elif j == 4:
        raw_data[2].append(i)  # prices
    elif j == 5:
        raw_data[3].append(i.replace("@", ""))  # Rates(per Square feet)
    elif j == 7:
        raw_data[4].append(i)  # Area
    elif j == 10:
        raw_data[5].append(i)  # Facing
    elif j == 12:
        raw_data[6].append(i)  # Status
    elif j == 13:
        raw_data[7].append(i)  # Floor no
    elif j == 14:
        raw_data[8].append(i)  # Furnish type
    elif j == 15:
        raw_data[9].append(i)  # Freehold
    elif j == 16:
        raw_data[10].append(i[0:1])  # No. of bathrooms
    elif j == 17:
        raw_data[11].append(i)  # Posted by
    elif j == 18:
        raw_data[12].append(i.replace('Posted:', ' '))  # Posted Time

    j = j + 1

df = pd.DataFrame({colms[i]: raw_data[i] for i in range(len(colms))})
print(df)

file_name = 'All.xlsx'

df.to_excel(file_name, sheet_name='Sheet1', index=False)

print('Process Successful!!')
