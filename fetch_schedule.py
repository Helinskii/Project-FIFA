# Fetches the schedule
# Use with 'python fetch_schedule' directly, or call it from the menu


# Import libraries
from bs4 import BeautifulSoup as soup
from requests import get
from colorama import Fore, Back, Style
from datetime import datetime as dt

# Main fetch function
def fetch():
    print(Fore.RED + 'FIFA 2018 - Schedule')
    print(Style.RESET_ALL, end = '')

    # URL for scraping data
    url_schedule = 'https://www.fifa.com/worldcup/matches/#groupphase'
    html = get(url_schedule)

    # Creating a 'soup' of the fetched webpage
    page = soup(html.content, 'html.parser')

    # Find all the instances of the upcoming matches
    matches = page.find_all('div', attrs = {'class':'fixture'})
    matches = matches[:48]

    # Find all the instances of the past matches
    results = page.find_all('div', attrs = {'class':'result'})

    # For an organized display
    print(Fore.MAGENTA + "Previous Matches:")
    print(Fore.BLUE)
    print('Date\t', end = '')
    print('\tGroup\t', end = '')
    print('Home\t', end = '')
    print('\tAway\t', end = '')
    print('\tFinal Score\t')
    print(Style.RESET_ALL)

    # Loop to print data on past matches (Date, Teams and Score)
    for result in results:
        info = result.select('.fi-mu__info')[0]
        match_info = info.text.split()
        # Date
        date = ' '.join(match_info[0:3])
        # Group Name
        group = ' '.join(match_info[10:12])
        # Venue Name
        venue = ' '.join(match_info[-3:])

        # Teams
        teams = result.select('.fi-t__n')
        home_team = teams[0].text.split()[0]
        away_team = teams[1].text.split()[0]

        # Score
        score = result.find('span', attrs = {'class':'fi-s__scoreText'}).text.strip()

        print(date + '\t', end = '')
        print(group + '\t', end = '')
        print(home_team + '\t', end = '')
        if len(home_team) < 8:
            print('\t' + away_team + '\t', end = '')
        else:
            print(away_team + '\t', end = '')
        if len(away_team) < 8:
            print('\t' + score + '\t')
        else:
            print(score + '\t')

    now = dt.now()
    cur_date = str(now.strftime("%d %b %Y"))

    counter = 0

    print(Fore.BLUE)
    print('Date\t', end = '')
    print('\tTime\t', end = '')
    print('Group\t', end = '')
    print('Home\t', end = '')
    print('\tAway\t')
    print(Style.RESET_ALL)

    print(Fore.MAGENTA, end = '')
    print("Today's Matches:\n")

    # Loop through all the instances of today's matches
    for match in matches:
        info = match.select('.fi-mu__info')[0]
        match_info = info.text.split()
        date = ' '.join(match_info[0:3])
        group_list = match_info[10:12]
        group = ' '.join(group_list)
        venue = ' '.join(match_info[-3:])

        # Checks if the match is today for segragation
        if date == cur_date:
            teams = match.select('.fi-t__n')
            home_team = teams[0].text.split()[0]
            away_team = teams[1].text.split()[0]

            # Finds the time for the match
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

            print(date + '\t', end = '')
            print(str(time_local_hour) + ':' + str(time_local_minute) + '\t', end = '')
            print(group + '\t', end = '')
            print(home_team + '\t', end = '')
            if len(home_team) < 8:
                print('\t' + away_team + '\t')
            else:
                print(away_team + '\t')
            counter += 1

    print('\n', end = '')
    print(Fore.MAGENTA, end = '')
    print("Upcoming Matches:\n")

    # Loops through all the instances of the matches that are upcoming and not today
    for match in matches[counter:]:
        info = match.select('.fi-mu__info')[0]
        match_info = info.text.split()
        date = ' '.join(match_info[0:3])
        group_list = match_info[10:12]
        group = ' '.join(group_list)
        venue = ' '.join(match_info[-3:])

        teams = match.select('.fi-t__n')
        home_team = teams[0].text.split()[0]
        away_team = teams[1].text.split()[0]

        time_tag = match.find('div', attrs = {'class':'fi-s__score'})
        time_utc = time_tag['data-timeutc']

        time_hour = int(time_utc[0:2])
        time_minute = int(time_utc[3:5])

        time_local_hour = time_hour + 5
        time_local_minute = time_minute + 30

        # Change team name here to highlight it
        if home_team == 'Argentina' or away_team == 'Argentina':
            print(Fore.RED, end = '')
        else:
            print(Style.RESET_ALL, end = '')

        print(date + '\t', end = '')
        print(str(time_local_hour) + ':' + str(time_local_minute) + '\t', end = '')
        print(group + '\t', end = '')
        print(home_team + '\t', end = '')
        if len(home_team) < 8:
            print('\t' + away_team + '\t')
        else:
            print(away_team + '\t')

if __name__ == '__main__':
    fetch()
