#!./env/bin/python
import argparse
import datetime
import sys
import time

from utils.banner import print_banner
from utils.states import get_state, get_all_states
from scrapers.school_scraper import scrape_school
from scrapers.college_scraper import scrape_college
from termcolor import colored

if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', '-s', type=str, required=False, metavar='State')
    parser.add_argument('--wait', '-w', type=int, default=0)
    parser.add_argument('--verbose', '-v', action='count', default=0, required=False)
    parser.add_argument('--scraper', '-sc', type=str, default='school', choices=['school', 'college'])
    parser.add_argument('--proxy', '-p', type=str, default = None)

    args = parser.parse_args()

    scraper = scrape_school
    if args.scraper.lower() == 'college':
      scraper = scrape_college

    if args.state:
      try:
        state_id = get_state(args.state)
        start_time = time.perf_counter()
        db, os = scraper(state_id, 1, wait=args.wait, proxy=args.proxy)
        stop_time = time.perf_counter()
        duration = str(datetime.timedelta(seconds=(stop_time - start_time)))
        print(f'Added to DB: {db}')
        print(f'Added to Opensearch: {os}')
        print(f'Completed in {duration}')
      except KeyError as error:
        print('State Abrreviation not found')
        print(colored(error, 'red'))
      except KeyboardInterrupt:
         print('[CTRL-C] Exiting...')
         sys.exit()
    else:
       try:
        states = get_all_states()
        start_time = time.perf_counter()
        total_db_count = 0
        total_os_count = 0
        for state in states:
          db, os = scraper(states[state], 1, wait=args.wait, proxy=args.proxy)
          total_db_count += db
          total_os_count += os

        stop_time = time.perf_counter()
        duration = str(datetime.timedelta(seconds=(stop_time - start_time)))
        print(f'Added to DB: {db}')
        print(f'Added to Opensearch: {os}')
        print(f'Completed in {duration}')
        print('')
       except KeyboardInterrupt:
          print('[CTRL-C] Exiting...')
          sys.exit()
    