import json
import logging
import psycopg2
import requests

from classes.address import Address
from utils.config import get_config
from requests.auth import HTTPBasicAuth
from utils.soundex import soundex_generate
from termcolor import colored
db_params = get_config()
os_params = get_config(filename='opensearch.ini', section='opensearch')

class Account:
    def __init__(self, name: str, address: Address, phone) -> None:
        self.name = name
        self.address = address
        self.phone = phone
        self.soundex = soundex_generate(self.name, 15)
        logging.basicConfig(filename=f'{self.__class__.__name__.lower()}.log')

    def generate_sql(self):
        table_name = f'{self.__class__.__name__}s'
        return f"""
          INSERT into {table_name}(name, address1, city, state, zip, phone, soundex)
          VALUES(%s, %s, %s, %s ,%s, %s, %s)
        """
    
    def execute_sql(self, cursor, sql):
        cursor.execute(sql, self.name,
            self.address.address_1,
            self.address.city,
            self.address.state,
            self.address.zip,
            self.phone,
            self.soundex)

    def save(self):
        sql = self.generate_sql()
        conn = None

        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()
            self.execute_sql(cur, sql)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(colored(error, 'red'))
        finally:
            if conn is not None:
                conn.close()

    def save_index(self):
        try:
          auth_token = HTTPBasicAuth(os_params['username'],os_params['password'])
          url = os_params['url']
          headers = {
              'Content-Type': 'application/json',
          }
          data = json.dumps(self, default=lambda o: o.__dict__)
          requests.post(url, data, headers=headers, auth=auth_token)

        except Exception as e:
            print(colored(e, 'red' ))
    
    def exists(self):
        table_name = f'{self.__class__.__name__.lower()}s'
        sql = f"""SELECT count(id) from {table_name} where soundex=%s AND zip=%s"""
        results = False
        conn = None

        try:
          conn = psycopg2.connect(**db_params)
          cur = conn.cursor()
          cur.execute(sql, (self.soundex, self.address.zip))
          count = cur.fetchone()[0]

          if count != 0:
              results = True 
        except (Exception, psycopg2.DatabaseError) as error:
          message = f'Error in {self.__class__.__name__}: {error}'
          logging.error(message)
          print(colored(message, 'red'))
        finally:
          if conn is not None:
              conn.close()
        return results
    
    def index_exists(self):
      response = None
      auth_token = HTTPBasicAuth(os_params['username'], os_params['password'])
      url = os_params['graph_url']
      headers = { 'Content-Type': 'application/json' }

      data = {
         "query": {
            "match_bool_prefix": {
               "soundex": self.soundex
            }
         }
      }

      try:
        response = requests.post(url, json.dumps(data), headers=headers, auth=auth_token)
      except Exception as e:
         logging.error(e)
         print(e)
      if response.status_code == 404:
         return False
      
      content = json.loads(response.text)
      return int(content['hits']['total']['value']) != 0
    