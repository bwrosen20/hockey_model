from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app import app
from urllib.request import Request, urlopen
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Game, Player, Goalie, GoalieGame, PlayerGame, FinalBet
from unidecode import unidecode
import requests
import time
import ipdb

html = requests.get(f"https://www.baseball-reference.com/leagues/majors/2022-schedule.shtml", headers={'User-Agent':"Mozilla/5.0"})
doc = BeautifulSoup(html.text, 'html.parser')
rows = doc.select('p.game')


total_games= 0
even_games = 0
odd_games = 0



for game in rows:
    total_games+=1
    game_value = 0  
    odd_or_even = "odd"

    try: 
        values = [int(item.replace('(','').replace(')','').replace('\n','')) for item in game.text.split(' ') if '(' in item]
    except ValueError:
        continue

    for item in values:
        game_value +=item

    if game_value%2==0:
        even_games+=1
        odd_or_even = "even"
    else:
        odd_games+=1
        odd_or_even = "odd"

    print(f'{values[0]}, {values[1]}, {odd_or_even}')

print(f'Total Games: {total_games}')
print(f'Odd Games: {odd_games}')
print(f'Even Games: {even_games}')

ipdb.set_trace()


