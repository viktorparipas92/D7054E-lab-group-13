from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = ("https://covid19.who.int/table")
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 10)

driver.get(url)
#  To scroll down table in order to get all records - It doesn't work
for i in range(5):
    inner_scroll_bar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tbody")))
    # element = driver.find_element_by_id('gatsby-focus-wrapper')
    scroll_top = 12000
    driver.execute_script("arguments[0].scrollTop = arguments[1]", inner_scroll_bar)
    inner_scroll_contents = inner_scroll_bar.text



# Path for Headers / Totals
temp_list =[]

elements = driver.find_elements(By.CLASS_NAME, "th")

for item in elements:
    temp_list.append(item.text)


# Split headers / totals

totals_list = []
totals_list = temp_list[8:]
headers_list = temp_list[:8]



# List for Rows


elements = driver.find_elements(By.CLASS_NAME, "td")
rows_list = []

for item in elements:
    rows_list.append(item.text)

driver.quit()

# Slice rows list of 160 values, into sublists of 8 values
sublist_size = 8
row_list_2 =  [rows_list[i:i+sublist_size] for i in range(0, len(rows_list), sublist_size)]



# turn measures to float from strings

row_list_3 = row_list_2.copy()
row_list_3 = [[value.replace(",", "") for value in sublist] for sublist in row_list_3]
for i in range(2,20):
    for j in range(1,8):
        if row_list_3[i][j] != "":
            row_list_3[i][j] = float(row_list_3[i][j])



# Create dictionary based on Header - Rows
covid_dict = [dict(zip(headers_list, row)) for row in row_list_3]

