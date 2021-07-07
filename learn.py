import requests
from bs4 import BeautifulSoup
import shutil


def find_content(elements):
    all_text = []
    for element in elements:
        element = element.find('td', {'class': 'title al va-t word-break'})
        link_text = element.find('div', {'class': 'detail'})
        link_text = link_text.find('div', {'class': 'di-ib clearfix'}).find('a').text

        img = element.find('a', {'class': 'hoverinfo_trigger fl-l ml12 mr8'})
        img = img.find('img')
        img = img.get('data-src')

        response = requests.get(img, stream=True)
        with open(link_text + '.jpg', 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

        all_text.append(link_text)
    return all_text


url = "https://myanimelist.net/topanime.php"

page = requests.get(url).text

soup = BeautifulSoup(page, features="html.parser")

tds = soup.find_all('tr', {'class': 'ranking-list'})

print(find_content(tds))
