import requests
from bs4 import BeautifulSoup
import shutil


def find_content(elements):
    all_text = []
    for element in elements:
        element = element.find('a', {'class': 'sc-feJyhm gTpfnr'})
        link_text = element.get('title')

        img_url = element.get('href')
        img = element.find('a', {'class': 'hoverinfo_trigger fl-l ml12 mr8'})
        img = img.find('img')
        img = img.get('data-src')

        response = requests.get(img, stream=True)
        with open('flowers\\' + link_text + '.jpg', 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

        all_text.append(link_text)
    return all_text


url = "https://youla.ru/user/57958909d53f3d7f5dbb357e"

page = requests.get(url).text

soup = BeautifulSoup(page, features="html.parser")

tds = soup.find_all('div', {'class': 'sc-cMljjf sc-gPEVay ekWwLJ'})

find_content(tds, url)
