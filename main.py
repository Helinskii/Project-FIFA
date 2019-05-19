# Main script to consolidate all functionality

import fetch_schedule
import fetch_points_table
import fetch_score
import live_score

print('Welcome to Project FIFA\n')

while True:
    print('What data would you like to fetch?\n')
    print('1. Schedule\n2. Points Table\n3. Past Results\n4. Live Score')
    option = input('Enter Option: ')
    if option not in ['1', '2', '3', '4']:
        print('Invalid Option.\n')
        continue
    else:
        break

print('\n')
if option == '1':
    fetch_schedule.fetch()
elif option == '2':
    fetch_points_table.fetch()
elif option == '3':
    fetch_score.fetch()
elif option == '4':
    live_score.fetch()
