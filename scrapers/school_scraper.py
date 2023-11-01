import datetime
import logging
import requests
import time
import unicodedata

from utils.banner import print_banner, print_stats
from bs4 import BeautifulSoup
from classes.address import Address
from classes.school import School
from utils.states import get_abbr
from termcolor import colored
from utils.constants import PUBLIC_SCHOOL_URL, PRIVATE_SCHOOL_URL

URLS = [PUBLIC_SCHOOL_URL, PRIVATE_SCHOOL_URL]
added_to_db = 0
added_to_opensearch = 0

def scrape_school(id, page=1, wait=0,):
   state = get_abbr(id)

   for url in URLS:
      _scrape_school(url, id, page, wait)

   print_banner(state)
   return added_to_db, added_to_opensearch

def _scrape_school(url, id, page=1, wait=0):
    logging.basicConfig(filename='logs/school_scraper.log', encoding='utf-8', level=logging.ERROR)
    global added_to_opensearch, added_to_db
    
    qs = f'&State={id}&SchoolPageNum={page}'
    response = requests.get(f'{url}{qs}')
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all(tag_selector)
    
    for i, table in enumerate(tables):
        if i == 0:
            continue
        
        datas = table.find_all('td')
        grade_range = datas[5].font.text.split('-')
        school_name = datas[1].a.text
        enrollment = datas[4].font.text
        phone = datas[2].font.text
        county = datas[3].font.text

        try:
           address = Address(unicodedata.normalize('NFKC', datas[1].font.font.text))
        except Exception as error:
           message = f'school_scraper:There was an issue getting address from {datas[1].font.font.text}:{error}'
           print(colored(message, 'red'))
           logging.error(message)
           continue

        try:
          int(enrollment.replace(',',''))
        except:
          enrollment = '0'

        school = School(
          school_name,
          address,
          phone,
          county,
          enrollment,
          grade_range[0],
          grade_range[-1]
        )

        if school.exists():
          message = f'[*] {school.name} in {school.address.zip} already Exists in DB'
          print(colored(message, 'light_magenta'))
          logging.info(message)
        else:
          school.save()
          added_to_db += 1
          time.sleep(wait)

        if school.index_exists():
          print_banner(school.address.state)
          print_stats(added_to_db, added_to_opensearch)

          message = f'[*] {school.name} in {school.address.zip} already Exists in Index'
          print(colored(message, 'light_magenta'))
          logging.info(message)
        else:
          added_to_opensearch += 1
          print(colored(f'[√] {school_name} being added to Index', 'green'))
          school.save_index()
          print_banner(school.address.state)
          print_stats(added_to_db, added_to_opensearch)
          time.sleep(wait)
           

    if len(tables) > 1: # when length is 1, this includes only the header and we're done
        page += 1
        _scrape_school(url, id, page=page, wait=wait)

def tag_selector(tag):
    return tag.name == "table" and tag.has_attr("width") and "99%" in tag.get("width") and "0" in tag.get("border")
