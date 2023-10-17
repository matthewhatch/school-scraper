import requests
import logging

from utils.banner import print_banner, print_stats
from bs4 import BeautifulSoup
from classes.address import Address
from classes.college import College
from utils.constants import COLLEGE_URL
from utils.states import get_abbr
from termcolor import colored

added_to_db = 0
added_to_opensearch = 0

def scrape_college(id, page=1, wait=0):
    global added_to_db, added_to_opensearch
    logging.basicConfig(filename='logs/college_scraper.log', encoding='utf-8', level=logging.ERROR)
    state_abbr = get_abbr(id)
    print_banner(state_abbr)
    print_stats(added_to_db, added_to_opensearch)
    qs=f'?s={state_abbr}&pg={page}'

    response = requests.get(f'{COLLEGE_URL}{qs}')
    if response.status_code == 200:   
      soup = BeautifulSoup(response.content, 'html.parser')
      colleges = soup.find_all(class_='itables')
      
      for college in colleges:  
        
        try:
          datas = college.find_all('tr')
          name = datas[0].h2.text
          address = Address(datas[0].text.replace(name, '').strip())
          try:
            phone = datas[1].text.split(':')[1].strip()
          except:
            phone = None

          try:
            enrollment = datas[6].find_all('td')[1].text.split(' ')[0].replace(',', '')
          except:
             enrollment = 0

          c = College(name, address, phone, enrollment)
          
          if c.exists():
              print_banner(state_abbr)
              print_stats(added_to_db, added_to_opensearch)

              db_message = f'[*] {name} in {c.address.zip} already Exists in DB'
              print(colored(db_message, 'light_magenta'))
          else:
              print_banner(state_abbr)
              print_stats(added_to_db, added_to_opensearch)

              c.save()
              added_to_db += 1
              print(colored(f'[√] {name} being added to DB', 'green'))

          if c.index_exists():
              index_message = f'[*] {name} in {c.address.zip} already Exists in Index'
              print(colored(index_message, 'light_magenta'))
          else:
              print(colored(f'[√] {name} being added to Index', 'green'))
              c.save_index()
              added_to_opensearch +=1
         
        except Exception as e:
           message = f'[x] There was an issue adding {name} with address {datas[0].text.replace(name, "").strip()}: {e}'
           print(colored(message, 'red'))
           logging.error(message)
           continue
    else:
       print(f'Error Status Code: {response.status_code}')

    if len(colleges) > 1:
       page += 1
       scrape_college(id, page, wait)
       print_banner(state_abbr)
       print_stats(added_to_db, added_to_opensearch)
    
    print_banner(state_abbr)
    return added_to_db, added_to_opensearch
