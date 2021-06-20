import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.propertiesguru.com/residential-search/2bhk-residential_apartment_flat-for-sale-in-new_delhi"
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = requests.get(url, headers=headers)

var = req.status_code
print(var)

soup = BeautifulSoup(req.content, "lxml")

info = soup.find('div', {'class': 'searchlistitems'})
totalEntries = info.find('input')['value']

j = -3

colms = ['Location', 'Prices (in Rupees)', 'Rates(per Square feet)', 'Area(in Square Feet)', 'Facing', 'Status',
         'Floor no.', 'Furnish type', 'Freehold', 'No. of bathrooms', 'Posted by', 'Posted Time']
raw_data = [[] for x in range(len(colms))]

for i in info.stripped_strings:
    print(i + str(j))  # for each line correlation with j
    if j == 0:
        raw_data[0].append(i)  # Location
    elif j == 2:
        raw_data[1].append(i)  # Prices (in Rupees)
    elif j == 3:
        raw_data[2].append(i.replace("@", "").replace("/Sq Ft.", ""))  #Rates(per Square feet)
    elif j == 5:
        raw_data[3].append(i)   #Area(in Square Feet)
    elif j == 8:
        raw_data[4].append(i)   #Facing
    elif j == 10:
        raw_data[5].append(i)   #Status
    elif j == 11:
        raw_data[6].append(i)   #Floor no.
    elif j == 12:
        raw_data[7].append(i)   #Furnish type
    elif j == 13:
        raw_data[8].append(i)   #Freehold
    elif j == 14:
        raw_data[9].append(i)   #No. of bathrooms
    elif j == 15:
        raw_data[10].append(i)  #Posted by
    elif j == 16:
        raw_data[11].append(i.replace('Posted:', ' '))  #Posted Time
    elif j == 20:
        j = 0
        raw_data[0].append(i)

    j = j + 1

df = pd.DataFrame({colms[i]: raw_data[i] for i in range(len(colms))})
print(df)

file_name = '2BHK.xlsx'

df.to_excel(file_name, sheet_name='Sheet1', index=False)

print('FINISHED')
