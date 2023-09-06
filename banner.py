import os
from termcolor import colored

def print_banner(state=None):
  BANNER = f"""
   ___                             _  ___                                          
  (  _`\                          ( )(  _`\                                        
  | (_(_)   _ _  _   _    _ _    _| || (_(_)   ___  _ __   _ _  _ _      __   _ __ 
  `\__ \  /'_` )( ) ( ) /'_` ) /'_` |`\__ \  /'___)( '__)/'_` )( '_`\  /'__`\( '__)
  ( )_) |( (_) || (_) |( (_| |( (_| |( )_) |( (___ | |  ( (_| || (_) )(  ___/| |   
  `\____)`\__, |`\___/'`\__,_)`\__,_)`\____)`\____)(_)  `\__,_)| ,__/'`\____)(_)   
             | |                                               | |                 
             (_)                                               (_)                 

  SquadScraper - Scraping All the things...
  Author: M. Hatch
  """

  if state:
    BANNER = f'{BANNER}\nState: {state}'
  
  os.system('clear')
  print(colored(BANNER, 'cyan'))