from bs4 import BeautifulSoup as soup
from requests import get

url_standings = 'http://www.espn.in/football/table/_/league/fifa.world'
html = get(url_standings)
page = soup(html.content, 'html.parser')

heads = page.find_all('thead', attrs = 'class':'standings-categories'})
groups = []
categories = []
count_categories = 0

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

all_groups = page.find_all('tr', attrs = {'classs':'standings-row'})
