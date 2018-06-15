# Add status functionality

from bs4 import BeautifulSoup as soup
from requests import get
from colorama import Fore, Back, Style


print(Fore.RED + 'FIFA 2018 - Schedule')
print(Style.RESET_ALL, end = '')
print(Fore.BLUE)
print('Date\t', end = '')
print('\tTime\t', end = '')
print('\tGroup\t', end = '')
print('\tHome\t', end = '')
print('\tAway\t')
print(Style.RESET_ALL)

url_schedule = 'https://www.fifa.com/worldcup/matches/#groupphase'
html = get(url_schedule)

page = soup(html.content, 'html.parser')

matches = page.find_all('div', attrs = {'class':'fixture'})
matches = matches[:48]

for match in matches:
    info = match.select('.fi-mu__info')[0]
    match_info = info.text.split()
    date = match_info[0:3]
    group_list = match_info[10:12]
    group = ' '.join(group_list)
    venue = match_info[-3:]

    teams = match.select('.fi-t__n')
    home_team = teams[0].text.split()[0]
    away_team = teams[1].text.split()[0]

    time_tag = match.find('div', attrs = {'class':'fi-s__score'})
    time_utc = time_tag['data-timeutc']

    time_hour = int(time_utc[0:2])
    time_minute = int(time_utc[3:5])

    time_local_hour = time_hour + 5
    time_local_minute = time_minute + 30

    if home_team == 'Spain' or away_team == 'Spain':
        print(Fore.RED, end = '')
    else:
        print(Style.RESET_ALL, end = '')

    print(*date, sep = ' ', end = '')
    print('\t', end = '')
    print(str(time_local_hour) + ':' + str(time_local_minute) + '\t', end = '')
    print('\t' + group + '\t', end = '')
    print('\t' + home_team + '\t', end = '')
    if len(home_team) < 8:
        print('\t' + away_team + '\t')
    else:
        print(away_team + '\t')
    # print('Date: ', end = '')
    # print(*date, sep = ' ')
    # print('Venue: ', end = '')
    # print(*venue, sep = ' ')
