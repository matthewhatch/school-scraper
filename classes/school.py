import psycopg2

from classes.account import Account
from classes.address import Address
from termcolor import colored
from banner import print_banner

class School(Account):
   def __init__(self, name: str, address: Address, phone, county, enrollment, low_grade, high_grade):
      super().__init__(name, address, phone)
      self.county = county
      self.enrollment = enrollment
      self.low_grade = low_grade
      self.high_grade = high_grade

   def save(self):
      sql = """INSERT INTO schools(name, address1, city, state, county, enrollment, start_grade, end_grade, zip, soundex, phone)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING name;"""

      conn = None

      try:
        conn = psycopg2.connect(**self.db_params)

        cur = conn.cursor()
        cur.execute(sql, (self.name, self.address.address_1, self.address.city, self.address.state, self.county, self.enrollment.replace(',',''), self.low_grade, self.high_grade, self.address.zip, self.soundex, self.phone))

        name = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print_banner(self.address.state)
        print(colored(f'[√] {name} has been saved!', 'green'))
      except (Exception, psycopg2.DatabaseError) as error:
         print(colored(f'Error in {self.__class__.__name__}: {error}'))
      finally:
         if conn is not None:
            conn.close()

