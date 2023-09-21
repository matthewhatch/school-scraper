import requests

from banner import print_banner
from bs4 import BeautifulSoup
from classes.address import Address
from classes.college import College
from states import get_abbr
from termcolor import colored

URL = 'https://nces.ed.gov/collegenavigator'
college_count = 0

def scrape_college(id, page=1, wait=0):
    global college_count

    state_abbr = get_abbr(id)
    qs=f'?s={state_abbr}&pg={page}'

    response = requests.get(f'{URL}{qs}')
    if response.status_code == 200:   
      soup = BeautifulSoup(response.content, 'html.parser')
      colleges = soup.find_all(class_='itables')
      
      for college in colleges:  
        print_banner(state_abbr)
        try:
          datas = college.find_all('tr')
          name = datas[0].h2.text
          address = Address(datas[0].text.replace(name, '').strip())
          phone = datas[1].text.split(':')[1].strip()
          enrollment = datas[6].find_all('td')[1].text.split(' ')[0].replace(',', '')
  
          c = College(name, address, phone, enrollment)
          
          if c.exists():
              print_banner(state_abbr)
              message = f'[*] {name} in {c.address.zip} already Exists in DB'
              print(colored(message, 'light_magenta'))
              continue

          c.save()
 
          print(colored(f'[√] {name} being added', 'green'))
          college_count += 1
        except Exception as e:
           print(colored(f'There was an issue adding {name}: {e}', 'red'))
           continue
    else:
       print(f'Error Status Code: {response.status_code}')

    if len(colleges) > 1:
       page += 1
       scrape_college(id, page, wait)
       print_banner(state_abbr)
       print(colored(f'Added {college_count}!', 'green'))
