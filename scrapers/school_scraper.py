
import datetime
import logging
import requests
import time
import unicodedata

from banner import print_banner
from bs4 import BeautifulSoup
from classes.address import Address
from classes.school import School
from utils.states import get_abbr
from termcolor import colored

PUBLIC_SCHOOL_URL = 'https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&SpecificSchlTypes=all&IncGrade=-1&LoGrade=10&HiGrade=13'
PRIVATE_SCHOOL_URL = 'https://nces.ed.gov/surveys/pss/privateschoolsearch/school_list.asp?Search=1&NumOfStudentsRange=more&IncGrade=13&LoGrade=-1&HiGrade=-1'
URLS = [PUBLIC_SCHOOL_URL, PRIVATE_SCHOOL_URL]
school_count = 0

def scrape_school(id, page=1, wait=0,):
   start_time = time.perf_counter()
   state = get_abbr(id)

   for url in URLS:
      _scrape_school(url, id, page, wait)

   print_banner(state)
   stop_time = time.perf_counter()
   duration = str(datetime.timedelta(seconds=(stop_time - start_time)))
   print(f'Total Found: {school_count}\r\nElapsed Time: {duration}')

def _scrape_school(url, id, page=1, wait=0):
    logging.basicConfig(filename='school_scraper.log', encoding='utf-8', level=logging.ERROR)
    global school_count
    
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
           message = f'school_scraper:There was ab issue getting address from {datas[1]}:{error}'
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
          print_banner(school.address.state)  
          message = f'[*] {school.name} in {school.address.zip} already Exists in DB'
          print(colored(message, 'light_magenta'))
          logging.info(message)
          continue
        
        school.save()
        school_count += 1
        time.sleep(wait)

    if len(tables) > 1: # when length is 1, this includes only the header and we're done
        page += 1
        _scrape_school(url, id, page=page, wait=wait)

def tag_selector(tag):
    return tag.name == "table" and tag.has_attr("width") and "99%" in tag.get("width") and "0" in tag.get("border")
