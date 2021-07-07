import requests
from bs4 import BeautifulSoup


def next_day(day):
    days = {'Понедельник': 0, 'Вторник': 1, 'Среда': 2,
            'Четверг': 3, 'Пятница': 4, 'Суббота': 5, 'Воскресенье': 6}
    nums = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
            4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}
    n = days[day]
    n = (n + 1) % 6
    return nums[n]


url = 'https://bsu.ru/rasp/?g='
group = '17300'
# group = input()
page = requests.get(url+group).text
soup = BeautifulSoup(page, features="html.parser")
soup = soup.find_all(attrs={'class': 'week'})
soup = soup[0] if '(текущая)' in soup[0] else soup[1]
soup = soup.find(attrs={'class': 'rasp_week'})
soup = soup.find_all('tr')
day = 'Вторник'
nextday = next_day(day)
rasp = []
found = False
for tr in soup:
    if found:
        try:
            if tr.find(attrs={'class': 'rasp_day'}).text == nextday:
                break
        except AttributeError:
            pass
        subj = [tr.find(attrs={'class': 'rasp_time'}).text, tr.find(attrs={'class': 'rasp_subj'}).find('span').text,
                tr.find(attrs={'class': 'rasp_subj_type'}).text, tr.find(attrs={'class': 'rasp_aud'}).text]
        rasp.append(' '.join(subj))
    try:
        if tr.find(attrs={'class': 'rasp_day'}).text == day:
            found = True
    except AttributeError:
        pass

print(rasp)


