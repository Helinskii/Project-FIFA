# Developer     - Shubham Saha
# Github        - https://github.com/Helinskii
# Telegram      - https://t.me/Helinskii
# @license      - Code and Contributions have 'MIT License'
#                 More Details: LICENSE
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software with proper credit to the original author.

# Fetches the points table

# Import libraries
from bs4 import BeautifulSoup
from requests import get
from colorama import Fore, Back, Style

# Main fetch function
def fetch():

    print('Glossary')
    print('GP:\tGames Played')
    print('W:\tWins')
    print('D:\tDraws')
    print('L:\tLosses')
    print('F:\tGoals For')
    print('A:\tGoals Against')
    print('GD:\tGoal Difference')
    print('P:\tPoints')
    print('\n')

    # URL for scraping the data
    url_standings = 'http://www.espn.in/football/table/_/league/fifa.world'
    html = get(url_standings)
    page = BeautifulSoup(html.content, 'html.parser')

    standings_table = page.select('.has-team-logos')

    heads = page.find_all('thead', attrs = {'class':'standings-categories'})
    groups = []
    categories = []
    count_categories = 0

    # Loop through all the 'headings' and make lists out of them
    for head in heads:
        count_group_name = 0
        for title in head:
            count_group_name += 1
            count_categories += 1

            if count_group_name == 1:
                groups.append(title.text)
            else:
                if (count_categories > 1 and count_categories <= 9):
                    categories.append(title.text)

    all_groups = page.find_all('tr', attrs = {'class':'standings-row'})
    divide_counter = 0
    group_counter = 0
    group_track = 0

    # Loop through all the teams segregated in to groups
    for group in all_groups:
        row_list = []
        if divide_counter == 0:
            print(Fore.BLUE + Style.BRIGHT + groups[group_track] + '\t\t\t', end = '')
            for category in categories:
                print(category + '\t', end = '')
            divide_counter += 1
            group_track += 1

        for team in group:
            row_list.append(team.text)

        team_number = row_list[0][0]
        team_name = row_list[0][1:-3]
        team_abbr = row_list[0][-3:]
        print(Style.RESET_ALL)
        print(team_number + ' ', end = '')
        print(team_name, end = '')
        if len(team_name) > 5:
            print('\t(' + team_abbr + ')\t', end = '')
        else:
            print('\t\t(' + team_abbr + ')\t', end = '')

        for i in range(1, len(row_list)):
            print(row_list[i] + '\t', end = '')
        divide_counter += 1
        if divide_counter > 4:
            print('\n')
            divide_counter = 0

if __name__ == '__main__':
    fetch()
