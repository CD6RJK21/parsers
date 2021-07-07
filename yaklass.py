from selenium import webdriver
from time import sleep


# test_page = input()
# search_text = input()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=selenium")
driver = webdriver.Chrome(chrome_options=chrome_options)

with open('config.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    page = lines[1].replace('\n', '')
    search_text = lines[0].replace('\n', '')

driver.get(page)
found = False
first = True
while not found:
    sleep(4)
    try:
        if first:
            first = False
            button = driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div/div[3]/div/div/div[4]/div[2]/div[2]/a')
            button.click()
    except BaseException as be:
        print(be)
    try:
        if search_text in driver.page_source:
            found = True if input() == '1' else False
    except BaseException as be:
        print(be)
    try:
        button = driver.find_element_by_id('submitAnswerBtn')
        button.click()
        button = driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div/div[3]/div/div/div[4]/div[2]/div[2]/a')
        button.click()
    except BaseException as be:
        print(be)
        sleep(10)
