import xlsxwriter
import requests
from bs4 import BeautifulSoup
from io import BytesIO

from PIL import Image
from shutil import copyfileobj

from urllib.request import urlopen


def calculate_scale(file_path, bound_size):
    # check the image size without loading it into memory
    im = Image.open(file_path)
    original_width, original_height = im.size

    # calculate the resize factor, keeping original aspect and staying within boundary
    bound_width, bound_height = bound_size
    ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
    return min(ratios)


workbook = xlsxwriter.Workbook('merten.xlsx')

worksheet = workbook.add_worksheet()
worksheet.set_default_row(100)

worksheet.write('A1', 'Картинка')
worksheet.write('B1', 'Описание')

j = 2
# for n in range(1, 40):
for n in range(1, 2):
    url = 'http://web.se-ecatalog.ru/catalog/search-references?ProductSearch%5Bsearch%5D=MERTEN+&page={}&per-page=50'.format(n)
    page = requests.get(url).text
    soup = BeautifulSoup(page, features="html.parser")
    elements = soup.find('table', {'class': 'table table-striped table-bordered table-catalog'})
    elements = elements.find('tbody')
    elements = elements.find_all('tr')
    for element in elements:
        desciption = element.find_all('td')[2].find('div').text
        img_url = 'http://web.se-ecatalog.ru' + element.find('a').get('href')
        img_page = requests.get(img_url).text
        img_soup = BeautifulSoup(img_page, features="html.parser")
        element = img_soup.find('div', {'class': 'read_more_img_box'})
        element = element.find('a')
        img = element.get('href')
        if img == '/images/image_no.jpg':
            img = 'http://web.se-ecatalog.ru' + img
        img_data = BytesIO(urlopen(img).read())

        response = requests.get(img, stream=True)
        with open('buffer' + '.jpg', 'wb') as file:
            copyfileobj(response.raw, file)

        image_path = 'buffer.jpg'
        bound_width_height = (120, 120)
        resize_scale = calculate_scale(image_path, bound_width_height)

        # worksheet.insert_image('A' + str(j), img, {'image_data': img_data})
        worksheet.insert_image('A' + str(j), img, {'image_data': img_data,
                                                   'x_scale': resize_scale,
                                                   'y_scale': resize_scale})
        worksheet.write('B' + str(j), desciption)
        print(j)

        j += 1
workbook.close()



