from bs4 import BeautifulSoup as soup
from requests import get
import re
import os
import time

url = 'http://www.espn.in/football/match?gameId=511040'

#teams list
teams = []

def score():
    #opening the connection and grabbing the page
    response = get(url)

    #html parser
    html = soup(response.text, "html.parser")
    print '\n\n'
    page = html.select('.competitors')
    for data in page:

        # ---------------------- AWAY TEAM SCORE ---------------------
        team_away = data.findAll('div',attrs={'class','away'})
        for container in team_away:
            team_container = container.findAll('div',attrs={'class','team-container'})
            for info in team_container:
                team_info = info.findAll('div',attrs={'class','team-info-wrapper'})
                for anchor in team_info:
                    a = anchor.findAll('a',attrs={'class','team-name'})
                    for an in a:
                        name = an.findAll('span',attrs={'class','long-name'})[0].string
                        teams.append(name)
                        print '\t\t'+name,
                        #short = an.findAll('span',attrs={'clas','abbrev'})[0].string
                        #print short,
            score_container = container.findAll('div',attrs={'class','score-container'})
            for span in score_container:
                sp = span.findAll('span',attrs={'class','score'})[0].string
                print '('+sp.strip()+')',

        # ---------------------- GAME TIME ---------------------

        game_status = data.findAll('div',attrs={'class','game-status'})
        for span in game_status:
            game_time = span.findAll('span',attrs={'class','game-time'})[0].string
            print '\t\t'+game_time,

        # ---------------------- HOME TEAM SCORE ---------------------

        team_home = data.findAll('div',attrs={'class','home'})
        for container in team_home:
            team_container = container.findAll('div',attrs={'class','team-container'})
            for info in team_container:
                team_info = info.findAll('div',attrs={'class','team-info-wrapper'})
                for anchor in team_info:
                    a = anchor.findAll('a',attrs={'class','team-name'})
                    for an in a:
                        name = an.findAll('span',attrs={'class','long-name'})[0].string
                        teams.append(name)
                        print '\t'+name,
                        #short = an.findAll('span',attrs={'clas','abbrev'})[0].string
                        #print short,
            score_container = container.findAll('div',attrs={'class','score-container'})
            for span in score_container:
                sp = span.findAll('span',attrs={'class','score'})[0].string
                print '('+sp.strip()+')',

        # ---------------------- AWAY GOAL SCORER ---------------------
        away_goal = data.findAll('div',attrs={'class','away'})
        for goal_data in away_goal:
            team_away_scorer = goal_data.findAll('ul',attrs={'class','goal'})
            print ''
            for li in team_away_scorer:
                children = li.select('li')
                for child in children:
                    print '\t\t'+re.sub(r'\s', '', child.text)

        # ---------------------- HOME GOAL SCORER ---------------------

        home_goal = data.findAll('div',attrs={'class','home'})
        for goal_data in home_goal:
            team_away_scorer = goal_data.findAll('ul',attrs={'class','goal'})
            print ''
            for li in team_away_scorer:
                children = li.select('li')
                for child in children:
                    print '\t\t\t\t'+re.sub(r'\s', '', child.text)



def stats():
    #opening the connection and grabbing the page
    response = get(url)

    #html parser
    html = soup(response.text, "html.parser")
    print '\n\n\n'
    page = html.select('.stat-list')
    print '\t\t' + teams[0] + '\t\t\t\t\t\t' + teams[1] + '\n'
    for tbody in page:
        table_data = tbody.findAll('tbody')
        for data in table_data:
            tr = data.findAll('tr')
            for sub in tr:
                td = sub.findAll('td')
                MAX = 12
                for stat in td:
                    MIN = len(stat.text)
                    diff = MAX - MIN
                    print '\t\t' + stat.text,
                    while diff > 0:
                        print '',
                        diff = diff - 1
                print ''

def init():
    while True:
        time.sleep(1)
        os.system('cls')
        score()
        print '\n\n\n\n\t\t-----------**------------> STATS <-----------**------------'
        stats()


if __name__ == '__main__':
    init()
