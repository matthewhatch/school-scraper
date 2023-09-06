import psycopg2
from classes.address import Address
from config import db_config
from soundex import soundex_generate
from termcolor import colored

class Account:
    def __init__(self, name: str, address: Address, phone) -> None:
        self.name = name
        self.address = address
        self.phone = phone
        self.db_params = db_config()
        self.soundex = soundex_generate(self.name, 15)
    
    def save(self):
        table_name = f'{self.__class__.__name__}s'
        sql = f"""
          INSERT into {table_name}(name, address1, city, state, zip, phone, soundex)
          VALUES(%s, %s, %s, %s ,%s, %s, %s)
        """

        conn = None

        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()
            cur.execute(sql, (self.name, self.address.address_1, self.address.city, self.address.state, self.address.zip, self.phone, self.soundex))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(colored(error, 'red'))
        finally:
            if conn is not None:
                conn.close()

    def exists(self):
        table_name = f'{self.__class__.__name__.lower()}s'
        sql = f"""SELECT count(id) from {table_name} where soundex=%s AND zip=%s"""
        results = False
        conn = None

        try:
          conn = psycopg2.connect(**self.db_params)
          cur = conn.cursor()
          cur.execute(sql, (self.soundex, self.address.zip))
          count = cur.fetchone()[0]

          if count != 0:
              results = True 
        except (Exception, psycopg2.DatabaseError) as error:
          print(error)
        finally:
          if conn is not None:
              conn.close()
        return results 