from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import xlsxwriter
import time

import requests
from bs4 import BeautifulSoup

with open('id3.txt', 'r') as file:
    lines = [line.replace('\n', '') for line in file.readlines()]
workbook = xlsxwriter.Workbook('declaracii.xlsx')

worksheet = workbook.get_worksheet_by_name('decla')
# worksheet.set_default_row(100)

worksheet.write('A1', 'Полное наименование юридического лица')
worksheet.write('B1', 'Телефон')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=selenium")
driver = webdriver.Chrome(chrome_options=chrome_options)

i = 21
m = 25


while i < m:
    line = lines[i]
    url = "https://pub.fsa.gov.ru/rds/declaration/view/{}/applicant".format(
        line)
    driver.get(url)
    # time.sleep(1.5)
    # if i % 5 == 0:
    #     time.sleep(10)
    try:
        text = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "/html/body/fgis-root/div/fgis-rds-view-declaration/fgis-rds-view-declaration-toolbar/div"))).text
    except TimeoutException as te:
        print(te)
        time.sleep(5)
        continue
    try:
        text = driver.find_element_by_xpath('/html/body/fgis-root/div/fgis-rds-view-declaration/div/div/div/div/fgis-rds-view-application-applicant/fgis-card-block-wrapper/fgis-card-block/div/div[2]/div/fgis-card-info-row/div[2]/span').text
        worksheet.write('A{}'.format(str(i + 2)), text)
    except BaseException as be:
        print(be)
    try:
        text = driver.find_element_by_xpath(
            '/html/body/fgis-root/div/fgis-rds-view-declaration/div/div/div/div/fgis-rds-view-application-applicant/fgis-card-block-wrapper/fgis-card-block/div/div[2]/div/fgis-rds-view-contacts/fgis-card-row-spoiler/div[2]/fgis-card-edit-row-two-columns/fgis-card-info-row[1]/div[2]/p').text
        worksheet.write('B{}'.format(str(i + 2)), text)
    except BaseException as be:
        print(be)
    i += 1
workbook.close()
