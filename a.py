import xlsxwriter
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.request import urlopen

workbook = xlsxwriter.Workbook('jkh.xlsx')

worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Адрес')
worksheet.write('B1', 'Кадастровый номер')
worksheet.write('C1', 'Ссылка на управляющую организацию')

j = 2
# for n in range(1, 40):
for n in range(1, 50):
    try:
        url = 'https://www.reformagkh.ru/myhouse/profile/view/900{}'.format(str(n).rjust(4, '0'))
        page = requests.get(url).text
        soup = BeautifulSoup(page, features="html.parser")
        head = soup.find('h2', {'class': 'text-white'})
        worksheet.write('A' + str(j), head.text)
        table = soup.find('div', {'class': 'tab-content fade tab-pane show active'}).find('table', {'class': 'w-100 simple-table'}).find_all('tr')
        for element in table:
            if element.find('td').text == 'Кадастровый номер':
                worksheet.write('B' + str(j), element.find_all('td')[-1].text)
                break

        profiles = url.replace('view', 'management')
        page = requests.get(profiles).text
        soup = BeautifulSoup(page, features="html.parser")

        table = soup.find('div', {
            'class': 'tab-content fade tab-pane show active'}).find('table', {
            'class': 'w-100 simple-table'}).find_all('tr')
        for element in table:
            if element.find('td').text == 'Домом управляет':
                worksheet.write('C' + str(j), element.find_all('td')[-1]['href'])
                break

        print(j)

        j += 1
    except AttributeError as ae:
        j -=1
        print(ae)
workbook.close()



