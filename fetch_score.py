from bs4 import BeautifulSoup as soup
from requests import get
from colorama import Fore, Back, Style
from datetime import datetime as dt
import itertools

def check_int(text):
    if text == '':
        return False
    try:
        int(text[0])
        return True
    except ValueError:
        return False

def fetch():
    url_schedule = 'https://www.fifa.com/worldcup/matches/#groupphase'
    html = get(url_schedule)

    page = soup(html.content, 'html.parser')

    results = page.find_all('div', attrs = {'class':'result'})
    el_to_remove = ['PEN', 'OG', ',']

    print('\n')
    print('Match\t', end = '')
    print('\t\tDate\t', end = '')
    print('\tScore\t')

    for result in results:
        info = result.select('.fi-mu__info')[0]
        match_info = info.text.split()
        date = ' '.join(match_info[0:3])
        group = ' '.join(match_info[10:12])
        venue = ' '.join(match_info[-3:])

        teams = result.select('.fi-t__n')
        home_team = teams[0].text.split()[0]
        away_team = teams[1].text.split()[0]

        score = result.find('span', attrs = {'class':'fi-s__scoreText'}).text.strip()
        link = result.parent['href']
        link = 'http://www.fifa.com' + link
        html = get(link)
        score_page = soup(html.content, 'html.parser')

        score_list = score_page.find_all('ul', attrs = {'class':'fi-mh__scorers-list'})
        home_score_list = score_list[0].text.split()
        away_score_list = score_list[1].text.split()

        home_scorers = list(filter(lambda a: a not in el_to_remove, home_score_list))
        away_scorers = list(filter(lambda a: a not in el_to_remove, away_score_list))

        print(Fore.GREEN + home_team + ' vs. ' + away_team + '\t', end = '')
        print(date + '\t', end = '')
        print(score)
        print(Style.RESET_ALL, end = '')
        if home_scorers:
            print(Fore.RED + home_team)
            print(Style.RESET_ALL)
            for home_scorer in home_scorers:
                if not check_int(home_scorer):
                    print(home_scorer + ' ', end = '')
                else:
                    print('(' + home_scorer + ')')

        if away_scorers:
            print('\n')
            print(Fore.BLUE + away_team)
            print(Style.RESET_ALL)
            for away_scorer in away_scorers:
                if not check_int(away_scorer):
                    print(away_scorer + ' ', end = '')
                else:
                    print('(' + away_scorer + ')')

        print(Style.RESET_ALL, end = '')
        print('\n')

if __name__ == '__main__':
    fetch()
