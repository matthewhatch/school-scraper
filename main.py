import requests
import sys
import time
import unicodedata
import usaddress

from bs4 import BeautifulSoup
from states import get_state, get_all_states
from school import School
from termcolor import colored

PUBLIC_SCHOOL_URL = 'https://nces.ed.gov/ccd/schoolsearch/school_list.asp?Search=1&SpecificSchlTypes=all&IncGrade=-1&LoGrade=10&HiGrade=13'
PRIVATE_SCHOOL_URL = 'https://nces.ed.gov/surveys/pss/privateschoolsearch/school_list.asp?Search=1&NumOfStudentsRange=more&IncGrade=13&LoGrade=-1&HiGrade=-1'
URLS = [PUBLIC_SCHOOL_URL, PRIVATE_SCHOOL_URL]
school_count = 0

def tag_selector(tag):
    return tag.name == "table" and tag.has_attr("width") and "99%" in tag.get("width") and "0" in tag.get("border")

def main(url, id, page=1):
    global school_count 
    qs = f'&State={id}&SchoolPageNum={page}'
    response = requests.get(f'{url}{qs}')
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all(tag_selector)

    for i, table in enumerate(tables):
        if i == 0: 
            continue #skip the first row
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
           # TODO: write detailed error to log
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

        try:
           int(enrollment)
        except:
           enrollment = '0'

        school = School(
           school_name,
           address1,
           city,
           state,
           zip,
           datas[2].font.text, # Phone
           datas[3].font.text, # County
           enrollment, # Enrollment
           grade_range[0],
           grade_range[-1]
        )

        school_count += 1
        exists = school.exists(school.soundex, school.zip)

        if exists:
           print(colored(f'[*] {school_name} in {zip} already Exists in DB', 'light_magenta'))
           continue
        
        school.save()

    if len(tables) > 1: # when length is 1, this includes only the header and we're done
        page += 1
        main(url, id, page=page)

if __name__ == '__main__':
    start_time = time.perf_counter()
    if len(sys.argv) == 2:
      state_abbr = sys.argv[1]

      try:
        state_id = get_state(state_abbr)
        for url in URLS:
          main(url, state_id, 1)
      except KeyError:
        print('State Abrreviation not found')
      except KeyboardInterrupt:
         print('[CTRL-C] Exiting...')
         sys.exit()
    else:
       try:
        states = get_all_states()
        for state in states:
            for url in URLS:
              main(url, states[state], 1)
       except KeyboardInterrupt:
          print('[CTRL-C] Exiting...')
          sys.exit()

    stop_time = time.perf_counter()
    duration = stop_time - start_time
    print(f'Total Found: {school_count}\r\nElapsed Time: {duration:0.2f} Seconds')

    