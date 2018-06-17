from bs4 import BeautifulSoup as soup
from requests import get
from colorama import Fore, Back, Style
import datetime

def check_time(hour, minute):
    now = datetime.datetime.now()

    if now.hour in range(hour, hour + 3):
        if now.hour == hour + 2 and now.minute < minute:
            return True
        elif now.hour < hour + 3:
            return True
        else:
            return False
    else:
        return False

def cur_match_link():
    url_schedule = 'https://www.fifa.com/worldcup/matches/#groupphase'
    html = get(url_schedule)

    page = soup(html.content, 'html.parser')

    matches = page.find_all('div', attrs = {'class':'fixture'})
    matches = matches[:48]

    cur_match_link = ''
    now = datetime.datetime.now()
    cur_date = str(now.strftime("%d %b %Y"))

    for match in matches:
        info = match.select('.fi-mu__info')[0]
        match_info = info.text.split()
        date = ' '.join(match_info[0:3])

        time_tag = match.find('div', attrs = {'class':'fi-s__score'})
        time_utc = time_tag['data-timeutc']

        time_hour = int(time_utc[0:2])
        time_minute = int(time_utc[3:5])

        time_local_hour = time_hour + 5
        time_local_minute = time_minute + 30

        if date == cur_date and check_time(time_local_hour, time_local_minute):
            score = match.find('span', attrs = {'class':'fi-s__scoreText'}).text.strip()
            link = match.parent['href']
            link = 'http://www.fifa.com' + link

            cur_match_link = link
            break

    return cur_match_link

def live_score():
    url_score = cur_match_link()
    if url_score:
        html = get(url_score)
        live_page = soup(html.content, 'html.parser')

    else:
        print('There are no Matches going on right now.')

if __name__ == '__main__':
    link = cur_match_link()
    if link:
        print(link)
    else:
        print('No matches are going on.')
