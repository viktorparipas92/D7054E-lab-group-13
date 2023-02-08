from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options

url = 'https://www.kaggle.com/unsdsn/world-happiness?select=2019.csv'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)

driver.get(url)

page = driver.page_source
# driver.quit()

soup = BeautifulSoup(page, 'html.parser')

header = soup.find_all('span', attrs={'class':'sc-ikZpkk sc-jIZahH sc-iDiDda fEheNQ fUZPns kwoekg'})
headers_list = [row.get_text(strip = True) for row in header]


text = []
elements = driver.find_elements("xpath", "//div[@class='sc-KpIxo sc-jPgKOH jZTfen fbMUHr']")
for item in elements:
    text.append(item.text)
driver.quit()


# Replace all occurences of \n with ,
row2 = []
for element in text:
    row2.append(element.replace("\n", ","))


# Its a list of index 50, Split it into 50 sublists of 9 values based on comma

row_list = [[] for _ in range(50)]


for index, i in enumerate(row2):
    count = 0
    count_2 = 0
    strng = ""
    for j in i:

        if j == "," :
            count += 1
            row_list[index].append( strng )
            strng = ""
            # to get last value of sublist
            if count == 8:
                row_list[index].append(i[-5:])
        else:
            strng = strng + j


happiness_dict = [dict(zip(headers_list, row)) for row in row_list]



