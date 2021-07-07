import xlsxwriter
import requests
from bs4 import BeautifulSoup
with open('id3.txt', 'r') as file:
    lines = [line.replace('\n', '') for line in file.readlines()]
workbook = xlsxwriter.Workbook('merten.xlsx')

worksheet = workbook.add_worksheet()
worksheet.set_default_row(100)

worksheet.write('A1', 'Полное наименование юридического лица')



for i in range(30):
    line = lines[i]
    url = "https://pub.fsa.gov.ru/rds/declaration/view/{}/applicant".format(line)
    page = requests.get(url, verify=False).text
    soup = BeautifulSoup(page, features="html.parser")
    data = soup.find('div', {'class': 'card-block__block-container card-block__block-container_single'})
    data = data.find('div', {'class': 'card-block__container'})
    data = data.find('div', {'class': 'card-block__container__content'})
    data = data.find_all('fgis-card-info-row')
    if "Полное наименование" in data.find('div', {'class': 'info-row__header'}).find('div').text:
        worksheet.write('A{}'.format(str(i + 2)), data.find('div', {'class': 'info-row__text'}).find('span').text)
        continue


