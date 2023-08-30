import psycopg2
from config import db_config
from soundex import soundex_generate
from termcolor import colored

class School:
   def __init__(self, name, address1, city, state, zip, phone, county, enrollment, low_grade, high_grade):
      self.name = name
      self.address1 = address1
      self.city = city
      self.state = state
      self.zip = zip
      self.phone = phone
      self.county = county
      self.enrollment = enrollment
      self.low_grade = low_grade
      self.high_grade = high_grade
      self.soundex = soundex_generate(self.name)
      self.db_params = db_config()

   def save(self):
      sql = """INSERT INTO schools(name, address1, city, state, county, enrollment, start_grade, end_grade, zip_code, soundex)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING name;"""

      conn = None

      try:
        conn = psycopg2.connect(**self.db_params)

        cur = conn.cursor()
        cur.execute(sql, (self.name, self.address1, self.city, self.state, self.county, self.enrollment.replace(',',''), self.low_grade, self.high_grade, self.zip, self.soundex))

        name = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(colored(f'[√] {name} has been saved!', 'green'))
      except (Exception, psycopg2.DatabaseError) as error:
         print(error)
      finally:
         if conn is not None:
            conn.close()

   def exists(self, soundex, zip):
      sql = """SELECT count(id) from schools where soundex=%s AND zip_code=%s"""
      results = False
      conn = None

      try:
         conn = psycopg2.connect(**self.db_params)
         cur = conn.cursor()
         cur.execute(sql, (soundex, zip))
         count = cur.fetchone()[0]

         if count != 0:
            results = True 
      except (Exception, psycopg2.DatabaseError) as error:
         print(error)
      finally:
         if conn is not None:
            conn.close()
      return results

   def print(self):
      print(f'Name: {self.name}')
      print(f'SoundEx: {self.soundex}')
      print(f'Address: {self.address1}')
      print(f'City: {self.city}')
      print(f'State: {self.state}')
      print(f'Zip: {self.zip}')
      print(f'Phone: {self.phone}')
      print(f'County: {self.county}')
      print(f'Enrollment: {self.enrollment}')
      print(f'Low Grade: {self.low_grade}')
      print(f'High Grade: {self.high_grade}')
      print('*'*50)
