#!./env/bin/python
import argparse
import sys

from banner import print_banner
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
    args = parser.parse_args()

    scraper = scrape_school
    if args.scraper.lower() == 'college':
      scraper = scrape_college

    if args.state:
      try:
        state_id = get_state(args.state)
        scraper(state_id, 1, wait=args.wait)
      except KeyError as error:
        print('State Abrreviation not found')
        print(colored(error, 'red'))
      except KeyboardInterrupt:
         print('[CTRL-C] Exiting...')
         sys.exit()
    else:
       try:
        states = get_all_states()
        for state in states:
          scraper(states[state], 1, wait=args.wait)
       except KeyboardInterrupt:
          print('[CTRL-C] Exiting...')
          sys.exit()
    