from bs4 import BeautifulSoup as soup
from requests import get
from colorama import Fore, Back, Style
import datetime
import time
import sys

el_to_remove = ['PEN', 'OG', ',']

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

def check_int(text):
    if text == '':
        return False
    try:
        int(text[0])
        return True
    except ValueError:
        return False

def cur_match_link():
    url_schedule = 'https://www.fifa.com/worldcup/matches/#groupphase'
    html = get(url_schedule)

    page = soup(html.content, 'html.parser')

    matches = page.find_all('div', attrs = {'class':'live'})
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
            link = match.parent['href']
            link = 'http://www.fifa.com' + link

            cur_match_link = link
            break

    return cur_match_link

def fetch():
    url_score = cur_match_link()
    if url_score:
        status = ''
        html = get(url_score)
        live_page = soup(html.content, 'html.parser')
        match_status = live_page.find('div', attrs = {'class':'fi-s__status'})
        for tag in match_status.find_all('span'):
            if 'hidden' not in tag['class']:
                status = tag.text.strip()

        minute = live_page.find('span', attrs = {'class':'minute'}).text

        home = live_page.find('div', attrs = {'class':'home'})
        home_team = home.text.strip().split('\n')
        home_team_name = ' '.join(home_team[:-1])
        home_team_abbr = home_team[-1]

        away = live_page.find('div', attrs = {'class':'away'})
        away_team = away.text.strip().split('\n')
        away_team_name = ' '.join(away_team[:-1])
        away_team_abbr = away_team[-1]

        score = live_page.find('div', attrs = {'class':'fi-s__score'}).text.strip()
        home_score = score[0]
        away_score = score[-1]

        score_list = live_page.find_all('ul', attrs = {'class':'fi-mh__scorers-list'})
        home_score_list = score_list[0].text.split()
        away_score_list = score_list[1].text.split()

        home_scorers = list(filter(lambda a: a not in el_to_remove, home_score_list))
        away_scorers = list(filter(lambda a: a not in el_to_remove, away_score_list))

        print(Fore.RED + 'LIVE MATCH')
        print('\n')
        print(Fore.GREEN + home_team_name + ' (' + home_team_abbr + ') ' + home_score, end = '')
        print(' - ', end = '')
        print(away_score + ' ' + away_team_name + ' (' + away_team_abbr + ')')
        print(Style.RESET_ALL, end = '')
        print('Status: ', end = '')
        if status:
            print(status)
        else:
            print(minute)

        if home_scorers:
            print(Fore.RED + home_team_name)
            print(Style.RESET_ALL, end = '')
            for home_scorer in home_scorers:
                if not check_int(home_scorer):
                    print(home_scorer + ' ', end = '')
                else:
                    print('(' + home_scorer + ')')

        if away_scorers:
            print('\n')
            print(Fore.BLUE + away_team_name)
            print(Style.RESET_ALL, end = '')
            for away_scorer in away_scorers:
                if not check_int(away_scorer):
                    print(away_scorer + ' ', end = '')
                else:
                    print('(' + away_scorer + ')')

        print(Style.RESET_ALL)

    else:
        print('There are no Matches going on right now.')

if __name__ == '__main__':
    fetch()
