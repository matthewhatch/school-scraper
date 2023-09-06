
import datetime
import logging
import requests
import time
import unicodedata
import usaddress

from banner import print_banner
from bs4 import BeautifulSoup
from classes.school import School
from states import get_abbr
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
    state = get_abbr(id)

    qs = f'&State={id}&SchoolPageNum={page}'
    response = requests.get(f'{url}{qs}')
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all(tag_selector)
    
    for i, table in enumerate(tables):
        if i == 0:
            continue

        address_number = None
        street_name = None
        street_name_post_type = None
        city = None
        state = None
        zip = None
        
        datas = table.find_all('td')
        grade_range = datas[5].font.text.split('-')
        school_name = datas[1].a.text
        address = unicodedata.normalize('NFKC', datas[1].font.font.text)
        
        try:
          parsed_address, _ = usaddress.tag(address)
        except (usaddress.RepeatedLabelError) as repeatLabelError:
          print(colored(f'[x] There was an issue with {address}', 'red'))
          logging.error(repeatLabelError)
          continue

        for component, value in parsed_address.items():
          if component == 'ZipCode':
              zip = value
          elif component == 'PlaceName':
              city = value
          elif component == 'AddressNumber':
              address_number = value
          elif component == 'StreetName':
              street_name = value
          elif component == 'StreetNamePostType':
              street_name_post_type = value
          elif component == 'StateName':
              state = value

        address1 = f'{address_number} {street_name} {street_name_post_type}' 
        enrollment = datas[4].font.text
        phone = datas[2].font.text
        county = datas[3].font.text

        try:
          int(enrollment.replace(',',''))
        except:
          enrollment = '0'

        school = School(
          school_name,
          address1,
          city,
          state,
          zip,
          phone,
          county,
          enrollment,
          grade_range[0],
          grade_range[-1]
        )

        school_count += 1
        exists = school.exists(school.soundex, school.zip)

        if exists:
          print_banner(state)
          message = f'[*] {school_name} in {zip} already Exists in DB'
          print(colored(message, 'light_magenta'))
          logging.info(message)
          continue
        
        school.save()
        time.sleep(wait)

    if len(tables) > 1: # when length is 1, this includes only the header and we're done
        page += 1
        _scrape_school(url, id, page=page, wait=wait)

def tag_selector(tag):
    return tag.name == "table" and tag.has_attr("width") and "99%" in tag.get("width") and "0" in tag.get("border")
