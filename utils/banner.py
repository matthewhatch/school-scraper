import os
from termcolor import colored

def print_banner(state=None):
  BANNER = f"""
 _____      _                 _ _____                                
/  ___|    | |               | /  ___|                               
\ `--.  ___| |__   ___   ___ | \ `--.  ___ _ __ __ _ _ __   ___ _ __ 
 `--. \/ __| '_ \ / _ \ / _ \| |`--. \/ __| '__/ _` | '_ \ / _ \ '__|
/\__/ / (__| | | | (_) | (_) | /\__/ / (__| | | (_| | |_) |  __/ |   
\____/ \___|_| |_|\___/ \___/|_\____/ \___|_|  \__,_| .__/ \___|_|   
                                                    | |              
                                                    |_|              

  SchoolScraper - Scraping All the things...
  Author: M. Hatch
  """

  if state:
    BANNER = f'{BANNER}\nState: {state}'

  os.system('clear')
  print(colored(BANNER, 'cyan'))
  print(colored(70*('-'), 'cyan'))

def print_stats(db_count, opensearch_count):
    print(colored(f'New Database Records: {db_count}','green'))
    print(colored(f'New OpenSearch Records: {opensearch_count}','green'))
    print(colored(70*('-'), 'cyan'))
