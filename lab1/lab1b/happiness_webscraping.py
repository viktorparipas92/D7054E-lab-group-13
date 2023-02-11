from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


WORLD_HAPPINESS_REPORT_URL = (
    'https://www.kaggle.com/unsdsn/world-happiness?select=2019.csv'
)


def scrape():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(driver, 40)

    driver.get(WORLD_HAPPINESS_REPORT_URL)

    #  To scroll down table in order to get all records
    for i in range(10):
        inner_scroll_bar = wait.until(
            ec.presence_of_element_located((
                By.XPATH,
                "/html/body/main/div[1]/div[1]/div[6]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]"
            ))
        )
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            inner_scroll_bar
        )

    # Path for Headers
    path = "/html/body/main/div[1]/div[1]/div[6]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[4]/div[1]"
    elements = driver.find_elements("xpath", path)

    # Create list with Headers by finding specific span element
    headers_list = []
    for element in elements:
        spans = element.find_elements("xpath", ".//span")
        for span in spans:
            # check if the span has the desired text
            if span.text != "":
                headers_list.append(span.text)

    # Find path for rows
    # For each span element which contains one row of table, add it to a list
    rows = []
    for i in range(1, 160):
        path = "/html/body/main/div[1]/div[1]/div[6]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[7]/span[2]"
        path = f"{path[:-2]}{str(i)}]"
        elements = driver.find_elements("xpath", path)
        for item in elements:
            rows.append(item.text)
            index = i

    driver.quit()

    # Replace all occurrences of \n with ,
    row2 = []
    for element in rows:
        row2.append(element.replace("\n", ","))

    # It's a list of 156 strings,
    # Split it into 156 sub-lists of 9 values based on comma
    row_list = [[] for _ in range(index)]
    for index, i in enumerate(row2):
        count = 0
        strng = ""
        for j in i:

            if j == ",":
                count += 1
                row_list[index].append(strng)
                strng = ""
                # to get last value of sublist
                if count == 8:
                    row_list[index].append(i[-5:])
            else:
                strng += j

    # turn measures to float from strings
    for i in range(index):
        for j in range(2, 9):
            if row_list[i][j] != "":
                row_list[i][j] = float(row_list[i][j])

    #  Create dictionary based on headers, rows
    happiness_dict = [dict(zip(headers_list, row)) for row in row_list]
    return happiness_dict


if __name__ == '__main__':
    happiness_dict = scrape()
