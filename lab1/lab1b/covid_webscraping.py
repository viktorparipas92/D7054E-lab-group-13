from bs4 import BeautifulSoup
import requests

url = ("https://covid19.who.int/table")

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser') #text and the parser to use  CHANGE from "html5lib" to "html.parser"

covid = soup.find('div', attrs={'role':'table'})


# List for Headers
headers_first = covid.find('div', attrs={'class':"sc-AxjAm kbGAkV"})
headers_list_first = [row.get_text(strip = True) for row in headers_first]
headers = covid.find_all('div', attrs={'class':"sc-pcJja jjDvpo"})
headers_list_second = [row.get_text(strip = True) for row in headers]

headers_list = headers_list_first + headers_list_second
headers_list.remove('')

# List for Totals
totals = covid.find_all('div', attrs={'data-id':"totals-header"})
totals_list = [row.get_text(strip = True) for row in totals]

# List for Rows
rows = covid.find_all('div', class_=lambda class_: class_ and ('sc-AxjAm sc-pliRl ylFcR' in class_ or 'sc-pXZzD fMTLAh' in class_))
rows_list = [row.get_text(strip = True) for row in rows]

# For first 2 rows, one value is missing
row_list = rows_list.insert( 7, '')
row_list = rows_list.insert( 15, '')

# Slice rows list of 158 values, into sublists of 8 values
sublist_size = 8
row_list_2 =  [rows_list[i:i+sublist_size] for i in range(0, len(rows_list), sublist_size)]


row_list_3 = row_list_2.copy()
row_list_3 = [[value.replace(",", "") for value in sublist] for sublist in row_list_3]

# turn measures to float from strings
for i in range(2,20):
    for j in range(1,8):
        if row_list_3[i][j] != "":
            row_list_3[i][j] = float(row_list_3[i][j])


# Create dictionary based on Header - Rows
covid_dict = [dict(zip(headers_list, row)) for row in row_list_3]

